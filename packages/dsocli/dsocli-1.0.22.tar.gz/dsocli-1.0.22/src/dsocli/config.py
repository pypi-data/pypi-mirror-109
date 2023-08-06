
import yaml
import os
from .constants import *
from .logger import Logger
from .utils import *
from .version import __version__
from pathlib import Path
from .exceptions import DSOException

default_config = {
    'version': int(__version__.split('.')[0]),
    'logs': {
        'colorize': True,
        'timestamp': False
    }
}

class ConfigManager:
    @property
    def config_dir(self):
        return '.dso'

    @property
    def config_file(self):
        return 'dso.yml'

    @property
    def install_path(self):
        return os.path.dirname(os.path.abspath(__file__))
    
    working_dir = ''
    config_files = []
    inherited_config = {}
    local_config = {}
    overriden_config = {}
    merged_config = {}

    # def __init__(self):
    #     # path = os.path.join(os.path.expanduser("~"), self.config_dir, self.config_file)
    #     # if os.path.exists(path):
    #     #     self.__config = yaml.safe_load(open(path))

    def load(self, working_dir, config_overrides):
        self.working_dir = working_dir
        localConfigDirPath = os.path.join(self.working_dir, self.config_dir)

        for dir in Path(localConfigDirPath).resolve().parents:
            configFilePath = os.path.join(dir, self.config_dir, self.config_file)
            if os.path.exists(configFilePath):
                self.config_files.append(configFilePath)

        localConfigFilePath = os.path.join(localConfigDirPath, self.config_file)
        if not os.path.exists(localConfigFilePath):
            Logger.warn(MESSAGES['DSOConfigFileNotFound'].format(localConfigDirPath))

        for configFile in reversed(self.config_files):
            try:
                config = yaml.load(open(configFile, 'r', encoding='utf-8'), yaml.SafeLoader)
            except:
                raise DSOException(MESSAGES['InvalidDSOConfigurationFile'])
            if os.path.exists(localConfigFilePath) and os.path.samefile(configFile, localConfigFilePath):
                self.local_config = config
            else:
                self.inherited_config = merge_dicts(config, self.inherited_config)

        ### construct overrides if any
        if config_overrides:
            try:
                configs = config_overrides.split(',')
                for config in configs:
                    key = config.split('=')[0].strip()
                    value = config.split('=')[1].strip()
                    set_dict_value(self.overriden_config, key.split('.'), value)
            except:
                raise DSOException(MESSAGES['InvalidConfigOverrides'])

        self.update_merged_config()
        self.check_version()

    def check_version(self):
        if not self.merged_config['version'] == default_config['version']:
            if  self.merged_config['version'] > default_config['version']:
                Logger.warn(MESSAGES['DSOConfigNewer'].format(default_config['version'], self.merged_config['version']))
            else:
                Logger.warn(MESSAGES['DSOConfigOlder'].format(default_config['version'], self.merged_config['version']))        

    def update_merged_config(self):
        self.merged_config = default_config
        self.merged_config = merge_dicts(self.inherited_config, self.merged_config)
        self.merged_config = merge_dicts(self.local_config, self.merged_config)
        self.merged_config = merge_dicts(self.overriden_config, self.merged_config)


    def flush_local_config(self):
        dir = os.path.join(self.working_dir, self.config_dir)
        os.makedirs(dir, exist_ok=True)
        with open(os.path.join(dir, self.config_file), 'w') as outfile:
            yaml.dump(self.local_config, outfile, default_flow_style=False)

    @property
    def application(self):
        if 'application' in self.merged_config:
            result = self.merged_config['application'] or 'default'
        else:
            result  = os.getenv('DSO_APPLICATION') or 'default'
        if self.project == 'default':
            if not result == 'default':
                Logger.warn("Application specific scope for application '{0}' was ignored because the global project scope was used.".format(result))
                result = 'default'
        return result.lower()

    @property
    def project(self):
        if 'project' in self.merged_config:
            result = self.merged_config['project'] or 'default'
        else:
            result  = os.getenv('DSO_PROJECT') or 'default'
        return result.lower()

    @property
    def parameter_provider(self):
        if not ('parameter' in self.merged_config and 
                'provider' in self.merged_config['parameter'] and 
                'id' in self.merged_config['parameter']['provider']):
            raise DSOException(MESSAGES['ProviderNotSet'].format('Parameter'))

        return self.merged_config['parameter']['provider']['id']

    @property
    def secret_provider(self):
        if not ('secret' in self.merged_config and 
                'provider' in self.merged_config['secret'] and 
                'id' in self.merged_config['secret']['provider']):
            raise DSOException(MESSAGES['ProviderNotSet'].format('secret'))

        return self.merged_config['secret']['provider']['id']

    @property
    def template_provider(self):
        if not ('template' in self.merged_config and 
                'provider' in self.merged_config['template'] and 
                'id' in self.merged_config['template']['provider']):
            raise DSOException(MESSAGES['ProviderNotSet'].format('template'))

        return self.merged_config['template']['provider']['id']

    def parameter_spec(self, key=None):
        if not key:
            return self.merged_config['parameter']['provider']['spec']
        if key in self.merged_config['parameter']['provider']['spec']:
            return self.merged_config['parameter']['provider']['spec'][key]
        return None

    def secret_spec(self, key=None):
        if not ('secret' in self.merged_config and 
                'provider' in self.merged_config['secret'] and 
                'spec' in self.merged_config['secret']['provider']):
            raise DSOException(MESSAGES['ProviderSpecSet'].format('secret'))

        if not key:
            return self.merged_config['secret']['provider']['spec']
        if key in self.merged_config['secret']['provider']['spec']:
            return self.merged_config['secret']['provider']['spec'][key]
        return None

    def template_spec(self, key):
        if not ('template' in self.merged_config and 
                'provider' in self.merged_config['template'] and 
                'spec' in self.merged_config['template']['provider']):
            raise DSOException(MESSAGES['ProviderSpecSet'].format('template'))

        if not key:
            return self.merged_config['template']['provider']['spec']
        if key in self.merged_config['template']['provider']['spec']:
            return self.merged_config['template']['provider']['spec'][key]
        return None

    def get_template_render_path(self, key=None):
        if not ('template' in self.local_config and 
                'render' in self.local_config['template']):
            return {}
        result = self.local_config['template']['render'] or {}
        if not key:
            return result
        return {x:result[x] for x in result if x==key}

    def register_template_custom_render_path(self, key, render_path):
        if not 'template' in self.local_config:
            self.local_config['template'] = {}
        if not 'render' in self.local_config['template'] or self.local_config['template']['render'] == None:
            self.local_config['template']['render'] = {}
        # if os.path.isabs(render_path):
        #     raise DSOException(MESSAGES['AbsTemplateRenderPath'].format(render_path))
        if os.path.isdir(render_path):
            raise DSOException(MESSAGES['InvalidRenderPathExistingDir'].format(render_path))
        self.local_config['template']['render'][key] = render_path
        self.flush_local_config()

    def unregister_template_custom_render_path(self, key):
        if not 'template' in self.local_config:
            self.local_config['template'] = {}
        if not 'render' in self.local_config['template'] or self.local_config['template']['render'] == None:
            self.local_config['template']['render'] = {}
            return
        if key in self.local_config['template']['render']:
            self.local_config['template']['render'].pop(key)
            self.flush_local_config()

    def get(self, key=None, uninherited=False):
        if key:
            Logger.info("Getting '{0}' from DSO configurations...".format(key))
        else:
            Logger.info("Getting DSO configurations...")

        usedConfig = merge_dicts(self.overriden_config, self.local_config) if uninherited else self.merged_config

        if key:
            result = get_dict_item(usedConfig, key.split('.'))
            if not result:
                raise DSOException("'{0}' has not been set.".format(key))
            return result
        else:
            return usedConfig

    def set(self, key, value):
        Logger.info("Setting '{0}' to '{1}' in the local DSO configurations...".format(key, value))        
        set_dict_value(self.local_config, key.split('.'), value, overwrite_parent=True,  overwrite_children=True)
        self.flush_local_config()
        self.update_merged_config()

    def delete(self, key):
        Logger.info("Deleting '{0}' from the local DSO configurations...".format(key))
        parent = get_dict_item(self.local_config, key.split('.')[:-1])
        if parent and key.split('.')[-1] in parent:
            parent.pop(key.split('.')[-1])
            self.flush_local_config()
            self.update_merged_config()
        else:
            raise DSOException("'{0}' not found in the local DSO configuratoins.".format(key))

Config = ConfigManager()

