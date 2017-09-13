import yaml
import os
from subprocess import PIPE, Popen


def run_cmd(cmd, read_output=False):
    options = {'shell': True}

    if read_output:
        options['stdout'] = PIPE

    output = Popen(cmd, **options).communicate()[0]
    try:
        return output.strip()
    except:
        return output


def load_yaml(filename):
    f = open(filename, 'r')
    return yaml.load(f) or {}


CONFIG_FILE_NAME = '.toolbox.yml'


def get_config():
    while True:
        cwd = os.path.abspath(os.curdir)
        if cwd == '/':
            raise ValueError(
                'config not found, '
                'please create {0} on project root'.format(CONFIG_FILE_NAME))

        config_file = os.path.join(cwd, CONFIG_FILE_NAME)
        if os.path.isfile(config_file):
            return load_yaml(config_file)

        os.chdir('..')


def get_config_section(name, required=True):
    retval = get_config().get(name, {})
    if not retval and required:
        raise ValueError('section `{0}` is required'.format(name))

    return retval


class FireBase(object):
    def list_config(self):
        def json_dumps(d):
            import json
            return json.dumps(d, indent=2)

        def exclude_key(k):
            return k.startswith('__') or k == 'config'

        c = {
            k: v
            for k, v in self._config.__class__.__dict__.items()
            if not exclude_key(k)
        }
        print('Final config:\n\n'
              '{0}'
              '\n\n'
              'Specified config:\n\n'
              '{1}'.format(json_dumps(c), json_dumps(self._config.config)))
