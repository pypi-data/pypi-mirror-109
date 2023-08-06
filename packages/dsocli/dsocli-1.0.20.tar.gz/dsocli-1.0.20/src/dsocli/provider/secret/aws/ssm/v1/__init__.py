__package__ = 'dsocli.provider.secret.aws.ssm.v1'
from .main import AwsSsmSecretProvider
from dsocli.providers import ProviderManager
ProviderManager.register(AwsSsmSecretProvider())
