import os
import re
import yaml
import json
import pathlib
import jinja2
from dsocli.logger import Logger
from dsocli.config import Config
from dsocli.templates import Templates, TemplateProvider
from dsocli.contexts import Contexts
from dsocli.constants import *
from dsocli.exceptions import DSOException


config = {
    'templates_dir' : '{0}/templates'.format(Config.config_dir),
}


class LocalTemplateProvider(TemplateProvider):
    def __init__(self):
        super().__init__('template/local/v1')

###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

    @property
    def __templates_root_path(self):
        return f"{Config.working_dir}/{config['templates_dir']}"

###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

    def get_key_validator(self):
        return r"^[a-zA-Z0-9_-]+(/[a-zA-Z0-9_-]+)*(.[a-zA-Z0-9_-]+)?$"

###--------------------------------------------------------------------------------------------

    def add(self, key, content, render_path):
        path = f"{self.__templates_root_path}/{key}"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

###--------------------------------------------------------------------------------------------

    def list(self):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.__templates_root_path, encoding='utf-8'))
        templatesKeys = env.list_templates()
        renderPaths = Config.get_template_render_path()
        result = []
        renderBasePath = Templates.default_render_path
        for key in templatesKeys:
            if key in renderPaths:
                renderPath = renderPaths[key]
                if not (renderPath == '.' or renderPath.startswith(f'.{os.sep}')):
                    renderPath = os.path.join('./', renderPath)
            else:
                renderPath = os.path.join(renderBasePath, key)
            result.append({'Key': key, 'Render': renderPath})

        return result

###--------------------------------------------------------------------------------------------

    def get(self, key):
        path = f"{self.__templates_root_path}/{key}"
        if not os.path.exists(path):
            raise DSOException(MESSAGES['TemplateNotFound'].format(key))
        with open(path, 'r', encoding='utf-8') as f:
            result = f.read()
        return result

###--------------------------------------------------------------------------------------------

    def delete(self, key):
        path = f"{self.__templates_root_path}/{key}"
        if not os.path.exists(path):
            raise DSOException(MESSAGES['TemplateNotFound'].format(key))
        os.remove(path)


