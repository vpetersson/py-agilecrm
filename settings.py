# AgileCRM
AGILECRM_EMAIL = 'user@example.com'
AGILECRM_APIKEY = ''
AGILECRM_BASEURL = 'https://somedomain.agilecrm.com'

# Bring in local overrides
try:
    from site_settings import *
except:
    pass
