"""CLI argument parsing and command handling."""

import argparse
import json
import sys
from typing import Optional

from . import db


def output_success(data: dict) -> None:
    """Output success response in JSON."""
    print(json.dumps({"success": True, **data}, indent=2))


def output_error(message: str) -> None:
    """Output error response in JSON."""
    print(json.dumps({"success": False, "error": message}, indent=2))
    sys.exit(1)


def cmd_create(args: argparse.Namespace) -> None:
    """Handle create command."""
    try:
        task = db.create_task(args.name, args.spec, args.agent)
        output_success({"task": task})
    except Exception as e:
        output_error(str(e))


def cmd_list(args: argparse.Namespace) -> None:
    """Handle list command."""
    try:
        tasks = db.list_tasks(args.agent, args.limit, args.offset)
        output_success({"tasks": tasks})
    except Exception as e:
        output_error(str(e))


def cmd_pop(args: argparse.Namespace) -> None:
    """Handle pop command."""
    try:
        task = db.pop_task(args.agent)
        if task:
            output_success({"task": task})
        else:
            output_error(f"No undone tasks found for agent: {args.agent}")
    except Exception as e:
        output_error(str(e))


def cmd_get(args: argparse.Namespace) -> None:
    """Handle get command."""
    try:
        task = db.get_task(args.identifier)
        if task:
            task["comments"] = db.get_comments(task["id"])
            output_success({"task": task})
        else:
            output_error(f"Task not found: {args.identifier}")
    except Exception as e:
        output_error(str(e))


def cmd_done(args: argparse.Namespace) -> None:
    """Handle done command."""
    try:
        task = db.mark_done(args.identifier)
        if task:
            output_success({"task": task})
        else:
            output_error(f"Task not found: {args.identifier}")
    except Exception as e:
        output_error(str(e))


def cmd_comment(args: argparse.Namespace) -> None:
    """Handle comment command."""
    try:
        task = db.get_task(args.identifier)
        if not task:
            output_error(f"Task not found: {args.identifier}")
        comment = db.add_comment(task["id"], args.body, args.agent)
        output_success({"comment": comment})
    except Exception as e:
        output_error(str(e))


def cmd_rm(args: argparse.Namespace) -> None:
    """Handle rm command."""
    try:
        result = db.delete_task(args.identifier)
        if result:
            output_success({"task": result})
        else:
            output_error(f"Task not found: {args.identifier}")
    except Exception as e:
        output_error(str(e))


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="task-cli",
        description="Task management CLI tool"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # create command
    create_parser = subparsers.add_parser("create", help="Create a new task")
    create_parser.add_argument("name", help="Task name")
    create_parser.add_argument("spec", help="Task specification")
    create_parser.add_argument("--agent", help="Agent name to assign")
    create_parser.set_defaults(func=cmd_create)
    
    # list command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--agent", help="Filter by agent name")
    list_parser.add_argument("--limit", type=int, help="Maximum number of tasks to return")
    list_parser.add_argument("--offset", type=int, help="Number of tasks to skip")
    list_parser.set_defaults(func=cmd_list)
    
    # pop command
    pop_parser = subparsers.add_parser("pop", help="Get oldest task for an agent")
    pop_parser.add_argument("--agent", required=True, help="Agent name")
    pop_parser.set_defaults(func=cmd_pop)
    
    # get command
    get_parser = subparsers.add_parser("get", help="Get a task by name or id")
    get_parser.add_argument("identifier", help="Task name or id")
    get_parser.set_defaults(func=cmd_get)
    
    # done command
    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("identifier", help="Task name or id")
    done_parser.set_defaults(func=cmd_done)
    
    # comment command
    comment_parser = subparsers.add_parser("comment", help="Add a comment to a task")
    comment_parser.add_argument("identifier", help="Task name or id")
    comment_parser.add_argument("body", help="Comment text")
    comment_parser.add_argument("--agent", help="Agent name")
    comment_parser.set_defaults(func=cmd_comment)
    
    # rm command
    rm_parser = subparsers.add_parser("rm", help="Delete a task")
    rm_parser.add_argument("identifier", help="Task name or id")
    rm_parser.set_defaults(func=cmd_rm)
    
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
