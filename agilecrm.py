import requests
import json
import settings
from urlparse import urljoin

APIKEY = settings.AGILECRM_APIKEY
EMAIL = settings.AGILECRM_EMAIL
BASEURL = settings.AGILECRM_BASEURL
CONTACT_ENDPOINT = urljoin(BASEURL, '/dev/api/contacts')
CONTACT_SEARCH_ENDPOINT = urljoin(BASEURL, '/dev/api/contacts/search/email')
CONTACT_ADD_TAG_ENDPOINT = urljoin(BASEURL, '/dev/api/contacts/email/tags/add')

"""
Module for dealing with AgileCRMs API.
Documentation is available here:
https://github.com/agilecrm/rest-api
"""


def create_contact(first_name=None, last_name=None, email=None, tags=None, company=None):
    """
    Create a contact. first_name is the only required field.
    Returns True if successful, otherwise the HTTP status code.
    """

    headers = {
        'content-type': 'application/json',
    }

    tags = tags or []
    payload = {
        'tags': tags,
        'properties': []
    }

    if first_name:
        payload['properties'].append(
            {
                "type": "SYSTEM",
                "name": "first_name",
                "value": first_name
            },
        )

    if last_name:
        payload['properties'].append(
            {
                "type": "SYSTEM",
                "name": "last_name",
                "value": last_name
            },
        )

    if company:
        payload['properties'].append(
            {
                "type": "SYSTEM",
                "name": "company",
                "value": company
            }
        )

    if email:
        payload['properties'].append(
            {
                "type": "SYSTEM",
                "name": "email",
                "subtype": "work",
                "value": email
            }
        )

    contact = requests.post(
        CONTACT_ENDPOINT,
        data=json.dumps(payload),
        headers=headers,
        auth=(EMAIL, APIKEY)
    )

    # We get 200 status instead of the expected 201.
    if contact.status_code in (200, 201):
        return True
    else:
        return contact.status_code


def update_contact(first_name=None, last_name=None, email=None, tags=None, company=None):
    """
    Update a contact. email is required.
    Returns True if successful, otherwise the HTTP status code.
    """

    headers = {
        'content-type': 'application/json',
    }

    payload = get_contact_by_email(email)

    if not payload:
        return False

    def index_of_dict_with_name(key):
        """
        Due to the annoying way this API is structured,
        we need to walk over the dicts to find the right
        one to update.
        """
        return next((n for n, d in enumerate(payload[0]['properties']) if d['name'] == key), None)

    tags = tags or []
    if tags:
        for t in tags:
            payload[0]['tags'].append(t)

        # Deduplicate tags (in case we're adding an existing tag)
        deduped_tags = list(set(payload[0]['tags']))
        payload[0]['tags'] = deduped_tags

    if first_name:
        data_location = index_of_dict_with_name('first_name')
        data_set = {
            "type": "SYSTEM",
            "name": "first_name",
            "value": first_name
        }

        # Remove the existing one and add a new one.
        if data_location:
            del payload[0]['properties'][data_location]

        payload[0]['properties'].append(data_set)

    if last_name:
        data_location = index_of_dict_with_name('last_name')
        data_set = {
            "type": "SYSTEM",
            "name": "last_name",
            "value": last_name
        }

        # Remove the existing one and add a new one.
        if data_location:
            del payload[0]['properties'][data_location]

        payload[0]['properties'].append(data_set)

    if company:
        data_location = index_of_dict_with_name('company')
        data_set = {
            "type": "SYSTEM",
            "name": "company",
            "value": company
        }

        # Remove the existing one and add a new one.
        if data_location:
            del payload[0]['properties'][data_location]

        payload[0]['properties'].append(data_set)

    if email:
        data_location = index_of_dict_with_name('email')
        data_set = {
            "type": "SYSTEM",
            "name": "email",
            "subtype": "work",
            "value": email
        }

        # Remove the existing one and add a new one.
        if data_location:
            del payload[0]['properties'][data_location]

        payload[0]['properties'].append(data_set)

    contact = requests.put(
        CONTACT_ENDPOINT,
        data=json.dumps(payload[0]),
        headers=headers,
        auth=(EMAIL, APIKEY)
    )

    # We get 200 status instead of the expected 201.
    if contact.status_code in (200, 201):
        return True
    else:
        return contact.status_code


def get_contact_by_email(email):
    """
    Returns a user object in JSON format if successful.
    Otherwise the HTTP status code is returned.

    From docs:
    curl https://{domain}.agilecrm.com/dev/api/contacts/search/email -H "Accept: application/json"
        -H "Content-Type :application/x-www-form-urlencoded"
        -d 'email_ids=["notifications@basecamp.com"]'
        -v -u {email}:{apikey} -X POST
    """

    payload = "email_ids=[%s]" % email

    headers = {
        'content-type': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    contact = requests.post(
        CONTACT_SEARCH_ENDPOINT,
        data=payload,
        headers=headers,
        auth=(EMAIL, APIKEY)
    )

    if contact.status_code == 200:
        return json.loads(contact.content)
    else:
        return contact.status_code


def add_tag(email, tag):
    """
    Returns True if successful, otherwise the HTTP status code.

    from docs:
    curl https://{domain}.agilecrm.com/dev/api/contacts/email/tags/add -H "Accept: application/xml"
        -H "Content-Type :application/x-www-form-urlencoded"
        -d 'email=notifications@basecamp.com&tags=["testing"]'
        -v -u {email}:{apikey} -X POST
    """

    payload = {
        'email': email,
        'tags': "[%s]" % tag
    }

    headers = {
        'content-type': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    contact = requests.post(
        CONTACT_ADD_TAG_ENDPOINT,
        data=payload,
        headers=headers,
        auth=(EMAIL, APIKEY)
    )

    # We get 200 status instead of the expected 201.
    if contact.status_code in (200, 201):
        return True
    else:
        return contact.status_code


def main():
    pass

if __name__ == '__main__':
    main()
