
import os
import re
import jinja2
from jinja2 import meta
from shutil import rmtree
from pathlib import Path
from .constants import *
from .config import Config
from .providers import StoreProvider, ProviderManager
from .parameters import Parameters
from .secrets import Secrets
from .logger import Logger
from .utils import clean_directory, merge_dicts
from .exceptions import DSOException

class TemplateProvider(StoreProvider):
    def list(self):
        raise NotImplementedError()

    def add(self, key, content, render_path):
        raise NotImplementedError()

    def delete(self, key):
        raise NotImplementedError()

    def get(self, key):
        raise NotImplementedError()

class TemplatesClass():

    @property
    def default_render_path(self):
        return Config.working_dir

    def list(self):
        provider = ProviderManager.TemplateProvider()
        Logger.debug("Template provider '{0}' used.".format(provider.id))
        Logger.info("Listing templates...")
        return provider.list()

    def add(self, key, content, render_path):
        provider = ProviderManager.TemplateProvider()
        Logger.debug("Template provider '{0}' used.".format(provider.id))
        Logger.info("Start adding template...")
        if render_path:
            # if '..' in render_path:
            #     raise DSOException(MESSAGES['InvalidRenderPath'].format(render_path))
            if '**' in render_path:
                render_path = render_path.replace('**', os.path.dirname(key))
            if '*' in render_path:
                render_path = render_path.replace('*', os.path.basename(key))
            if not re.match('^[A-Za-z0-9._/$-]+$', render_path):
                raise DSOException(MESSAGES['InvalidRenderPath'].format(render_path))
            if render_path == '.' or render_path == './':
                render_path = os.path.join(self.default_render_path, key)
            if os.path.isdir(render_path):
                raise DSOException(MESSAGES['InvalidRenderPathExistingDir'].format(render_path))
            if os.path.isabs(render_path):
                Logger.warn(f"Render path {render_path} is not releative to the application root.")
        try:
            result = provider.add(key, content, render_path)
        finally:
            Logger.debug(f"Template render path={render_path}")
            if render_path == os.path.join(self.default_render_path, key):
                Config.unregister_template_custom_render_path(key)
            else:
                Config.register_template_custom_render_path(key, render_path)
        return result

    def get(self, key):
        provider = ProviderManager.TemplateProvider()
        Logger.debug("Template provider '{0}' used.".format(provider.id))
        Logger.info("Start getting template...")
        return provider.get(key)

    def delete(self, key):
        provider = ProviderManager.TemplateProvider()
        Logger.debug("Template provider '{0}' used.".format(provider.id))
        Logger.info("Start deleting template...")
        try:
            result = provider.delete(key)
        finally:
            Config.unregister_template_custom_render_path(key)
        return result

    def validate_key(self, key):
        provider = ProviderManager.TemplateProvider()
        Logger.debug("Template provider '{0}' used.".format(provider.id))
        Logger.info("Start validating template key...")
        return provider.validate_key(key)


    def render(self, context, limit=''):
        Logger.info("Start rendering templates....")
        
        Logger.info(MESSAGES['LoadingParameters'])
        params = Parameters.list(context, uninherited=False)
        
        Logger.info(MESSAGES['LoadingSecrets'])
        secrets = Secrets.list(context, uninherited=False, decrypt=True)

        Logger.info(MESSAGES['MerginParameters'])
        merge_dicts(secrets, params)
        
        provider = ProviderManager.TemplateProvider()
        Logger.debug("Template provider '{0}' used.".format(provider.id))
        Logger.info(MESSAGES['LoadingTemplates'])
        templates = provider.list()
        renderPaths = Config.get_template_render_path()

        jinja_env = jinja2.Environment(undefined=jinja2.StrictUndefined)

        Logger.info(MESSAGES['RenderingTemplates'])
        rendered = []
        for item in templates:
            key = item['Key']

            if not key.startswith(limit): continue
            Logger.debug(MESSAGES['RenderingTemplate'].format(key))

            template = ProviderManager.TemplateProvider().get(key)
            try:
                template = jinja_env.from_string(template)
            except:
                Logger.error(f"Failed to load template: {key}")
                raise
            # undeclaredParams = jinja2.meta.find_undeclared_variables(env.parse(template))
            # if len(undeclaredParams) > 0:
            #     Logger.warn(f"Undecalared parameter(s) found:\n{set(undeclaredParams)}")
            try:
                renderedContent = template.render(params)
            except:
                Logger.error(f"Failed to render template: {key}")
                Logger.info("No context was given for rendering, haven't you forgot specify one?")
                raise

            if key in renderPaths:
                renderPath = renderPaths[key]
            else:
                renderPath = os.path.join(self.default_render_path, key)

            if not (renderPath == '.' or renderPath.startswith(f'.{os.sep}')):
                renderPath = os.path.join('./', renderPath)

            # outputFilePath = os.path.join(renderPath, key)
            # outputFilePath = os.path.join(renderPath, key)
            if os.path.dirname(renderPath):
                os.makedirs(os.path.dirname(renderPath), exist_ok=True)
            with open(renderPath, 'w', encoding='utf-8') as f:
                f.write(renderedContent)
            
            rendered.append(renderPath)

        return rendered


Templates = TemplatesClass()