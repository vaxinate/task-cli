# task-cli

A simple command-line task management tool backed by SQLite.

## Installation

```bash
# Clone the repository
git clone https://github.com/vaxinate/task-cli.git
cd task-cli

# Install in editable mode
pip install -e .
```

The `task-cli` command will now be available from anywhere.

## Usage

### Create a task

```bash
task-cli create "<name>" "<task_spec>" [--agent <agent_name>]
```

Example:
```bash
$ task-cli create schedule-9012 "schedule email 9012" --agent oscar
{
  "success": true,
  "task": {
    "id": 201,
    "name": "schedule-9012",
    "spec": "schedule email 9012",
    "agent_name": "oscar",
    "done": false
  }
}
```

Create a task without an agent:
```bash
$ task-cli create schedule-9012 "schedule email 9012"
{
  "success": true,
  "task": {
    "id": 201,
    "created_at": 1772667176,
    "name": "schedule-9012",
    "spec": "schedule email 9012",
    "agent_name": null,
    "done": false
  }
}
```

### List tasks

```bash
task-cli list [--agent "<agent_name>"]
```

Lists all undone tasks. If `--agent` is specified, only shows tasks for that agent. Tasks are ordered by creation time.

Example:
```bash
$ task-cli list --agent tim
{
  "success": true,
  "tasks": [
    {
      "id": 249,
      "created_at": 1772667176,
      "name": "schedule-2201",
      "spec": "schedule email 2201",
      "agent_name": "tim",
      "done": false
    },
    {
      "id": 201,
      "created_at": 1772661654,
      "name": "schedule-9012",
      "spec": "schedule email 9012",
      "agent_name": "tim",
      "done": false
    }
  ]
}
```

### Get the oldest task for an agent

```bash
task-cli pop --agent "<agent_name>"
```

Returns the oldest undone task for the agent (does not delete it).

Example:
```bash
$ task-cli pop --agent tim
{
  "success": true,
  "task": {
    "id": 201,
    "created_at": 1772661654,
    "name": "schedule-9012",
    "spec": "schedule email 9012",
    "agent_name": "tim",
    "done": false
  }
}
```

### Get a specific task

```bash
task-cli get <name|id>
```

Example:
```bash
$ task-cli get 201
{
  "success": true,
  "task": {
    "id": 201,
    "created_at": 1772661654,
    "name": "schedule-9012",
    "spec": "schedule email 9012",
    "agent_name": "tim",
    "done": false
  }
}
```

### Mark a task as done

```bash
task-cli done <name|id>
```

Example:
```bash
$ task-cli done 201
{
  "success": true,
  "task": {
    "id": 201,
    "created_at": 1772661654,
    "name": "schedule-9012",
    "spec": "schedule email 9012",
    "agent_name": "tim",
    "done": true
  }
}
```

### Delete a task

```bash
task-cli rm <name|id>
```

Example:
```bash
$ task-cli rm 201
{
  "success": true,
  "task": {
    "id": 201
  }
}
```

## Data Storage

Tasks are stored in a SQLite database at:

```
~/.task-cli/tasks.db
```

The database and schema are created automatically on first use.

## Command Reference

| Command | Description |
|---------|-------------|
| `create <name> <spec> [--agent <agent>]` | Create a new task |
| `list --agent <agent>` | List undone tasks for an agent |
| `pop --agent <agent>` | Get oldest undone task for an agent |
| `get <name\|id>` | Get a task by name or ID |
| `done <name\|id>` | Mark a task as complete |
| `rm <name\|id>` | Delete a task |

## Project Structure

```
task-cli/
├── .gitignore           # Ignores generated files (__pycache__, *.egg-info)
├── KIMI.md              # Original usage specification
├── README.md            # This file
├── pyproject.toml       # Package configuration for pip install
├── task-cli             # Executable entry point
└── task_cli/            # Python package
    ├── __init__.py
    ├── cli.py           # CLI argument parsing & command handling
    └── db.py            # Database operations (SQLite)
```

## Output Format

All commands output JSON to stdout. Successful operations include `"success": true`. Errors include `"success": false` and an `"error"` message.
