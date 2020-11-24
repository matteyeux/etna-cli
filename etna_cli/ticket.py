import click
from tabulate import tabulate
from etna_cli import config
from etna_cli.utils import prettify_lists


@click.group(name="ticket")
def main():
    """Tickets."""


@main.command(name="create")
@click.option("-t", "--title", required=True, help="set title")
@click.option("-c", "--content", required=True,
              help="set content")
@click.option("-T", "--tags", required=True,
              help="specify tags separeted by commas")
@click.option("-s", "--students",
              help="specify one or more student separated by commas")
def create_ticket(title: str, content: str, tags: str, students: str = None):
    """Create ticket."""
    wrapper = config.setup_api()

    tag_list = tags.split(',')
    if students:
        student_list = students.split(',')
    else:
        student_list = None
    wrapper.open_ticket(title, content, tag_list, student_list)


@main.command(name="list")
@click.option("-d", "--details", is_flag=True,
              help="show more details about tickets")
def list(details: bool = False):
    """List tickets."""
    wrapper = config.setup_api()
    tickets = wrapper.get_tickets()
    if details:
        header = ("id", "title", "created at", "updated at", "closed at",
                  "login", "last edit", "last author")
    else:
        header = ("id", "title", "created by", "last edit", "last author")
    final_list = []
    for ticket in tickets['data']:
        ticket_list = []
        ticket_list.append(ticket['id'])
        ticket_list.append(ticket['title'])
        if details:
            ticket_list.append(ticket['created_at'])
            ticket_list.append(ticket['updated_at'])
            ticket_list.append(ticket['closed_at'])
        ticket_list.append(ticket['creator']['login'])
        ticket_list.append(ticket['last_edit']['login'])
        ticket_list.append(ticket['last_author']['login'])
        final_list.append(ticket_list)

    pretty_list = prettify_lists(final_list)
    print(tabulate(pretty_list, headers=header, tablefmt="simple"))


def get_latest_ticket_id(wrapper) -> int:
    """Get latest ticket id."""
    ticket = wrapper.get_tickets()
    ticket_id = ticket['data'][0]['id']
    return int(ticket_id)


@main.command(name="close")
@click.option("-i", "--id", "task_id", help="ticket id")
def close_ticket(task_id: int = None):
    """Close ticket."""
    wrapper = config.setup_api()
    if task_id is None:
        task_id = get_latest_ticket_id(wrapper)

    close_ticket(task_id)


def print_view_order(views: dict):
    print("viewed by ({}) :".format(len(views)), end=" ")
    for view in views:
        for data in view:
            data_view = data.split(':')
            print("{} ({})".format(data_view[1], data_view[0]), end=' ')
    print(end="\n")


@main.command(name="show")
@click.option("-i", "--id", "task_id", help="ticket id")
def show(task_id: int = None):
    """Show content of ticket."""
    wrapper = config.setup_api()
    if task_id is None:
        task_id = get_latest_ticket_id(wrapper)
    ticket = wrapper.get_ticket(task_id)

    data = ticket['data']
    print("id            : {}".format(data['id']))
    print("title         : {}".format(data['title']))
    print("ttl           : {}".format(data['ttl']))
    print("created at    : {}".format(data['created_at']))
    print("updated at    : {}".format(data['updated_at']))
    print("closed at     : {}".format(data['closed_at']))
    print("creator       : {}".format(data['creator']['login']))
    print("users         : ", end="")
    [print(user['login'], end=" ") for user in data['users']]
    print(end="\n")
    print_view_order(data['views'])

    for message in data['messages']:
        print("========================")
        print("{} | {} :".format(message['created_at'],
                                 message['author']['login']))
        print(message['content'])
