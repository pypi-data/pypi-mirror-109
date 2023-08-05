from .logger import Logger
from .config import Config
from .providers import StoreProvider, ProviderManager

class SecretProvider(StoreProvider):
    def list(self, context, uninherited, format, decrypt):
        raise NotImplementedError()
    def add(self, context, key, value):
        raise NotImplementedError()
    def delete(self, context, key):
        raise NotImplementedError()
    def get(self, context, key):
        raise NotImplementedError()

class Secrets():
    @staticmethod
    def list(context, uninherited, decrypt):
        provider = ProviderManager.SecretProvider()
        Logger.debug("Secret provider '{0}' used.".format(provider.id))
        if uninherited:
            Logger.info(f"Start listing overridden SSM secrets: project={Config.project}, application={Config.application}, context={context}")
        else:
            Logger.info(f"Start listing SSM secrets: project={Config.project}, application={Config.application}, context={context}")
        return provider.list(context, uninherited, decrypt)

    @staticmethod
    def add(context, key, value):
        provider = ProviderManager.SecretProvider()
        Logger.debug("Secret provider '{0}' used.".format(provider.id))
        Logger.info(f"Start adding secrets: project={Config.project}, application={Config.application}, context={context}, key={key}")
        return provider.add(context, key, value)

    @staticmethod
    def get(context, key):
        provider = ProviderManager.SecretProvider()
        Logger.debug("Secret provider '{0}' used.".format(provider.id))
        Logger.info(f"Start getting secret: project={Config.project}, application={Config.application}, context={context}, key={key}")
        return provider.get(context, key)

    @staticmethod
    def delete(context, key):
        provider = ProviderManager.SecretProvider()
        Logger.debug("Secret provider '{0}' used.".format(provider.id))
        Logger.info(f"Start deleting secret: project={Config.project}, application={Config.application}, context={context}, key={key}")
        return provider.delete(context, key)

    @staticmethod
    def validate_key(key):
        provider = ProviderManager.SecretProvider()
        Logger.debug("Secret provider '{0}' used.".format(provider.id))
        Logger.info("Start validating secret key...")
        return provider.validate_key(key)
