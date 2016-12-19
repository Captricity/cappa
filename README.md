cappa
=====

`cappa` acts as a frontend for various package managers so that you can unify all your configurations into one requirements file.

Installation
------------

`pip install git+https://github.com/Captricity/cappa.git`

Usage
-----

Specify a requirements.json file with the list of requirements you would like to install for each package manager. The configuration is parsed as an ordered dictionary, so you can order the installation process by package manager.

Available package managers
--------------------------

- sys: Use to specify system packages to install. *Only available on Ubuntu*
- pip: Use to specify python packages to install
- npmg: Use to specify npm packages to install globally (`npm -g`)
- npm: Use to specify local npm packages to install
- bower: Use to specify bower packages to install

Example requirements.json file
------------------------------

```json
{
    "sys": {
        "postgresql-client": null,
        "libpq-dev": null
    },
    "pip": {
        "psycopg2": null
    },
    "npmg": {
        "bower": "1.3.12",
        "gulp": null
    },
    "npm": {
        "gulp-if": null
    },
    "bower": {
        "jquery": null
    }
}
```

Example requirements.yaml file
------------------------------
```yaml
sys:
    postgresql-client: null
    libpq-dev: null

pip:
    psycopg2: null

npmg:
    bower: 1.3.12
    gulp: null

npm:
    gulp-if: null

bower:
    jquery: null
```

Development
-----------

Get all the requirements for development through `dev_requirements.txt`:

    pip install -r dev_requirements.txt


Use `bumpversion` when updating the version, so that you won't miss any files:

    bumpversion minor

Also don't forget to update `CHANGELOG.md` with your changes.
