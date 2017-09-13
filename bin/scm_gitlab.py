#!/usr/bin/env python
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from toolbox_utils import get_config_section, run_cmd, FireBase


class Config(object):
    config = get_config_section('gitlab', required=True)

    mr_default_target_branch = config.get('default_target_branch', 'develop')
    mr_contained_fields = config['mr_contained_fields']
    mr_open_url_using = config.get('open_url_using', 'open')


config = Config()


class Gitlab(FireBase):
    _config = config

    def new_merge_request(self):
        default_target_branch = config.mr_default_target_branch
        default_source_branch = run_cmd(
            'git branch | grep "*" | sed "s/\* //g"', read_output=True)

        source_branch = raw_input('Please input source branch({0}): '.format(
            default_source_branch)) or default_source_branch
        target_branch = raw_input('Please input target branch({0}): '.format(
            default_target_branch)) or default_target_branch

        self._new_merge_request(source_branch, target_branch)

    def _new_merge_request(self,
                           source_branch,
                           target_branch,
                           open_with_browser=True):
        arguments = config.config
        arguments['source_branch'] = source_branch
        arguments['target_branch'] = target_branch

        url1 = '{url}/{source_project_name}/merge_requests/new?'.format(
            **arguments)
        url2 = '&'.join([
            'merge_request[{0}]={1}'.format(k, arguments[k])
            for k in config.mr_contained_fields
        ])

        command = 'echo "{0}/{1}"'.format(url1, url2)
        if open_with_browser:
            command += '| xargs {0}'.format(config.mr_open_url_using)

        run_cmd(command)


if __name__ == '__main__':
    from fire import Fire
    Fire(Gitlab)
