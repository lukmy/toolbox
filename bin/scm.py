#!/usr/bin/env python
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from toolbox_utils import get_config_section, run_cmd, FireBase


class Config(object):
    config = get_config_section('scm')

    service = config.get('service')


def get_fire_class():

    config = Config()

    if config.service is None:
        raise ValueError('Please config config service type')

    if config.service == 'gitlab':
        from scm_gitlab import Gitlab
        return Gitlab
    else:
        raise NotImplementedError(
            'service type {0} not supported for now'.format(config.service))


if __name__ == '__main__':
    from fire import Fire
    MyFireClass = get_fire_class()
    Fire(MyFireClass)
