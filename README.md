# Agile CRM Python library
Python library for [Agile CRM](https://www.agilecrm.com/) based on the [rest-api documentation](https://github.com/agilecrm/rest-api).

## Status
The is something I hacked together one night. This library should be considered work-in-progress, so use with care.

## Installation
Clone the repo as a sub-module inside your project.

Install the Python requirements.

    $ pip install -r /path/to/module/requirements.txt

## Configuration
This script depends on the variables provided in `settings.py`. These can be overridden in `site_settings.py`.

## Usage
First, you need to import the module. This may vary depending on your paths etc, but something like:

    import agilecrm

### Creating a user
Simply create a new user. Despite what is claimed in the documentation, all variables appear to be optional.

    agilecrm.create_contact(
        first_name='John',
        last_name='Doe',
        email='john@doe.com',
        tags=['signed_up'],
        company='Foobar Inc')

### Update a contact
Update a user object.

    agilecrm.update_contact(
        first_name='Steve',
        last_name='Smith',
        email='john@doe.com',
        tags=['name_updated'],
        company='Foobar2 Inc')


## Get a user (by email)
This will get the user by email and return the user object as JSON.

    agilecrm.get_contact_by_email('john@doe.com')

## Get a user (by UUID)
This will get the user by UUID and return the user object as JSON.

    agilecrm.get_contact_by_uuid(1234)

## Add a tag
This will add the tag 'awesome_user' to the user 'john@doe.com'. Both variables are required.

    agilecrm.add_tag('john@doe.com', 'awesome_user')
