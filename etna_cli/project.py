import click
from etna_cli import config
from etna_cli.utils import print_table


@click.group(name="project")
def main():
    """Projects."""


def is_validated(validation: str = None) -> str:
    """Check if validated."""
    if validation == "Validée":
        validated = "YES"
    elif validation == "Non validée":
        validated = "NO"
    else:
        validated = "Not yet"
    return validated


@main.command()
def list():
    """List projects."""
    wrapper = config.setup_api()
    projects = wrapper.get_projects()
    final_list = []
    header = ('Name', 'UV', 'starts at', 'ends on', 'Time', 'Validated')
    for project in projects:
        project_list = []
        project_list.append(project['long_name'])
        project_list.append(project['uv_name'])
        project_list.append(project['date_start'])
        project_list.append(project['date_end'])
        project_list.append(f"{int(project['duration']) / 3600} hours")
        project_list.append(is_validated(project['validation']))
        final_list.append(project_list)
    print_table(final_list, header)


@main.command()
@click.option("-t", "--type", "type_", help="[cours|project|quest]")
def activites(type_: str = None):
    """List activites."""
    wrapper = config.setup_api()
    projects = wrapper.get_projects()

    for project in projects:
        pid = project['id']
        activites = wrapper.get_project_activites(pid)
        handle_activites(activites, type_)


def handle_activites(activites: dict, act_type: str = None):
    """Handle different types of activites."""
    for activity in activites:
        if act_type is not None:
            if activity['type'] == act_type:
                print_activity(activity)
        else:
            print_activity(activity)


def print_activity(quest: dict):
    """Print content of activity."""
    val = "Yes"
    print("========================")
    print("name         : {}".format(quest['name']))
    print("coef         : {}".format(quest['coefficient']))
    print("type         : {}".format(quest['type']))
    if quest['eliminate'] is None:
        val = "No"
    print("eliminate    : {}".format(val))

    try:
        print("mark min     : {}".format(quest['mark_min']))
        print("mark max     : {}".format(quest['mark_max']))
        print("average mark : {}".format(quest['average_mark']))
        print("student mark : {}".format(quest['student_mark']))
    except KeyError:
        pass

    print("starts on    : {}".format(quest['date_start']))
    print("ends on      : {}".format(quest['date_end']))
