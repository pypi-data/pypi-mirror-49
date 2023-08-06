import json

from pconf import Pconf
import os


def read_json_file(json_file):
    # TODO: implementation is ugly, using extendable way
    config_format = os.environ.get('IOFLOW_CFG_FORMAT', 'raw')

    if not os.path.exists(json_file):
        return None

    if config_format == 'raw':
        with open(json_file) as fd:
            return json.load(fd)
    elif config_format == 'ecarx':
        with open(json_file) as fd:
            raw_data = json.load(fd)
            data = raw_data['data']['params']

            # inject task_id
            data['task_id'] = raw_data['data']['_id']
            # set data source scheme
            data['data_source_scheme'] = 'http'

            return data


def read_configure(return_empty=False) -> dict:
    # set return_empty to True for not read config from env
    # which can prevent unexpected result
    # e.g. './configure.json' is not for this app, but for other using
    if return_empty:
        return {}

    active_configure_file = os.getenv('_DEFAULT_CONFIG_FILE', './configure.json')
    builtin_configure_file = os.getenv('_BUILTIN_CONFIG_FILE', './builtin_configure.json')

    # Pconf.env()
    Pconf.file(active_configure_file, encoding='json')
    Pconf.file(builtin_configure_file, encoding='json')

    # Get all the config values parsed from the sources
    config = Pconf.get()

    print(config)

    return config

    # sys.exit(0)

    # return {
    #     'corpus': {
    #         'train': './data/train.conllz',
    #         'test': './data/test.conllz'
    #     },
    #     'model': {
    #         'shuffle_pool_size': 10,
    #         'batch_size': 32,
    #         'epochs': 20,
    #         'arch': {}
    #      }
    # }


read_config = read_configure  # alias
