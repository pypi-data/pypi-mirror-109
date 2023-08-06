import os
import re
import imp
import importlib.util
import sys
from .config import Config
from .constants import *
from .logger import Logger
from .exceptions import DSOException

class ProviderBase():
    def __init__(self, id):
        self.__id = id
    @property
    def id(self):
        return self.__id

class StoreProvider(ProviderBase):

    def validate_key(self, key):
        Logger.debug(f"Validating: key={key}")
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

    def load_provider(self, provider_id):
        providerPackage = os.path.join(Config.install_path,'provider',provider_id)
        if not os.path.exists(providerPackage):
            raise DSOException('No provider found for {0}'.format(provider_id))
        imp.load_package('', providerPackage)

    def register(self, provider: ProviderBase):
        if not provider.id in self.__map:
            self.__map[provider.id] = provider
            Logger.debug(f"Provider registered: id ={provider.id}")

    def get_provider(self, provider_id):
        if not provider_id in self.__map:
            self.load_provider(provider_id)

        ### try after lazy load
        if provider_id in self.__map:
            return self.__map[provider_id] 
        else:
            raise DSOException('No provider registered for {0}'.format(provider_id))

    def ParameterProvider(self):
        if not Config.parameter_provider:
            raise DSOException('Parameter provider has not been set.')
        return self.get_provider('parameter/' + Config.parameter_provider)

    def TemplateProvider(self):
        if not Config.parameter_provider:
            raise DSOException('Template provider has not been set.')
        return self.get_provider('template/' + Config.template_provider)

    def SecretProvider(self):
        if not Config.parameter_provider:
            raise DSOException('Secret provider has not been set.')
        return self.get_provider('secret/' + Config.secret_provider)

ProviderManager = ProviderManagerClass()

