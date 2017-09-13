#!/usr/bin/env python
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from toolbox_utils import get_config, run_cmd, FireBase


class Config(object):
    config = get_config().get('git', {})

    feature_prefix = config.get('feature_branch_prefix', 'feature/')
    feature_base = config.get('feature_branch_base', 'develop')

    publish_default_remote = config.get('publish_default_remote', 'origin')


config = Config()


class Git(FireBase):
    _config = config

    def feature_start(self, name, base=None):
        run_cmd('git checkout -b {0}{1} {2}'.format(
            config.feature_prefix, name, base or config.feature_base))

    def feature_publish(self, remote=None, force=False):
        run_cmd('git push {0} -u {1} HEAD'.format(
            remote or config.publish_default_remote, '-f' if force else ''))


if __name__ == '__main__':
    from fire import Fire
    Fire(Git)
