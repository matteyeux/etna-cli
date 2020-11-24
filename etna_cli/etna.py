#!/usr/bin/env python3

"""Main module for etna-cli."""

import click

from etna_cli import config
from etna_cli import conversation
from etna_cli import declaration
from etna_cli import etna_gitlab
from etna_cli import event
from etna_cli import project
from etna_cli import student
from etna_cli import rank
from etna_cli import task
from etna_cli import ticket

# This string is managed by Drone-CI
# Don't touch it
__version__ = 'replace_me'


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("-v", "--version", is_flag=True, help="print version")
@click.option("-d", "--docs", is_flag=True, help="open docs page")
def main(ctx, version, docs):
    if version:
        print("Etna CLI version %s" % __version__)
        print("~matteyeux")
    elif docs:
        click.launch("https://etna-cli.matteyeux.com")
    elif ctx.invoked_subcommand is None:
        click.echo(main.get_help(ctx))


main.add_command(config.main)
main.add_command(conversation.main)
main.add_command(declaration.main)
main.add_command(event.main)
main.add_command(project.main)
main.add_command(etna_gitlab.main)
main.add_command(student.main)
main.add_command(rank.main)
main.add_command(task.main)
main.add_command(ticket.main)

if __name__ == '__main__':
    main()
