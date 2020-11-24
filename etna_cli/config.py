import click
import configparser
import getpass
import keyring
import os
import sys
from pathlib import Path
from typing import Tuple
from etnawrapper import EtnaWrapper


@click.group(name="config")
def main():
    """Init, edit or delete etna config."""


@main.command()
def init():
    """Init config file."""
    config_path = os.getenv("HOME") + "/" + ".etna.conf"

    if Path(config_path).exists():
        print("config file already exists")
        return

    username = input("ETNA username : ")
    password = getpass.getpass()
    keyring.set_password('ETNA', username, password)

    wrapper = EtnaWrapper(login=username, password=password)
    if not wrapper._cookies:
        print("bad credentials")
        return

    config = configparser.ConfigParser()
    config['credentials'] = {}
    config['credentials']['username'] = username
    config['gitlab'] = {}
    config['gitlab']['url'] = "https://rendu-git.etna-alternance.net"

    if click.confirm("Add Gitlab API token ?", default=True):
        gitlab_token = getpass.getpass("Gitlab API token : ")
    else:
        gitlab_token = ""

    keyring.set_password('gitlab_etna', username, gitlab_token)

    with open(config_path, 'w') as configfile:
        config.write(configfile)


@main.command()
def edit():
    """Edit config file."""
    click.edit(filename=Path(os.getenv("HOME"), ".etna.conf"))


@main.command()
def delete():
    """Delete config file"""
    config_path = os.getenv("HOME") + "/" + ".etna.conf"
    if not Path(config_path).exists():
        print("config file not found")
        return

    config = configparser.ConfigParser()
    config.read(config_path)
    username = config['credentials']['username']
    keyring.delete_password('ETNA', username)
    keyring.delete_password('gitlab_etna', username)
    os.remove(config_path)


def setup_api() -> EtnaWrapper:

    """Setup EtnaWrapper."""
    config_path = os.getenv("HOME") + "/" + ".etna.conf"
    if not Path(config_path).exists():
        print("Please run 'etna config init' to get started")
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(config_path)

    username = config['credentials']['username']
    password = keyring.get_password('ETNA', username)
    creds = EtnaWrapper(login=username, password=password)

    return creds


def get_gitlab_credentials() -> Tuple[str, str]:
    """Get gitlab credentials."""
    config_path = os.getenv("HOME") + "/" + ".etna.conf"
    config = configparser.ConfigParser()
    config.read(config_path)
    gl_url = config['gitlab']['url']
    username = config['credentials']['username']
    gl_token = keyring.get_password('gitlab_etna', username)

    return gl_url, gl_token
