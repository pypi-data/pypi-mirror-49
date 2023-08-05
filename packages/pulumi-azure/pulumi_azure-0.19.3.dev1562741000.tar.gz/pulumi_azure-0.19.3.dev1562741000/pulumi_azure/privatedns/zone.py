# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Zone(pulumi.CustomResource):
    max_number_of_record_sets: pulumi.Output[float]
    """
    The maximum number of record sets that can be created in this Private DNS zone.
    """
    max_number_of_virtual_network_links: pulumi.Output[float]
    """
    The maximum number of virtual networks that can be linked to this Private DNS zone.
    """
    max_number_of_virtual_network_links_with_registration: pulumi.Output[float]
    """
    The maximum number of virtual networks that can be linked to this Private DNS zone with registration enabled.
    """
    name: pulumi.Output[str]
    """
    The name of the Private DNS Zone. Must be a valid domain name.
    """
    number_of_record_sets: pulumi.Output[float]
    """
    The current number of record sets in this Private DNS zone.
    """
    resource_group_name: pulumi.Output[str]
    """
    Specifies the resource group where the resource exists. Changing this forces a new resource to be created.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    def __init__(__self__, resource_name, opts=None, name=None, resource_group_name=None, tags=None, __name__=None, __opts__=None):
        """
        Enables you to manage Private DNS zones within Azure DNS. These zones are hosted on Azure's name servers.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the Private DNS Zone. Must be a valid domain name.
        :param pulumi.Input[str] resource_group_name: Specifies the resource group where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/private_dns_zone.html.markdown.
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

        __props__['name'] = name

        if resource_group_name is None:
            raise TypeError("Missing required property 'resource_group_name'")
        __props__['resource_group_name'] = resource_group_name

        __props__['tags'] = tags

        __props__['max_number_of_record_sets'] = None
        __props__['max_number_of_virtual_network_links'] = None
        __props__['max_number_of_virtual_network_links_with_registration'] = None
        __props__['number_of_record_sets'] = None

        super(Zone, __self__).__init__(
            'azure:privatedns/zone:Zone',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

