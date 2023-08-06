__package__ = 'dsocli.provider.parameter.aws.ssm.v1'
from .main import AwsSsmParameterProvider
from dsocli.providers import ProviderManager
ProviderManager.register(AwsSsmParameterProvider())
