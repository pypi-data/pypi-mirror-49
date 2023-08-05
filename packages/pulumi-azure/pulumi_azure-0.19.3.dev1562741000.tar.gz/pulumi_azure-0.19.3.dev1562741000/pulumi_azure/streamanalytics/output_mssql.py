# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class OutputMssql(pulumi.CustomResource):
    database: pulumi.Output[str]
    name: pulumi.Output[str]
    """
    The name of the Stream Output. Changing this forces a new resource to be created.
    """
    password: pulumi.Output[str]
    """
    Password used together with username, to login to the Microsoft SQL Server. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the Resource Group where the Stream Analytics Job exists. Changing this forces a new resource to be created.
    """
    server: pulumi.Output[str]
    """
    The SQL server url. Changing this forces a new resource to be created.
    """
    stream_analytics_job_name: pulumi.Output[str]
    """
    The name of the Stream Analytics Job. Changing this forces a new resource to be created.
    """
    table: pulumi.Output[str]
    """
    Table in the database that the output points to. Changing this forces a new resource to be created.
    """
    user: pulumi.Output[str]
    """
    Username used to login to the Microsoft SQL Server. Changing this forces a new resource to be created.
    """
    def __init__(__self__, resource_name, opts=None, database=None, name=None, password=None, resource_group_name=None, server=None, stream_analytics_job_name=None, table=None, user=None, __name__=None, __opts__=None):
        """
        Manages a Stream Analytics Output to Microsoft SQL Server Database.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the Stream Output. Changing this forces a new resource to be created.
        :param pulumi.Input[str] password: Password used together with username, to login to the Microsoft SQL Server. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Stream Analytics Job exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] server: The SQL server url. Changing this forces a new resource to be created.
        :param pulumi.Input[str] stream_analytics_job_name: The name of the Stream Analytics Job. Changing this forces a new resource to be created.
        :param pulumi.Input[str] table: Table in the database that the output points to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] user: Username used to login to the Microsoft SQL Server. Changing this forces a new resource to be created.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/stream_analytics_output_mssql.html.markdown.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if not resource_name:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(resource_name, str):
            raise TypeError('Expected resource name to be a string')
        if opts and not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if database is None:
            raise TypeError("Missing required property 'database'")
        __props__['database'] = database

        __props__['name'] = name

        if password is None:
            raise TypeError("Missing required property 'password'")
        __props__['password'] = password

        if resource_group_name is None:
            raise TypeError("Missing required property 'resource_group_name'")
        __props__['resource_group_name'] = resource_group_name

        if server is None:
            raise TypeError("Missing required property 'server'")
        __props__['server'] = server

        if stream_analytics_job_name is None:
            raise TypeError("Missing required property 'stream_analytics_job_name'")
        __props__['stream_analytics_job_name'] = stream_analytics_job_name

        if table is None:
            raise TypeError("Missing required property 'table'")
        __props__['table'] = table

        if user is None:
            raise TypeError("Missing required property 'user'")
        __props__['user'] = user

        super(OutputMssql, __self__).__init__(
            'azure:streamanalytics/outputMssql:OutputMssql',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

