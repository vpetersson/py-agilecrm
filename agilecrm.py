import requests
import json
import settings
from urlparse import urljoin

APIKEY = settings.AGILECRM_APIKEY
EMAIL = settings.AGILECRM_EMAIL
BASEURL = settings.AGILECRM_BASEURL


"""
Module for dealing with AgileCRMs API.
Documentation is available here:
https://github.com/agilecrm/rest-api
"""


def create_contact(first_name='', last_name='', email='', tags=[], company=''):
    """
    Create a contact. first_name is the only required field.
    Returns True if successful, or the HTTP status code if it fails.
    """

    endpoint = '/dev/api/contacts'
    url = urljoin(BASEURL, endpoint)

    headers = {
        'content-type': 'application/json',
    }

    payload = {
        'tags': [],
        'properties': []
    }

    if type(tags) is list:
        payload['tags'] = tags

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
        url,
        data=json.dumps(payload),
        headers=headers,
        auth=(EMAIL, APIKEY)
    )

    # We get 200 status instead of the expected 201.
    if contact.status_code == (200 or 201):
        return True
    else:
        return contact.status_code


def update_contact(first_name='', last_name='', email='', tags=[], company=''):

    """
    Update a contact. id is required.
    Returns True if successful, or the HTTP status code if it fails.
    """

    endpoint = '/dev/api/contacts'
    url = urljoin(BASEURL, endpoint)

    headers = {
        'content-type': 'application/json',
    }

    payload = get_contact_by_email(email)

    def find_dict(key):
        """
        Due to the annoying way this API is structured,
        we need to walk over the dicts to find the right
        one to update.
        """

        i = 0
        dict = payload[0]['properties']
        while i < len(payload[0]['properties']):
            if key in dict[i].values():
                return i
            i += 1
        return False

    if tags:
        for t in tags:
            payload['tags'].append(t)

    if first_name:
        data_location = find_dict('first_name')
        data_set = {
            "type": "SYSTEM",
            "name": "first_name",
            "value": first_name
        }

        if type(data_location) is int:
            payload[0]['properties'][data_location] = data_set
        else:
            payload[0]['properties'].append(data_set)

    if last_name:
        data_location = find_dict('last_name')
        data_set = {
            "type": "SYSTEM",
            "name": "last_name",
            "value": last_name
        }

        if type(data_location) is int:
            payload[0]['properties'][data_location] = data_set
        else:
            payload[0]['properties'].append(data_set)

    if company:
        data_location = find_dict('company')
        data_set = {
            "type": "SYSTEM",
            "name": "company",
            "value": company
        }

        if type(data_location) is int:
            payload[0]['properties'][data_location] = data_set
        else:
            payload[0]['properties'].append(data_set)

    if email:
        data_location = find_dict('email')
        data_set = {
            "type": "SYSTEM",
            "name": "email",
            "subtype": "work",
            "value": email
        }

        if type(data_location) is int:
            payload[0]['properties'][data_location] = data_set
        else:
            payload[0]['properties'].update(data_set)

        if type(data_location) is int:
            payload[0]['properties'][data_location] = data_set
        else:
            payload[0]['properties'].update(data_set)

    contact = requests.put(
        url,
        data=json.dumps(payload[0]),
        headers=headers,
        auth=(EMAIL, APIKEY)
    )

    # We get 200 status instead of the expected 201.
    if contact.status_code == (200 or 201):
        return True
    else:
        return contact.status_code


def get_contact_by_email(email):
    """
    Get a contacty by email.

    Returns the contact in JSON format if successful,
    or the HTTP status code if it fails.

    From docs:
    curl https://{domain}.agilecrm.com/dev/api/contacts/search/email -H "Accept: application/json"
        -H "Content-Type :application/x-www-form-urlencoded"
        -d 'email_ids=["notifications@basecamp.com"]'
        -v -u {email}:{apikey} -X POST
    """

    endpoint = '/dev/api/contacts/search/email'
    url = urljoin(BASEURL, endpoint)
    payload = "email_ids=[%s]" % email
    headers = {
        'content-type': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }
    contact = requests.post(url, data=payload, headers=headers, auth=(EMAIL, APIKEY))

    if contact.status_code == 200:
        return json.loads(contact.content)
    else:
        return contact.status_code


def add_tag(email, tag):
    """
    Add a tag to a user.

    Returns True if succcessful, or the HTTP status code if it fails.


    From docs:
    curl https://{domain}.agilecrm.com/dev/api/contacts/email/tags/add -H "Accept: application/xml"
        -H "Content-Type :application/x-www-form-urlencoded"
        -d 'email=notifications@basecamp.com&tags=["testing"]'
        -v -u {email}:{apikey} -X POST
    """

    endpoint = '/dev/api/contacts/email/tags/add'
    url = urljoin(BASEURL, endpoint)
    payload = "email=%s&tags=[%s]" % (email, tag)
    headers = {
        'content-type': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    contact = requests.post(url, data=payload, headers=headers, auth=(EMAIL, APIKEY))

    # We get 200 status instead of the expected 201.
    if contact.status_code == (200 or 201):
        return True
    else:
        return contact.status_code


def main():
    pass

if __name__ == '__main__':
    main()
