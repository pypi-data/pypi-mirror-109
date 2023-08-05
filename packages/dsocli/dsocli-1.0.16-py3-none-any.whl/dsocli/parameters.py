from .logger import Logger
from .config import Config
from .providers import StoreProvider, ProviderManager

class ParameterProvider(StoreProvider):
    def list(self, context, uninherited, format):
        raise NotImplementedError()
    def add(self, context, key, value):
        raise NotImplementedError()
    def delete(self, context, key):
        raise NotImplementedError()
    def get(self, context, key):
        raise NotImplementedError()

class Parameters():
    @staticmethod
    def list(context, uninherited):
        provider = ProviderManager.ParameterProvider()
        Logger.debug("Parameter provider '{0}' used.".format(provider.id))
        if uninherited:
            Logger.info(f"Start listing uninherited SSM parameters: project={Config.project}, application={Config.application}, context={context}")
        else:
            Logger.info(f"Start listing SSM parameters: project={Config.project}, application={Config.application}, context={context}")
        return provider.list(context, uninherited)

    @staticmethod
    def add(context, key, value):
        provider = ProviderManager.ParameterProvider()
        Logger.debug("Parameter provider '{0}' used.".format(provider.id))
        Logger.info(f"Start adding parameter: project={Config.project}, application={Config.application}, context={context}, key={key}, value={value}")
        return provider.add(context, key, value)

    @staticmethod
    def get(context, key):
        provider = ProviderManager.ParameterProvider()
        Logger.debug("Parameter provider '{0}' used.".format(provider.id))
        Logger.info(f"Start getting parameter: project={Config.project}, application={Config.application}, context={context}, key={key}")
        return provider.get(context, key)

    @staticmethod
    def delete(context, key):
        provider = ProviderManager.ParameterProvider()
        Logger.debug("Parameter provider '{0}' used.".format(provider.id))
        Logger.info(f"Start deleting parameter: project={Config.project}, application={Config.application}, context={context}, key={key}")
        return provider.delete(context, key)

    @staticmethod
    def validate_key(key):
        provider = ProviderManager.ParameterProvider()
        Logger.debug("Parameter provider '{0}' used.".format(provider.id))
        Logger.info("Start validating parameter key...")
        return provider.validate_key(key)

