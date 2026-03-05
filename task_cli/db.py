"""Database operations for task-cli."""

import os
import sqlite3
from pathlib import Path
from typing import Optional


def get_db_path() -> Path:
    """Get the path to the SQLite database file."""
    data_dir = Path.home() / ".task-cli"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "tasks.db"


def get_connection() -> sqlite3.Connection:
    """Get a database connection with row factory."""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize the database with schema."""
    conn = get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at INTEGER NOT NULL DEFAULT (unixepoch()),
                name TEXT NOT NULL UNIQUE,
                spec TEXT NOT NULL,
                agent_name TEXT,
                done INTEGER DEFAULT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                created_at INTEGER NOT NULL DEFAULT (unixepoch()),
                body TEXT NOT NULL,
                agent_name TEXT,
                FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
            )
        """)
        conn.commit()
    finally:
        conn.close()


def row_to_dict(row: sqlite3.Row) -> dict:
    """Convert a sqlite3.Row to a dictionary."""
    return {key: row[key] for key in row.keys()}


def create_task(name: str, spec: str, agent_name: Optional[str] = None) -> dict:
    """Create a new task."""
    init_db()
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO tasks (name, spec, agent_name) VALUES (?, ?, ?)",
            (name, spec, agent_name)
        )
        task_id = cursor.lastrowid
        conn.commit()
        
        row = conn.execute(
            "SELECT id, created_at, name, spec, agent_name, done FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()
        return row_to_dict(row)
    finally:
        conn.close()


def list_tasks(agent_name: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> list:
    """List all undone tasks. If agent_name is provided, filter by agent."""
    init_db()
    conn = get_connection()
    try:
        params = []
        if agent_name:
            where_clause = "WHERE agent_name = ? AND done IS NULL"
            params.append(agent_name)
        else:
            where_clause = "WHERE done IS NULL"
        
        query = f"SELECT id, created_at, name, spec, agent_name, done FROM tasks {where_clause} ORDER BY created_at ASC"
        
        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)
        if offset is not None:
            query += " OFFSET ?"
            params.append(offset)
        
        rows = conn.execute(query, params).fetchall()
        return [row_to_dict(row) for row in rows]
    finally:
        conn.close()


def pop_task(agent_name: str) -> Optional[dict]:
    """Get the oldest undone task for an agent (does not delete)."""
    init_db()
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT id, created_at, name, spec, agent_name, done FROM tasks WHERE agent_name = ? AND done IS NULL ORDER BY created_at ASC LIMIT 1",
            (agent_name,)
        ).fetchone()
        return row_to_dict(row) if row else None
    finally:
        conn.close()


def get_task(identifier: str) -> Optional[dict]:
    """Get a task by name or id."""
    init_db()
    conn = get_connection()
    try:
        # Try by id first
        if identifier.isdigit():
            row = conn.execute(
                "SELECT id, created_at, name, spec, agent_name, done FROM tasks WHERE id = ?",
                (int(identifier),)
            ).fetchone()
            if row:
                return row_to_dict(row)
        
        # Try by name
        row = conn.execute(
            "SELECT id, created_at, name, spec, agent_name, done FROM tasks WHERE name = ?",
            (identifier,)
        ).fetchone()
        return row_to_dict(row) if row else None
    finally:
        conn.close()


def mark_done(identifier: str) -> Optional[dict]:
    """Mark a task as done."""
    init_db()
    conn = get_connection()
    try:
        # Find task first
        task = get_task(identifier)
        if not task:
            return None
        
        conn.execute(
            "UPDATE tasks SET done = unixepoch() WHERE id = ?",
            (task["id"],)
        )
        conn.commit()
        
        return get_task(str(task["id"]))
    finally:
        conn.close()


def delete_task(identifier: str) -> Optional[dict]:
    """Delete a task by name or id."""
    init_db()
    conn = get_connection()
    try:
        # Find task first
        task = get_task(identifier)
        if not task:
            return None
        
        task_id = task["id"]
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        
        return {"id": task_id}
    finally:
        conn.close()


def add_comment(task_id: int, body: str, agent_name: Optional[str] = None) -> dict:
    """Add a comment to a task."""
    init_db()
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO comments (task_id, body, agent_name) VALUES (?, ?, ?)",
            (task_id, body, agent_name)
        )
        comment_id = cursor.lastrowid
        conn.commit()
        
        row = conn.execute(
            "SELECT id, task_id, created_at, body, agent_name FROM comments WHERE id = ?",
            (comment_id,)
        ).fetchone()
        return row_to_dict(row)
    finally:
        conn.close()


def get_comments(task_id: int) -> list:
    """Get all comments for a task, ordered by creation time."""
    init_db()
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT id, task_id, created_at, body, agent_name FROM comments WHERE task_id = ? ORDER BY created_at ASC",
            (task_id,)
        ).fetchall()
        return [row_to_dict(row) for row in rows]
    finally:
        conn.close()
