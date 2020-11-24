# etna-cli
[![PyPI version](https://badge.fury.io/py/etna-cli.svg)](https://badge.fury.io/py/etna-cli)
[![Build Status](https://drone.matteyeux.com/api/badges/matteyeux/etna-cli/status.svg)](http://drone.matteyeux.com:8080/matteyeux/etna-cli)
[![Packagist](https://img.shields.io/badge/Docs-etna-blue)](https://etna-cli.matteyeux.com)

Python tool for my school

### Usage

```
Usage: etna.py [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version  print version
  -d, --docs     open docs page
  --help         Show this message and exit.

Commands:
  config        Init, edit or delete etna config.
  conversation  Conversations on intranet.
  declare       Declaration.
  event         Events.
  gitlab        Gitlab.
  project       Projects.
  rank          Rank by promotion.
  student       Student stuff.
  task          Add quests and projects to TaskWarrior.
  ticket        Tickets.
```


### Installation

Make sure to have `taskwarrior` installed to task related stuff

#### Github repository
```bash
$ git clone https://github.com/matteyeux/etna-cli
$ cd etna-cli
$ poetry install
```

#### PyPI
- Installation : `pip3 install etna-cli`
- Update : `pip3 install --upgrade etna-cli`

### Setup

Make sure to have `~/.local/bin` in your `$PATH` (`export PATH=$PATH:~/.local/bin`)

If you run etna-cli for the first time you may run `etna config init` to set credentials and optional Gitlab Token.
```
$ etna config init
ETNA username : demo_t
Password:
Add Gitlab API token ? [Y/n]: Y
Gitlab API token :
```

Password and Gitlab token are not printed to STDOUT.


### Credits
Powered by [etnawrapper](https://github.com/tbobm/etnawrapper)
