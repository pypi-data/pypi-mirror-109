
import re
from .config import Config
from .providers import ProviderManager
from .constants import *

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
    def parse_context(context):
        if not context:
            return '', ''
        m = re.match(REGEX_PATTERNS['context'], context)
        if m is None:
            raise Exception(MESSAGES['InvalidContext'].format(context, REGEX_PATTERNS['context']))
        stage = m.groups()[0]
        if len(m.groups()) > 1:
            env = 'default' if m.groups()[1] == '' else  m.groups()[1] 
        return stage, env

    @staticmethod
    def normalize(context):
        if not context or context == 'default':
            return 'default'
        m = re.match(REGEX_PATTERNS['context'], context)
        if m is None:
            raise Exception(MESSAGES['InvalidContext'].format(context, REGEX_PATTERNS['context']))
        stage = m.groups()[0]
        env = m.groups()[1] if len(m.groups()) > 0 and m.groups()[1] else 'default'
        return f"{stage}/{env}"

    @staticmethod
    def get_default(context=None):
        if not context:
            return 'default'
        m = re.match(REGEX_PATTERNS['context'], context)
        if m is None:
            raise Exception(MESSAGES['InvalidContext'].format(context, REGEX_PATTERNS['context']))
        stage = m.groups()[0]
        return f"{stage}/default"

    @staticmethod
    def is_default(context):
        context = Contexts.normalize(context)
        if context == 'default':
            return True
        m = re.match(REGEX_PATTERNS['context'], context)
        return m.groups()[1] == 'default'
