import copy
import inspect
import importlib

from pathlib import Path

from unv.utils.collections import update_dict_recur
from unv.app.settings import ComponentSettings, validate_schema


class DeploySettings(ComponentSettings):
    KEY = 'deploy'
    SCHEMA = {
        'tasks': {
            'type': 'list',
            'schema': {'type': 'string'}
        },
        'hosts': {
            'type': 'dict',
            'keyschema': {'type': 'string'},
            'valueschema': {
                'type': 'dict',
                'schema': {
                    'public_ip': {'type': 'string', 'required': True},
                    'private_ip': {'type': 'string'},
                    'port': {'type': 'integer'},
                    'provider': {'type': 'string'},
                    'tags': {'type': 'list', 'schema': {'type': 'string'}},
                    'components': {
                        'type': 'list',
                        'schema': {'type': 'string'}
                    }
                }
            }
        },
        'components': {'required': True, 'allow_unknown': True},
        'tags': {'type': 'dict'}
    }
    DEFAULT = {
        'tasks': [],
        'hosts': {},
        'components': {},
        'tags': {}
    }

    def get_hosts(self, component=''):
        for key, value in self._data['hosts'].items():
            if component in value.get('components', []) or not component:
                value.setdefault('private_ip', value['public_ip'])
                value.setdefault('port', 22)
                yield key, value

    def get_components(self, public_ip):
        for value in self._data['hosts'].values():
            if value['public_ip'] == public_ip:
                return value['components']
        return []

    def get_component_user(self, name):
        return self._data.get(name, {}).get('user', name)

    def get_component_settings(self, name):
        return self._data['components'].get(name, {})

    def get_tags_settings(self, name):
        return self._data['tags'].get(name, {})

    @property
    def task_classes(self):
        for module_path in self._data['tasks']:
            module_path, class_path = module_path.split(':')
            yield getattr(importlib.import_module(module_path), class_path)


SETTINGS = DeploySettings()


class DeployComponentSettings:
    NAME = ''
    DEFAULT = {}
    SCHEMA = {}
    SETTINGS = SETTINGS

    def __init__(self, settings=None, root=None):
        cls = self.__class__
        if settings is None:
            settings = cls.SETTINGS.get_component_settings(cls.NAME)
        tags_settings = cls.SETTINGS.get_tags_settings(cls.NAME)
        settings = update_dict_recur(
            copy.deepcopy(cls.DEFAULT), settings)
        settings = update_dict_recur(
            copy.deepcopy(tags_settings), settings)
        settings = validate_schema(cls.SCHEMA, settings)

        self._data = settings
        self.local_root = root or Path(inspect.getfile(cls)).parent

    @property
    def user(self):
        return self._data.get('user', self.__class__.NAME)

    @property
    def enabled(self):
        if 'enabled' in self._data:
            return self._data['enabled']
        for _, host in self.__class__.SETTINGS.get_hosts():
            if self.__class__.NAME in host['components']:
                return True
        return False

    @property
    def home(self):
        return Path('~')

    @property
    def home_abs(self):
        return Path('/', 'home', self.user)

    @property
    def systemd(self):
        return self._data.get('systemd', {})

    @property
    def systemd_config(self):
        # TODO: move to class all systemd stuff
        return self.systemd.get('config', [])

    @property
    def systemd_dir(self):
        return Path('/etc', 'systemd', 'system')

    @property
    def systemd_type(self):
        return self.systemd.get('type', 'simple')

    @property
    def root(self):
        return self.home / self._data['root']

    @property
    def root_abs(self):
        return self.home_abs / self._data['root']
