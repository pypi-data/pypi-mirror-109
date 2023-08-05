import os
import re
import yaml
import json
import pathlib
import numbers
import boto3
from botocore.exceptions import ClientError
from dsocli.logger import Logger
from dsocli.config import Config
from dsocli.parameters import ParameterProvider
from dsocli.contexts import Contexts
from dsocli.constants import *
from dsocli.utils import set_dict_value


defaults = {
    'allowGroups': 'no',
    'prependGroups': 'yes',
    'groupDelimiter': '/',
    'nestedDelimiter': '.',
}


session = boto3.session.Session()
ssm = session.client(
    service_name='ssm',
    region_name='ap-southeast-2',
)


class AwsSsmParameterProvider(ParameterProvider):

    def __init__(self):
        super().__init__('parameter/aws/ssm/v1')

###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

    def __get_parameter_prefix(self, project, application, context, key=None):
        # output = f"/dso/{project}/{application}/{context}"
        output = "/dso"
        output += f"/{project}"
        ### every application must belong to a project, no application overrides allowed in the default project
        if not project == 'default':
            output += f"/{application}"
        else:
            output += f"/default"
        ### context must be normalized before
        output += f"/{context}"
        if key:
            output += f"/{key}"
        return output


###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

    def get_key_validator(self):

        allowGroups = Config.parameter_spec('allowGroups')
        if allowGroups is None:
            Logger.debug(f"'allowGroups' is not set for the parameter provider, defaulted to '{defaults['allowGroups']}'.")
            allowGroups = defaults['allowGroups']

        if allowGroups:
            return r"^([a-zA-Z][a-zA-Z0-9]*/)?([a-zA-Z][a-zA-Z0-9_.-]*)$"
        else:
            return r"^([a-zA-Z][a-zA-Z0-9_.-]*)$"


###--------------------------------------------------------------------------------------------

    def check_parameter_overwrites(self, context, key):
        scopes = key.split('.')
        ### check parent parameters
        for n in range(len(scopes)-1):
            subKey = '.'.join(scopes[0:n+1])
            path = self.__get_parameter_prefix(Config.project, Config.application, context, subKey)
            parameters = ssm.describe_parameters(ParameterFilters=[{'Key':'Type', 'Values':['String', 'StringList']},{'Key':'Name', 'Values':[path]}])
            if len(parameters['Parameters']) > 0:
                raise Exception("Parameter key '{0}' is not allowed in the given context becasue it would overwrite parameter '{1}'.".format(key, subKey))
        ### check children parameters
        path = self.__get_parameter_prefix(Config.project, Config.application, context, key)
        parameters = ssm.describe_parameters(ParameterFilters=[{'Key':'Type','Values':['String', 'StringList']},{'Key':'Name', 'Option': 'BeginsWith', 'Values':[f"{path}."]}])
        if len(parameters['Parameters']) > 0:
            raise Exception("Parameter key '{0}' is not allowed in the given context becasue it would overwrite parameter '{1}'.".format(key,parameters['Parameters'][0]['Name'][len(path):]))

###--------------------------------------------------------------------------------------------

    def describe_parameters(self, context, key):
        path = self.__get_parameter_prefix(Config.project, Config.application, context, key)
        result = ssm.describe_parameters(ParameterFilters=[{'Key':'Type','Values':['String', 'StringList']},{'Key':'Name', 'Values':[path]}])
        return result['Parameters']

###--------------------------------------------------------------------------------------------

    def list(self, context, uninherited):

        def load_ssm_path(parameters, path, recurisve=True):
            Logger.debug(f"Loading SSM parameters: path={path}")
            p = ssm.get_paginator('get_parameters_by_path')
            paginator = p.paginate(Path=path, Recursive=recurisve, ParameterFilters=[{'Key': 'Type','Values': ['String', 'StringList']}]).build_full_result()
            for parameter in paginator['Parameters']:
                key = parameter['Name'][len(path)+1:]
                value = parameter['Value']
                if key in parameters:
                    Logger.debug("Inherited parameter '{0}' overridden.".format(key))
                parameters[key] = value

        if Config.project == 'default':
            if not Config.application == 'default':
                Logger.warn("Application specific scope for '{0}' was ignored because the default project scope was used.".format(Config.application))

        parameters = {}

        if uninherited:
            load_ssm_path(parameters, self.__get_parameter_prefix(project=Config.project, application=Config.application, context=context))
        else:
 
            ### get default project, default application, default context: /dso/default/default/default
            load_ssm_path(parameters, self.__get_parameter_prefix(project='default', application='default', context='default'))
            if not context == 'default':
                ### get default project, default application, stage specific, default environment: /dso/default/default/stage/default
                load_ssm_path(parameters, self.__get_parameter_prefix(project='default', application='default', context=Contexts.get_default(context)))
                if not Contexts.is_default(context):
                    ### get default project, default application, stage specific, environment specific: /dso/default/stage/env
                    load_ssm_path(parameters, self.__get_parameter_prefix(project='default', application='default', context=context))

            if not Config.project == 'default':
                ### get project specific, default application, default context: /dso/project/default/default
                load_ssm_path(parameters, self.__get_parameter_prefix(project=Config.project, application='default', context='default'))
                if not context == 'default':
                    ### get project specific, default application, stage specific, default environment: /dso/project/default/stage/default
                    load_ssm_path(parameters, self.__get_parameter_prefix(project=Config.project, application='default', context=Contexts.get_default(context)))
                    if not Contexts.is_default(context):
                        ### get project specific, default application, stage specific, environment specific: /dso/project/default/stage/default
                        load_ssm_path(parameters, self.__get_parameter_prefix(project=Config.project, application='default', context=context))

                if not Config.application == 'default':
                    ### get project specific, application specific, default context: /dso/project/application/default
                    load_ssm_path(parameters, self.__get_parameter_prefix(project=Config.project, application=Config.application, context='default'))
                    if not context == 'default':
                        ### get project specific, application specific, stage specific, default environment: /dso/project/application/stage/default
                        load_ssm_path(parameters, self.__get_parameter_prefix(project=Config.project, application=Config.application, context=Contexts.get_default(context)))
                        if not Contexts.is_default(context):
                            ### get project specific, application specific, stage specific, environment specific: /dso/project/application/stage/env
                            load_ssm_path(parameters, self.__get_parameter_prefix(project=Config.project, application=Config.application, context=context))

        result = {}

        prependGroups = Config.parameter_spec('prependGroups')
        if prependGroups is None:
            Logger.debug(f"'prependGroups' is not set for the parameter provider, defaulted to '{defaults['prependGroups']}'.")
            prependGroups = defaults['prependGroups']

        groupDelimiter = Config.parameter_spec('groupDelimiter')
        if groupDelimiter is None:
            Logger.debug(f"'groupDelimiter' is not set for the parameter provider, defaulted to '{defaults['groupDelimiter']}'.")
            groupDelimiter = defaults['groupDelimiter']

        nestedDelimiter = Config.parameter_spec('nestedDelimiter')
        if nestedDelimiter is None:
            Logger.debug(f"'nestedDelimiter' is not set for the parameter provider, defaulted to '{defaults['nestedDelimiter']}'.")
            nestedDelimiter = defaults['nestedDelimiter']

        for key, value in parameters.items():
            if prependGroups:
                key = key.replace('.', nestedDelimiter).replace('/', groupDelimiter)
            else:
                key = key.split('/')[-1].replace('.', nestedDelimiter)
            set_dict_value(result, key.split('.'), value, overwrite_parent=True,  overwrite_children=True)

        return result

###--------------------------------------------------------------------------------------------

    def add(self, context, key, value):
        if Config.project == 'default':
            if not Config.application == 'default':
                Logger.warn("Application specific scope for '{0}' was ignored because the default project scope was used.".format(Config.application))
        self.check_parameter_overwrites(context, key)
        path = self.__get_parameter_prefix(project=Config.project, application=Config.application, context=context, key=key)
        Logger.debug(f"Parameter path={path}")
        ssm.put_parameter(Name=path, Value=value, Type='String', Overwrite=True)

###--------------------------------------------------------------------------------------------

    def get(self, context, key):
        if Config.project == 'default':
            if not Config.application == 'default':
                Logger.warn("Application specific scope for '{0}' was ignored because the default project scope was used.".format(Config.application))
        existing = self.describe_parameters(context, key)
        if len(existing) == 0:
                raise Exception(MESSAGES['ParameterNotFound'].format(key))
        path = self.__get_parameter_prefix(Config.project, Config.application, context, key)
        Logger.debug(f"Parameter path={path}")
        try:
            result = ssm.get_parameter(Name=path, WithDecryption=True)
            return result['Parameter']['Value']
        except ClientError as e:
            if e.response['Error']['Code'] == 'ParameterNotFound':
                raise Exception(MESSAGES['ParameterNotFound'].format(key))
            else:
                raise
        except:
            raise

###--------------------------------------------------------------------------------------------

    def delete(self, context, key):
        if Config.project == 'default':
            if not Config.application == 'default':
                Logger.warn("Application specific scope for '{0}' was ignored because the default project scope was used.".format(Config.application))
        existing = self.describe_parameters(context, key)
        if len(existing) == 0:
                raise Exception(MESSAGES['ParameterNotFound'].format(key))
        path = self.__get_parameter_prefix(Config.project, Config.application, context, key)
        Logger.debug(f"Parameter path={path}")
        try:
            ssm.delete_parameter(Name=path)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ParameterNotFound':
                raise Exception(MESSAGES['ParameterNotFound'].format(key))
            else:
                raise
        except:
            raise
