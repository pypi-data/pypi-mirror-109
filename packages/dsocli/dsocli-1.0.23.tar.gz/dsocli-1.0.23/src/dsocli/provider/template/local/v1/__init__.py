__package__ = 'dsocli.provider.template.local.v1'
from .main import LocalTemplateProvider
from dsocli.providers import ProviderManager
ProviderManager.register(LocalTemplateProvider())
