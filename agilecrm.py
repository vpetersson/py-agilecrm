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


def create_contact(first_name=None, last_name=None, email=None, tags=None, company=None, custom={}):
    """
    Create a contact. first_name is the only required field.
    Returns the ID if successful, otherwise return None and log the error.
    """

    headers = {
        'content-type': 'application/json',
    }

    tags = tags or []
    payload = {
        'tags': tags,
        'properties': []
    }

    def add_element(element_id, value):
        if element_id in ['first_name', 'last_name', 'company', 'email']:
            payload_type = 'SYSTEM'
        else:
            payload_type = 'CUSTOM'

        payload['properties'].append(
            {
                "type": payload_type,
                "name": element_id,
                "value": value
            },
        )

    if first_name:
        add_element('first_name', first_name)

    if last_name:
        add_element('last_name', last_name)

    if company:
        add_element('company', company)

    if email:
        add_element('email', email)

    for key in custom:
        add_element(key, custom[key])

    contact = requests.post(
        CONTACT_ENDPOINT,
        data=json.dumps(payload),
        headers=headers,
        auth=(EMAIL, APIKEY)
    )

    # We get 200 status instead of the expected 201.
    if contact.status_code in (200, 201):
        result = json.loads(contact.content)
        return result['id']
    else:
        print "Failed to create contact.\nError message:\n%s.\nError code: %i" % (contact.content, contact.status_code)
        return None



def update_contact(uuid=None, first_name=None, last_name=None, email=None, tags=None, company=None, custom={}, score=0):
    """
    Update a contact. email is required.
    Returns the response if successful, otherwise log error and return None.
    """

    headers = {
        'content-type': 'application/json',
    }

    if uuid:
        payload = get_contact_by_uuid(uuid)
    else:
        payload = get_contact_by_email(email)

    if not payload:
        print "Failed to get contact %s" % email
        return None

    def update_element(key, value):
        new_values = set()
        if key == 'email':
            # Email is a special case -- the email key can appear more than once. We'll keep the existing values (deduplicated).
            new_values = {d['value'] for d in payload['properties'] if d['name'] == 'email'}

        new_values.add(value)

        new_properties = [{"type": "SYSTEM" if key in ('first_name', 'last_name', 'company', 'email') else "CUSTOM", "name": key, "value": new_value} for new_value in new_values]

        payload['properties'] = [d for d in payload['properties'] if d['name'] != key] + new_properties

    def update_score(score):
        payload['lead_score'] = score

    tags = tags or []
    if tags:
        payload['tags'] = list(set(payload['tags'] + list(tags)))

    if first_name:
        update_element('first_name', first_name)

    if last_name:
        update_element('last_name', last_name)

    if company:
        update_element('company', company)

    if email:
        update_element('email', email)

    for key in custom:
        update_element(key, custom[key])

    if score:
        update_score(score)

    contact = requests.put(
        CONTACT_ENDPOINT,
        data=json.dumps(payload),
        headers=headers,
        auth=(EMAIL, APIKEY)
    )

    # We get 200 status instead of the expected 201.
    if contact.status_code not in (200, 201):
        print "Failed to update contact.\nError message:\n%s.\nError code: %i" % (contact.content, contact.status_code)
        return None
    return json.loads(contact.content)


def get_contact_by_email(email):
    """
    Returns a user object in JSON format if successful.
    Otherwise return None and log the error.

    From docs:
    $ curl https://{domain}.agilecrm.com/dev/api/contacts/search/email -H "Accept: application/json"
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

    if contact.status_code != 200:
        print "Failed to get contact.\nError message:\n%s.\nError code: %i" % (contact.content, contact.status_code)
        return None
    return json.loads(contact.content)[0]


def get_contact_by_uuid(uuid):
    """
    Returns a user object in JSON format if successful.
    Otherwise return None and log the error.

    From docs:
    $ curl https://{domain}.agilecrm.com/dev/api/contacts/{id} \
        -H "Accept :application/xml" \
        -v -u {email}:{apikey}
    """

    headers = {
        'Accept': 'application/json',
    }

    contact = requests.get(
        '%s/%s' % (CONTACT_ENDPOINT, uuid),
        headers=headers,
        auth=(EMAIL, APIKEY)
    )

    if contact.status_code != 200:
        print "Failed to get contact.\nError message:\n%s.\nError code: %i" % (contact.content, contact.status_code)
        return None
    return json.loads(contact.content)


def add_tag(email, tag):
    """
    Returns True if successful, otherwise return None and log the error.

    From docs:
    $ curl https://{domain}.agilecrm.com/dev/api/contacts/email/tags/add -H "Accept: application/xml"
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
        print "Failed to add tag.\nError message:\n%s.\nError code: %i" % (contact.content, contact.status_code)
        return None


def main():
    pass

if __name__ == '__main__':
    main()
