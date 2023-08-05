# Startin'Blox Manager

## Requirements

You will need both Python3 and Pip3 installed.

Just make sure you got the last version of Pip by upgrading it:
```
pip install --user -U pip
```

Then install the `sib` command line:
```
$ pip3 install --user -U sib-manager
```

## Get started with a development instance

Create a new project with your favorite modules. To create a project with `djangoldp_project` and `oidc_provider` :
```
$ sib startproject myproject -m djangoldp_project -m oidc_provider@django-oidc-provider
$ cd myproject
$ sib initproject
```

And launch it locally !
```
$ python3 manage.py runserver
```

For development instance, the administartion interface is available at `http://localhost/admin/` with default `admin` user and password.

## Usage

```
$ sib --help
Usage: sib [OPTIONS] COMMAND [ARGS]...

  Startin'Blox installer
```

`sib` manager can be used to deploy local development and production instances. Whereas a development instance relies on testing components as a `sqlite` database and comes with default configuration, a production instance needs more parameters to configure the `postgresql` database.

### Available commands

Both `startproject` and `initproject` take an optional path for the project as a second argument to define the project directory.

A production setup can made by the `--production` switch option.

**startproject**

```
$ sib startproject --help
Usage: sib startproject [OPTIONS] NAME [DIRECTORY]

  Start a new startin'blox project
```

This command takes an optional directory giving the folder where the project will be created. The default is the current directory.

* `--module` (or `-m`)

This option gives the startin'blox module with the format `<package>@<distribution>`. The distribution is optional. When specified it can take a distribution name as known on PYPI.org or an URL `git+https://git.somewhere.io/module.git` for private `git` repositories.


* `--site-url`

This option is used to generate links and ids. Defaults to `http://localhost:8000`.


* `--db-host`, `--db-name`, `--db-user` and `--db-pass` are used to configure the database (mandatory with `--production`)

* `--smtp-host`, `--smtp-user` and `--smtp-pass` are used to configure the SMTP (optional)

**initproject**

```
# sib initproject --help
Usage: sib initproject [OPTIONS] [DIRECTORY]

  Initialize a startin'blox project
```

This command takes an optional directory giving the folder where the project resides. The default is the current directory.

* `--admin-name`, `--admin-pass` and `--admin-email` give details about the default admin (default to `admin` in development, mandatory in production)

**startpackage**

```
d# sib startpackage --help
Usage: sib startpackage [OPTIONS] NAME [DIRECTORY]

  Create a new startin'blox package
```

This command takes an optional directory giving the folder where the project resides. The default is the current directory. It will then create the package folder inside the project.

## Contribute

Get the last unreleased version of the project:
```
$ pip3 install --user -U git+https://git.happy-dev.fr/startinblox/devops/sib
```

## Testing in docker

Test production setup with postgres:
```
# docker network create sib
# docker run --rm --network sib --name db -e POSTGRES_PASSWORD=test -d postgres
# docker run --rm --network sib -p 127.0.0.1:80:8000 -v $PWD:/code -it python:3.6 bash
# pip install -e .[dev]
# sib startproject --production --db-host db --db-name postgres --db-user postgres --db-pass test -m djangoldp_project -m oidc_provider:django-oidc-provider myproject /tmp/test-sib-docker
# sib initproject --production --admin-name admin --admin-email 'something' --admin-pass admin myproject /tmp/test-sib-docker
# cd /tmp/test-sib-docker/
# python manage.py runserver 0.0.0.0:8000
```
