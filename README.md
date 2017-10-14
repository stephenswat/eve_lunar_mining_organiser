# ELMO

EVE Online's 2017 October expansion Lifeblood brings with it a completely
revamped system of moon mining. Since the moons of New Eden are being completely
reseeded with random resources alliances all over low- and null-sec space will
be surveying their moons once more. The EVE Lunar Mining Organizer (or ELMO) was
designed to facilitate this by providing a collaborative moon mining database
that can either be configured to be public or alliance-private.

## Installation instructions

Create a virtual environment:

    mkvirtualenv --python=python3 elmo

Install the required packages:

    pip install -r requirements.txt

Create and populate the database:

    python manage.py makemigrations
    python manage.py migrate
    python manage.py loaddata eve_sde/fixtures/eve_sde_map.json
    python manage.py create_permissions
    python manage.py create_groups

That should be all!
