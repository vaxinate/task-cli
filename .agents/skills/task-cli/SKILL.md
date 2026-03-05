---
name: task-cli
description: Task management CLI tool for creating, tracking, and managing tasks with comments. Use when the user wants to create tasks, list tasks, mark tasks as done, add comments to tasks, or manage task workflow using the task-cli tool.
---

# task-cli

A command-line task management tool backed by SQLite. Tasks are stored in `~/.task-cli/tasks.db`.

## Commands

### Create a task
```bash
task-cli create "<name>" "<spec>" [--agent <agent_name>]
```

### List undone tasks
```bash
task-cli list [--agent <agent_name>] [--limit <n>] [--offset <n>]
```

### Get oldest task for an agent
```bash
task-cli pop --agent "<agent_name>"
```

### Get a specific task (includes comments)
```bash
task-cli get <name|id>
```

### Mark a task as done
```bash
task-cli done <name|id>
```

### Add a comment to a task
```bash
task-cli comment <name|id> "<body>" [--agent <agent_name>]
```

### Delete a task
```bash
task-cli rm <name|id>
```

## Task Schema

- `id`: Integer primary key
- `created_at`: Unix timestamp
- `name`: Unique task name
- `spec`: Task description/specification
- `agent_name`: Optional agent assignment
- `done`: Unix timestamp when completed, or null
- `comments`: Array of comments (only in `get` response)

## Comment Schema

- `id`: Integer primary key
- `task_id`: Reference to task
- `created_at`: Unix timestamp
- `body`: Comment text
- `agent_name`: Optional agent name

## Output Format

All commands output JSON. Success: `{"success": true, ...}`. Error: `{"success": false, "error": "..."}`.

## Best Practices

- Use descriptive task names (kebab-case recommended)
- Use `--agent` to assign tasks to specific agents
- Use `task-cli get` to view task details and comment history
- Add comments to track progress or notes on tasks
