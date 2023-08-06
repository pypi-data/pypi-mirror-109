import os
import re
import yaml
import json
import pathlib
import numbers
import boto3
from botocore.exceptions import ClientError
from dsocli.exceptions import DSOException
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

    def get_parameter_prefix(self, project, application, context, key=None):
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

    def assert_no_scope_overwrites(self, project, application, context, key):
        """
            check if a parameter will overwrite parent or childern parameters (with the same scopes) in the same context (always uninherited)
            e.g.: 
                parameter a.b.c would overwrite a.b (super scope)
                parameter a.b would overwrite a.b.c (sub scope)
        """
        Logger.info(f"Checking parameter overwrites: project={project}, application={application}, context={context}, key={key}")
        scopes = key.split('.')
        ### check parent parameters
        for n in range(len(scopes)-1):
            subKey = '.'.join(scopes[0:n+1])
            path = self.get_parameter_prefix(project, application, context, subKey)
            Logger.info(f"Describing parameters: path={path}")
            # parameters = ssm.describe_parameters(ParameterFilters=[{'Key':'Type', 'Values':['String', 'StringList']},{'Key':'Name', 'Values':[path]}])
            parameters = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Values':[path]}])
            if len(parameters['Parameters']) > 0:
                raise DSOException("Parameter key '{0}' is not allowed in the given context becasue it would overwrite parameter '{1}'.".format(key, subKey))
        ### check children parameters
        path = self.get_parameter_prefix(project, application, context, key)
        # parameters = ssm.describe_parameters(ParameterFilters=[{'Key':'Type','Values':['String', 'StringList']},{'Key':'Name', 'Option': 'BeginsWith', 'Values':[f"{path}."]}])
        parameters = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Option': 'BeginsWith', 'Values':[f"{path}."]}])
        if len(parameters['Parameters']) > 0:
            raise DSOException("Parameter key '{0}' is not allowed in the given context becasue it would overwrite all the parameters in '{0}.*', such as '{0}.{1}'.".format(key,parameters['Parameters'][0]['Name'][len(path)+1:]))

###--------------------------------------------------------------------------------------------

    def locate_parameter(self, project, application, context, key, uninherited=False):

        Logger.debug(f"Locating SSM parameter: project={project}, application={application}, context={context}, key={key}")
        paths = self.get_ssm_search_paths(project, application, context, key, uninherited)
        Logger.debug(f"SSM paths to search in order: {paths}")
        for path in paths:
            Logger.debug(f"Describing SSM parameters: path={path}")
            # result = ssm.describe_parameters(ParameterFilters=[{'Key':'Type','Values':['String', 'StringList']},{'Key':'Name', 'Values':[path]}])
            result = ssm.describe_parameters(ParameterFilters=[{'Key':'Name', 'Values':[path]}])
            if len(result['Parameters']) > 0: return result['Parameters']

###--------------------------------------------------------------------------------------------

    def load_ssm_path(self, parameters, path, recurisve=True):
        Logger.debug(f"Loading SSM parameters: path={path}")
        p = ssm.get_paginator('get_parameters_by_path')
        paginator = p.paginate(Path=path, Recursive=recurisve, ParameterFilters=[{'Key': 'Type','Values': ['String', 'StringList']}]).build_full_result()
        for parameter in paginator['Parameters']:
            key = parameter['Name'][len(path)+1:]
            value = parameter['Value']
            if key in parameters:
                Logger.warn("Inherited parameter '{0}' overridden.".format(key))
            parameters[key] = value
        return parameters

###--------------------------------------------------------------------------------------------

    def get_ssm_search_paths(self, project, application, context, key, uninherited):
        paths = []
        if uninherited:
            paths.append(self.get_parameter_prefix(project, application, context, key))
        else:
            ### check /dso/project/application/stage/env
            paths.append(self.get_parameter_prefix(project, application, context, key))
            if not Contexts.is_stage_default_env(context): ### otherwise already added above
                ### check /dso/project/application/stage/default
                paths.append(self.get_parameter_prefix(project, application, Contexts.get_stage_default_env(context), key))
            if not Contexts.is_default(context): ### otherwise already added above
                ### check /dso/project/application/default
                 paths.append(self.get_parameter_prefix(project, application, Contexts.default_context(), key))
            if not application == 'default': ### otherwise already added above
                ### check /dso/project/default/stage/env
                paths.append(self.get_parameter_prefix(project, 'default', context, key))
                if not Contexts.is_stage_default_env(context): ### otherwise already added above
                    ### check /dso/project/default/stage/default
                    paths.append(self.get_parameter_prefix(project, 'default', Contexts.get_stage_default_env(context), key))
                if not Contexts.is_default(context): ### otherwise already added above
                    ### check /dso/project/default/default
                    paths.append(self.get_parameter_prefix(project, 'default', Contexts.default_context(), key))
                if not project == 'default': ### otherwise already added above
                    ### check /dso/default/default/stage/env
                    paths.append(self.get_parameter_prefix('default', 'default', context, key))
                    if not Contexts.is_stage_default_env(context): ### otherwise already added above
                        ### check /dso/default/default/stage/default
                        paths.append(self.get_parameter_prefix('default', 'default', Contexts.get_stage_default_env(context), key))
                    if not Contexts.is_default(context): ### otherwise already added above
                        ### check /dso/default/default/default
                        paths.append(self.get_parameter_prefix('default', 'default', Contexts.default_context(), key))

        return paths

###--------------------------------------------------------------------------------------------

    def check_application_scope(self):
        applcation = Config.application
        if Config.project == 'default':
            if not Config.application == 'default':
                Logger.warn("Application specific scope for application '{0}' was ignored because the global project scope was used.".format(Config.application))
                application = 'default'
        return applcation

###--------------------------------------------------------------------------------------------

    def list(self, context, uninherited):
        application = self.check_application_scope()
        ### construct search path in hierachy with no key specified in reverse order
        paths = list(reversed(self.get_ssm_search_paths(Config.project, application, context, None, uninherited)))
        Logger.debug(f"SSM paths to search in order: {paths}")
        parameters = {}
        for path in paths:
            self.load_ssm_path(parameters, path)

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

        result = {}
        for key, value in parameters.items():
            if prependGroups:
                key = key.replace('.', nestedDelimiter).replace('/', groupDelimiter)
            else:
                key = key.split('/')[-1].replace('.', nestedDelimiter)
            set_dict_value(result, key.split('.'), value, overwrite_parent=True,  overwrite_children=True)

        return result

###--------------------------------------------------------------------------------------------

    def add(self, context, key, value):
        application = self.check_application_scope()
        self.assert_no_scope_overwrites(Config.project, application, context, key)
        found = self.locate_parameter(Config.project, application, context, key, True)
        if found and len(found) > 0 and not found[0]['Type'] in ['String', 'StringList']:
            raise DSOException(f"Failed to add parameter '{key}' becasue there is already a SSM secret with the same key in the given context.")
        path = self.get_parameter_prefix(Config.project, application, context=context, key=key)
        Logger.debug(f"Adding SSM parameter: path={path}")
        ssm.put_parameter(Name=path, Value=value, Type='String', Overwrite=True)

###--------------------------------------------------------------------------------------------

    def get(self, context, key):
        application = self.check_application_scope()
        found = self.locate_parameter(Config.project, application, context, key)
        if not found or len(found) == 0:
            raise DSOException(f"Parameter '{key}' not found nor inherited: project={Config.project}, application={Config.application}, context={context}, key={key}")
        else:
            # if len(found) > 1:
            #     Logger.warn(f"More than one parameter found at '{found[0]['Name']}'. The first one taken, and the rest were discarded.")
            if not found[0]['Type'] in ['String', 'StringList']:
                raise DSOException(f"Parameter not found: project={Config.project}, application={Config.application}, context={context}, key={key}")
        Logger.debug(f"Getting SSM parameter: path={found[0]['Name']}")
        result = ssm.get_parameter(Name=found[0]['Name'], WithDecryption=True)
        return result['Parameter']['Value']

###--------------------------------------------------------------------------------------------

    def delete(self, context, key):
        application = self.check_application_scope()
        ### only parameters owned by the context can be deleted, hence uninherited=True
        found = self.locate_parameter(Config.project, application, context, key, uninherited=True)
        if not found or len(found) == 0:
            raise DSOException(f"Parameter not found: project={Config.project}, application={Config.application}, context={context}, key={key}")
        else:
            # if len(found) > 1:
            #     Logger.warn(f"More than one parameter found at '{found[0]['Name']}'. The first one taken, and the rest were discarded.")
            if not found[0]['Type'] in ['String', 'StringList']:
                raise DSOException(f"Parameter not found: project={Config.project}, application={Config.application}, context={context}, key={key}")
        Logger.debug(f"Deleting SSM parameter: path={found[0]['Name']}")
        ssm.delete_parameter(Name=found[0]['Name'])

