# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Certificate(pulumi.CustomResource):
    certificate_content: pulumi.Output[str]
    """
    The Base-64 representation of the X509 leaf certificate .cer file or just a .pem file content.
    """
    iot_dps_name: pulumi.Output[str]
    """
    The name of the IoT Device Provisioning Service that this certificate will be attached to. Changing this forces a new resource to be created.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the Iot Device Provisioning Service Certificate resource. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group under which the Iot Device Provisioning Service Certificate resource has to be created. Changing this forces a new resource to be created.
    """
    def __init__(__self__, resource_name, opts=None, certificate_content=None, iot_dps_name=None, name=None, resource_group_name=None, __name__=None, __opts__=None):
        """
        Manages an IoT Device Provisioning Service Certificate.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate_content: The Base-64 representation of the X509 leaf certificate .cer file or just a .pem file content.
        :param pulumi.Input[str] iot_dps_name: The name of the IoT Device Provisioning Service that this certificate will be attached to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Iot Device Provisioning Service Certificate resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group under which the Iot Device Provisioning Service Certificate resource has to be created. Changing this forces a new resource to be created.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/iot_dps_certificate.html.markdown.
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

        if certificate_content is None:
            raise TypeError("Missing required property 'certificate_content'")
        __props__['certificate_content'] = certificate_content

        if iot_dps_name is None:
            raise TypeError("Missing required property 'iot_dps_name'")
        __props__['iot_dps_name'] = iot_dps_name

        __props__['name'] = name

        if resource_group_name is None:
            raise TypeError("Missing required property 'resource_group_name'")
        __props__['resource_group_name'] = resource_group_name

        super(Certificate, __self__).__init__(
            'azure:iot/certificate:Certificate',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

