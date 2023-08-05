import json
import logging
import random
import sys
import time

from faker import Faker

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
#logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def generate_text_log(seed):
    Factory = Faker()
    Factory.seed(seed)
    logging.info(Factory.sentence(nb_words=15))

def generate_kv_log(seed):
    Factory = Faker()
    Factory.seed(seed)
    profile = Factory.profile()
    # The following fields aren't strings so we will remove them to avoid additional processing.
    del profile['current_location']
    del profile['website']
    logging.info(' '.join(['{0}={1}'.format(k,v) for k,v in profile.items()]))

def generate_json_log(seed):
    def json_default(o):
        # Two of the values returned by Faker.profile fail to serialize into json. They are
        # decimal.Decimal and datetime.date.  They both have a __str__ function that we can use
        # to convert the values to a strings.
        return o.__str__()

    Factory = Faker()
    Factory.seed(seed)
    logging.info(json.dumps(Factory.profile(), default=json_default))
