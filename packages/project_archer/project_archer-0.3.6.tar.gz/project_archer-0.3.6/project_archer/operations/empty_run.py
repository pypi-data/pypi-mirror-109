from project_archer.environment.read_shell_parameters import current_project
from project_archer.operations.list_projects import list_projects
from project_archer.operations.select_project import read_project_data

from termcolor_util import blue, green


def empty_project_run(args, env):
    project = current_project(args.internalRunMode)
    if project:
        project_name = project
    else:
        project_name = "<none>"

    list_projects(args, env)
    env.log("Current " + args.internalRunMode + ": " + blue(project_name))

    if not project:
        return

    project_data = read_project_data(project_name, args.internalRunMode)

    if not project_data["commands"]:
        return

    env.log("Commands")
    for command in project_data["commands"]:
        env.log("- " + green(command))
