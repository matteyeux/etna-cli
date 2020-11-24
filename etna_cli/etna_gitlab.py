import click
import gitlab
from etna_cli import config


@click.group(name="gitlab")
def main():
    """Gitlab."""


def init_gitlab():
    """Init Gitlab and return gl."""
    gl_url, gl_token = config.get_gitlab_credentials()
    gl = gitlab.Gitlab(gl_url, private_token=gl_token)
    return gl


@main.command()
@click.option("-l", "--list", "list_", is_flag=True, help="list projects")
def projects(list_: bool = False):
    """Projects related stuff."""
    gl = init_gitlab()

    if list_:
        projects = gl.projects.list()
        for project in projects:
            print("==============================")
            print("repo : {}".format(project.name_with_namespace))
            print("URL  : {}".format(project.web_url))
            print("name : {}".format(project.namespace['name']))


@main.command()
@click.option("-c", "--create", help="create snippet, specify a file")
@click.option("-d", "--delete", help="delete snippet by ID")
@click.option("-l", "--list", "list_", is_flag=True, help="list snippets")
def snippets(create: str = None, delete: int = None, list_: bool = False):
    """Create and list snippets."""
    gl = init_gitlab()
    if create:
        print(create)
        snippet_data = {}
        snippet_data['title'] = create
        snippet_data['file_name'] = create
        snippet_data['content'] = open(create).read()
        gl.snippets.create(snippet_data)

    elif list_:
        snippets = gl.snippets.list()

        for snip in snippets:
            print("==============================")
            print("id : {}".format(snip.id))
            print("title : {}".format(snip.title))
            print("description : {}".format(snip.description))
            print("visibility : {}".format(snip.visibility))
            print("author: {}".format(snip.author['username']))
    elif delete:
        gl.snippets.delete(delete)
