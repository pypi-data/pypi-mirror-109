# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['TemplateArgs', 'Template']

@pulumi.input_type
class TemplateArgs:
    def __init__(__self__, *,
                 code: pulumi.Input[str],
                 cloud_config: Optional[pulumi.Input[str]] = None,
                 default_username: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 image_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 short_description: Optional[pulumi.Input[str]] = None,
                 volume_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Template resource.
        :param pulumi.Input[str] code: This is a unqiue, alphanumerical, short, human readable code for the template.
        :param pulumi.Input[str] cloud_config: Commonly referred to as 'user-data', this is a customisation script that is run after
               the instance is first booted. We recommend using cloud-config as it's a great distribution-agnostic
               way of configuring cloud servers. If you put `$INITIAL_USER` in your script, this will automatically
               be replaced by the initial user chosen when creating the instance, `$INITIAL_PASSWORD` will be
               replaced with the random password generated by the system, `$HOSTNAME` is the fully qualified
               domain name of the instance and `$SSH_KEY` will be the content of the SSH public key.
               (this is technically optional, but you won't really be able to use instances without it -
               see our learn guide on templates for more information).
        :param pulumi.Input[str] default_username: The default username to suggest that the user creates
        :param pulumi.Input[str] description: A multi-line description of the template, in Markdown format
        :param pulumi.Input[str] image_id: This is the Image ID of any default template or the ID of another template
               either owned by you or global (optional; but must be specified if no volume_id is specified).
        :param pulumi.Input[str] name: This is a short human readable name for the template
        :param pulumi.Input[str] short_description: A one line description of the template
        :param pulumi.Input[str] volume_id: This is the ID of a bootable volume, either owned by you or global
               (optional; but must be specified if no image_id is specified)
        """
        pulumi.set(__self__, "code", code)
        if cloud_config is not None:
            pulumi.set(__self__, "cloud_config", cloud_config)
        if default_username is not None:
            pulumi.set(__self__, "default_username", default_username)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if image_id is not None:
            pulumi.set(__self__, "image_id", image_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if short_description is not None:
            pulumi.set(__self__, "short_description", short_description)
        if volume_id is not None:
            pulumi.set(__self__, "volume_id", volume_id)

    @property
    @pulumi.getter
    def code(self) -> pulumi.Input[str]:
        """
        This is a unqiue, alphanumerical, short, human readable code for the template.
        """
        return pulumi.get(self, "code")

    @code.setter
    def code(self, value: pulumi.Input[str]):
        pulumi.set(self, "code", value)

    @property
    @pulumi.getter(name="cloudConfig")
    def cloud_config(self) -> Optional[pulumi.Input[str]]:
        """
        Commonly referred to as 'user-data', this is a customisation script that is run after
        the instance is first booted. We recommend using cloud-config as it's a great distribution-agnostic
        way of configuring cloud servers. If you put `$INITIAL_USER` in your script, this will automatically
        be replaced by the initial user chosen when creating the instance, `$INITIAL_PASSWORD` will be
        replaced with the random password generated by the system, `$HOSTNAME` is the fully qualified
        domain name of the instance and `$SSH_KEY` will be the content of the SSH public key.
        (this is technically optional, but you won't really be able to use instances without it -
        see our learn guide on templates for more information).
        """
        return pulumi.get(self, "cloud_config")

    @cloud_config.setter
    def cloud_config(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cloud_config", value)

    @property
    @pulumi.getter(name="defaultUsername")
    def default_username(self) -> Optional[pulumi.Input[str]]:
        """
        The default username to suggest that the user creates
        """
        return pulumi.get(self, "default_username")

    @default_username.setter
    def default_username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_username", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A multi-line description of the template, in Markdown format
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="imageId")
    def image_id(self) -> Optional[pulumi.Input[str]]:
        """
        This is the Image ID of any default template or the ID of another template
        either owned by you or global (optional; but must be specified if no volume_id is specified).
        """
        return pulumi.get(self, "image_id")

    @image_id.setter
    def image_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "image_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        This is a short human readable name for the template
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="shortDescription")
    def short_description(self) -> Optional[pulumi.Input[str]]:
        """
        A one line description of the template
        """
        return pulumi.get(self, "short_description")

    @short_description.setter
    def short_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "short_description", value)

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> Optional[pulumi.Input[str]]:
        """
        This is the ID of a bootable volume, either owned by you or global
        (optional; but must be specified if no image_id is specified)
        """
        return pulumi.get(self, "volume_id")

    @volume_id.setter
    def volume_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "volume_id", value)


@pulumi.input_type
class _TemplateState:
    def __init__(__self__, *,
                 cloud_config: Optional[pulumi.Input[str]] = None,
                 code: Optional[pulumi.Input[str]] = None,
                 default_username: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 image_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 short_description: Optional[pulumi.Input[str]] = None,
                 volume_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Template resources.
        :param pulumi.Input[str] cloud_config: Commonly referred to as 'user-data', this is a customisation script that is run after
               the instance is first booted. We recommend using cloud-config as it's a great distribution-agnostic
               way of configuring cloud servers. If you put `$INITIAL_USER` in your script, this will automatically
               be replaced by the initial user chosen when creating the instance, `$INITIAL_PASSWORD` will be
               replaced with the random password generated by the system, `$HOSTNAME` is the fully qualified
               domain name of the instance and `$SSH_KEY` will be the content of the SSH public key.
               (this is technically optional, but you won't really be able to use instances without it -
               see our learn guide on templates for more information).
        :param pulumi.Input[str] code: This is a unqiue, alphanumerical, short, human readable code for the template.
        :param pulumi.Input[str] default_username: The default username to suggest that the user creates
        :param pulumi.Input[str] description: A multi-line description of the template, in Markdown format
        :param pulumi.Input[str] image_id: This is the Image ID of any default template or the ID of another template
               either owned by you or global (optional; but must be specified if no volume_id is specified).
        :param pulumi.Input[str] name: This is a short human readable name for the template
        :param pulumi.Input[str] short_description: A one line description of the template
        :param pulumi.Input[str] volume_id: This is the ID of a bootable volume, either owned by you or global
               (optional; but must be specified if no image_id is specified)
        """
        if cloud_config is not None:
            pulumi.set(__self__, "cloud_config", cloud_config)
        if code is not None:
            pulumi.set(__self__, "code", code)
        if default_username is not None:
            pulumi.set(__self__, "default_username", default_username)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if image_id is not None:
            pulumi.set(__self__, "image_id", image_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if short_description is not None:
            pulumi.set(__self__, "short_description", short_description)
        if volume_id is not None:
            pulumi.set(__self__, "volume_id", volume_id)

    @property
    @pulumi.getter(name="cloudConfig")
    def cloud_config(self) -> Optional[pulumi.Input[str]]:
        """
        Commonly referred to as 'user-data', this is a customisation script that is run after
        the instance is first booted. We recommend using cloud-config as it's a great distribution-agnostic
        way of configuring cloud servers. If you put `$INITIAL_USER` in your script, this will automatically
        be replaced by the initial user chosen when creating the instance, `$INITIAL_PASSWORD` will be
        replaced with the random password generated by the system, `$HOSTNAME` is the fully qualified
        domain name of the instance and `$SSH_KEY` will be the content of the SSH public key.
        (this is technically optional, but you won't really be able to use instances without it -
        see our learn guide on templates for more information).
        """
        return pulumi.get(self, "cloud_config")

    @cloud_config.setter
    def cloud_config(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cloud_config", value)

    @property
    @pulumi.getter
    def code(self) -> Optional[pulumi.Input[str]]:
        """
        This is a unqiue, alphanumerical, short, human readable code for the template.
        """
        return pulumi.get(self, "code")

    @code.setter
    def code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "code", value)

    @property
    @pulumi.getter(name="defaultUsername")
    def default_username(self) -> Optional[pulumi.Input[str]]:
        """
        The default username to suggest that the user creates
        """
        return pulumi.get(self, "default_username")

    @default_username.setter
    def default_username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_username", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A multi-line description of the template, in Markdown format
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="imageId")
    def image_id(self) -> Optional[pulumi.Input[str]]:
        """
        This is the Image ID of any default template or the ID of another template
        either owned by you or global (optional; but must be specified if no volume_id is specified).
        """
        return pulumi.get(self, "image_id")

    @image_id.setter
    def image_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "image_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        This is a short human readable name for the template
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="shortDescription")
    def short_description(self) -> Optional[pulumi.Input[str]]:
        """
        A one line description of the template
        """
        return pulumi.get(self, "short_description")

    @short_description.setter
    def short_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "short_description", value)

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> Optional[pulumi.Input[str]]:
        """
        This is the ID of a bootable volume, either owned by you or global
        (optional; but must be specified if no image_id is specified)
        """
        return pulumi.get(self, "volume_id")

    @volume_id.setter
    def volume_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "volume_id", value)


class Template(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cloud_config: Optional[pulumi.Input[str]] = None,
                 code: Optional[pulumi.Input[str]] = None,
                 default_username: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 image_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 short_description: Optional[pulumi.Input[str]] = None,
                 volume_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Civo Template resource.
        This can be used to create, modify, and delete Templates.

        ## Import

        Template can be imported using the template `code`, e.g.

        ```sh
         $ pulumi import civo:index/template:Template my-custom-template my-template-code
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cloud_config: Commonly referred to as 'user-data', this is a customisation script that is run after
               the instance is first booted. We recommend using cloud-config as it's a great distribution-agnostic
               way of configuring cloud servers. If you put `$INITIAL_USER` in your script, this will automatically
               be replaced by the initial user chosen when creating the instance, `$INITIAL_PASSWORD` will be
               replaced with the random password generated by the system, `$HOSTNAME` is the fully qualified
               domain name of the instance and `$SSH_KEY` will be the content of the SSH public key.
               (this is technically optional, but you won't really be able to use instances without it -
               see our learn guide on templates for more information).
        :param pulumi.Input[str] code: This is a unqiue, alphanumerical, short, human readable code for the template.
        :param pulumi.Input[str] default_username: The default username to suggest that the user creates
        :param pulumi.Input[str] description: A multi-line description of the template, in Markdown format
        :param pulumi.Input[str] image_id: This is the Image ID of any default template or the ID of another template
               either owned by you or global (optional; but must be specified if no volume_id is specified).
        :param pulumi.Input[str] name: This is a short human readable name for the template
        :param pulumi.Input[str] short_description: A one line description of the template
        :param pulumi.Input[str] volume_id: This is the ID of a bootable volume, either owned by you or global
               (optional; but must be specified if no image_id is specified)
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TemplateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Civo Template resource.
        This can be used to create, modify, and delete Templates.

        ## Import

        Template can be imported using the template `code`, e.g.

        ```sh
         $ pulumi import civo:index/template:Template my-custom-template my-template-code
        ```

        :param str resource_name: The name of the resource.
        :param TemplateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TemplateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cloud_config: Optional[pulumi.Input[str]] = None,
                 code: Optional[pulumi.Input[str]] = None,
                 default_username: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 image_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 short_description: Optional[pulumi.Input[str]] = None,
                 volume_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TemplateArgs.__new__(TemplateArgs)

            __props__.__dict__["cloud_config"] = cloud_config
            if code is None and not opts.urn:
                raise TypeError("Missing required property 'code'")
            __props__.__dict__["code"] = code
            __props__.__dict__["default_username"] = default_username
            __props__.__dict__["description"] = description
            __props__.__dict__["image_id"] = image_id
            __props__.__dict__["name"] = name
            __props__.__dict__["short_description"] = short_description
            __props__.__dict__["volume_id"] = volume_id
        super(Template, __self__).__init__(
            'civo:index/template:Template',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cloud_config: Optional[pulumi.Input[str]] = None,
            code: Optional[pulumi.Input[str]] = None,
            default_username: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            image_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            short_description: Optional[pulumi.Input[str]] = None,
            volume_id: Optional[pulumi.Input[str]] = None) -> 'Template':
        """
        Get an existing Template resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cloud_config: Commonly referred to as 'user-data', this is a customisation script that is run after
               the instance is first booted. We recommend using cloud-config as it's a great distribution-agnostic
               way of configuring cloud servers. If you put `$INITIAL_USER` in your script, this will automatically
               be replaced by the initial user chosen when creating the instance, `$INITIAL_PASSWORD` will be
               replaced with the random password generated by the system, `$HOSTNAME` is the fully qualified
               domain name of the instance and `$SSH_KEY` will be the content of the SSH public key.
               (this is technically optional, but you won't really be able to use instances without it -
               see our learn guide on templates for more information).
        :param pulumi.Input[str] code: This is a unqiue, alphanumerical, short, human readable code for the template.
        :param pulumi.Input[str] default_username: The default username to suggest that the user creates
        :param pulumi.Input[str] description: A multi-line description of the template, in Markdown format
        :param pulumi.Input[str] image_id: This is the Image ID of any default template or the ID of another template
               either owned by you or global (optional; but must be specified if no volume_id is specified).
        :param pulumi.Input[str] name: This is a short human readable name for the template
        :param pulumi.Input[str] short_description: A one line description of the template
        :param pulumi.Input[str] volume_id: This is the ID of a bootable volume, either owned by you or global
               (optional; but must be specified if no image_id is specified)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TemplateState.__new__(_TemplateState)

        __props__.__dict__["cloud_config"] = cloud_config
        __props__.__dict__["code"] = code
        __props__.__dict__["default_username"] = default_username
        __props__.__dict__["description"] = description
        __props__.__dict__["image_id"] = image_id
        __props__.__dict__["name"] = name
        __props__.__dict__["short_description"] = short_description
        __props__.__dict__["volume_id"] = volume_id
        return Template(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cloudConfig")
    def cloud_config(self) -> pulumi.Output[Optional[str]]:
        """
        Commonly referred to as 'user-data', this is a customisation script that is run after
        the instance is first booted. We recommend using cloud-config as it's a great distribution-agnostic
        way of configuring cloud servers. If you put `$INITIAL_USER` in your script, this will automatically
        be replaced by the initial user chosen when creating the instance, `$INITIAL_PASSWORD` will be
        replaced with the random password generated by the system, `$HOSTNAME` is the fully qualified
        domain name of the instance and `$SSH_KEY` will be the content of the SSH public key.
        (this is technically optional, but you won't really be able to use instances without it -
        see our learn guide on templates for more information).
        """
        return pulumi.get(self, "cloud_config")

    @property
    @pulumi.getter
    def code(self) -> pulumi.Output[str]:
        """
        This is a unqiue, alphanumerical, short, human readable code for the template.
        """
        return pulumi.get(self, "code")

    @property
    @pulumi.getter(name="defaultUsername")
    def default_username(self) -> pulumi.Output[Optional[str]]:
        """
        The default username to suggest that the user creates
        """
        return pulumi.get(self, "default_username")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A multi-line description of the template, in Markdown format
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="imageId")
    def image_id(self) -> pulumi.Output[Optional[str]]:
        """
        This is the Image ID of any default template or the ID of another template
        either owned by you or global (optional; but must be specified if no volume_id is specified).
        """
        return pulumi.get(self, "image_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        This is a short human readable name for the template
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="shortDescription")
    def short_description(self) -> pulumi.Output[Optional[str]]:
        """
        A one line description of the template
        """
        return pulumi.get(self, "short_description")

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> pulumi.Output[Optional[str]]:
        """
        This is the ID of a bootable volume, either owned by you or global
        (optional; but must be specified if no image_id is specified)
        """
        return pulumi.get(self, "volume_id")

