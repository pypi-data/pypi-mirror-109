
import re
from .config import Config
from .providers import ProviderManager
from .constants import *
from .exceptions import DSOException

class Contexts():
    # @staticmethod
    # def list(context):
    #     pass
    
    # @staticmethod
    # def create(context):
    #     m = re.match(REGEX_PATTERNS['context'], context)
    #     stage = m.groups()[0]
    #     context = m.groups()[1] if len(m.groups()) > 1 else 'default'
    #     # contexts = Config.app_spec['contexts']
    #     # if contexts is None:
    #     #     Config.app_spec['contexts'] = {}
    #     #     contexts = {}
    #     # contexts[stage][context] = 1
    #     Config.app_spec['contexts'][stage][context] = 1
    # @staticmethod
    # def download(context):
    #     pass
    # @staticmethod
    # def delete(context):
    #     pass


    @staticmethod
    def default_context():
        return "default/default"

    @staticmethod
    def raw_parse(context):
        if not context:
            return '', ''
        m = re.match(REGEX_PATTERNS['context'], context)
        if m is None:
            raise DSOException(MESSAGES['InvalidContext'].format(context, REGEX_PATTERNS['context']))
        stage = m.groups()[0]
        env = m.groups()[1] if len(m.groups()) > 1 else ''
        return stage, env

    @staticmethod
    def normalize(context=None):
        if not context:
            return Contexts.default_context()
        stage, env = Contexts.raw_parse(context)
        stage = stage or 'default'
        ### force dafault env if stage is default: default/env not allowed
        env = env if env and not stage == 'default' else 'default'
        return f"{stage}/{env}"

    def parse_normalized(context):
        context = Contexts.normalize(context)
        return Contexts.raw_parse(context)

    @staticmethod
    def get_stage_default_env(context):
        stage = Contexts.parse_normalized(context)[0]
        return f"{stage}/default"


    @staticmethod
    def is_default(context):
        return context == Contexts.default_context()

    @staticmethod
    def is_stage_default_env(context):
        env = Contexts.parse_normalized(context)[1]
        return env == 'default'
