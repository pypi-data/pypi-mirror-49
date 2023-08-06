from .MESSENGERdata import MESSENGERdata, merc_year
from .databasebackups import databasebackups
from .database_setup import messenger_database_setup


name = 'MESSENGERuvvs'
__author__ = 'Matthew Burger'
__email__ = 'mburger@stsci.edu'
__version__ = '1.1.3'


try:
    messenger_database_setup()
except:
    print('Database setup failed')
