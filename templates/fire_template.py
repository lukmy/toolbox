#!/usr/bin/env python
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from toolbox_utils import get_config_section, run_cmd, FireBase


class Config(object):
    config = get_config_section('my_config_section')


config = Config()


class MyFireClass(FireBase):
    _config = config

    def do_fire_func(self):
        pass


if __name__ == '__main__':
    from fire import Fire
    Fire(MyFireClass)
