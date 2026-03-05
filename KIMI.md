Create a task:
task-cli create "<name>" "<task_spec>" [--assign <agent_name>]

List tasks assigned to <agent_name>:
task-cli list --agent "<agent_name>"

Get the oldest task assigned to <agent_name>:
task-cli pop --agent "<agent_name>"

Get any task:
task-cli get <name|id>

Mark task done/complete:
task-cli done <name|id>

Examples:

$ task-cli create schedule-9012 "schedule email 9012" --agent oscar
{
  success: true,
  task: {
    id: 201
    name: "schedule-9012",
    spec: "schedule email 9012",
    agent_name: "oscar",
    done: false
  }
}

$ task-cli create schedule-9012 "schedule email 9012"
{
  success: true,
  task: {
    id: 201
    created_at: 1772667176,
    name: "schedule-9012",
    spec: "schedule email 9012",
    agent_name: null,
    done: false
  }
}

$ task-cli list --agent tim
{
  success: true,
  tasks: [
    {
      id: 249
      created_at: 1772667176,
      name: "schedule-2201",
      spec: "schedule email 2201",
      agent_name: "tim",
      done: false
    },
    {
      id: 201
      created_at: 1772661654,
      name: "schedule-9012",
      spec: "schedule email 9012",
      agent_name: "tim"
      done: false
    }
  ]
}

$ task-cli pop --agent tim
{
  success: true,
  task: {
    id: 201
    created_at: 1772661654,
    name: "schedule-9012",
    spec: "schedule email 9012",
    agent_name: "tim",
    done: false
  }
}

$ task-cli get 201
{
  success: true,
  task: {
    id: 201
    created_at: 1772661654,
    name: "schedule-9012",
    spec: "schedule email 9012",
    agent_name: "tim",
    done: false
  }
}

$ task-cli done 201
{
  success: true,
  task: {
    id: 201
    created_at: 1772661654,
    name: "schedule-9012",
    spec: "schedule email 9012",
    agent_name: "tim",
    done: true
  }
}

$ task-cli rm 201
{
  success: true,
  task: {
    id: 201
  }
}
