import os
import re
import imp
import importlib.util
import sys
from .config import Config
from .constants import *
from .logger import Logger

class ProviderBase():
    def __init__(self, id):
        self.__id = id
    @property
    def id(self):
        return self.__id

class StoreProvider(ProviderBase):

    def validate_key(self, key):
        pattern = self.get_key_validator()
        if re.match(pattern, key):
            return True
        else:
            Logger.error(MESSAGES['InvalidKey'].format(key, pattern))
            return False

    def get_key_validator(self, key):
        raise NotImplementedError()


class ProviderManagerClass():
    __map = {}

    # def load_all_providers(self):
    #     __import__(Config.root_path + 'lib/dso/provider')
    #     # importdir.do(os.path.dirname(__file__)+'/secret_providers', globals())
    #     # importdir.do(os.path.dirname(__file__)+'/template_providers', globals())

    def __load_provider(self, provider_id):
        providerPackage = os.path.join(Config.install_path,'provider',provider_id)
        if not os.path.exists(providerPackage):
            raise Exception('No provider found for {0}'.format(provider_id))
        imp.load_package('', providerPackage)

    def register(self, provider: ProviderBase):
        if not provider.id in self.__map:
            self.__map[provider.id] = provider
            Logger.debug("Provider '{0}' registered.".format(provider.id))

    def get_provider(self, provider_id):
        if not provider_id in self.__map:
            self.__load_provider(provider_id)

        ### try after possible load
        if provider_id in self.__map:
            return self.__map[provider_id] 
        else:
            raise Exception('No provider registered for {0}'.format(provider_id))

    def ParameterProvider(self):
        if not Config.parameter_provider:
            raise Exception('Parameter provider has not been set.')
        return self.get_provider('parameter/' + Config.parameter_provider)

    def TemplateProvider(self):
        if not Config.parameter_provider:
            raise Exception('Template provider has not been set.')
        return self.get_provider('template/' + Config.template_provider)

    def SecretProvider(self):
        if not Config.parameter_provider:
            raise Exception('Secret provider has not been set.')
        return self.get_provider('secret/' + Config.secret_provider)

ProviderManager = ProviderManagerClass()

