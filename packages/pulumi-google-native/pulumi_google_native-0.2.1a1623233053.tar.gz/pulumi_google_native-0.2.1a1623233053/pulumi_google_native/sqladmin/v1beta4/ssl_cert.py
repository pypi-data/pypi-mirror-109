# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['SslCertArgs', 'SslCert']

@pulumi.input_type
class SslCertArgs:
    def __init__(__self__, *,
                 instance: pulumi.Input[str],
                 project: pulumi.Input[str],
                 common_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SslCert resource.
        :param pulumi.Input[str] common_name: User supplied name. Must be a distinct name from the other certificates for this instance.
        """
        pulumi.set(__self__, "instance", instance)
        pulumi.set(__self__, "project", project)
        if common_name is not None:
            pulumi.set(__self__, "common_name", common_name)

    @property
    @pulumi.getter
    def instance(self) -> pulumi.Input[str]:
        return pulumi.get(self, "instance")

    @instance.setter
    def instance(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance", value)

    @property
    @pulumi.getter
    def project(self) -> pulumi.Input[str]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: pulumi.Input[str]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="commonName")
    def common_name(self) -> Optional[pulumi.Input[str]]:
        """
        User supplied name. Must be a distinct name from the other certificates for this instance.
        """
        return pulumi.get(self, "common_name")

    @common_name.setter
    def common_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "common_name", value)


class SslCert(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 common_name: Optional[pulumi.Input[str]] = None,
                 instance: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates an SSL certificate and returns it along with the private key and server certificate authority. The new certificate will not be usable until the instance is restarted.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] common_name: User supplied name. Must be a distinct name from the other certificates for this instance.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SslCertArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates an SSL certificate and returns it along with the private key and server certificate authority. The new certificate will not be usable until the instance is restarted.

        :param str resource_name: The name of the resource.
        :param SslCertArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SslCertArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 common_name: Optional[pulumi.Input[str]] = None,
                 instance: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
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
            __props__ = SslCertArgs.__new__(SslCertArgs)

            __props__.__dict__["common_name"] = common_name
            if instance is None and not opts.urn:
                raise TypeError("Missing required property 'instance'")
            __props__.__dict__["instance"] = instance
            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            __props__.__dict__["cert"] = None
            __props__.__dict__["cert_serial_number"] = None
            __props__.__dict__["create_time"] = None
            __props__.__dict__["expiration_time"] = None
            __props__.__dict__["kind"] = None
            __props__.__dict__["self_link"] = None
            __props__.__dict__["sha1_fingerprint"] = None
        super(SslCert, __self__).__init__(
            'google-native:sqladmin/v1beta4:SslCert',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SslCert':
        """
        Get an existing SslCert resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SslCertArgs.__new__(SslCertArgs)

        __props__.__dict__["cert"] = None
        __props__.__dict__["cert_serial_number"] = None
        __props__.__dict__["common_name"] = None
        __props__.__dict__["create_time"] = None
        __props__.__dict__["expiration_time"] = None
        __props__.__dict__["instance"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["self_link"] = None
        __props__.__dict__["sha1_fingerprint"] = None
        return SslCert(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def cert(self) -> pulumi.Output[str]:
        """
        PEM representation.
        """
        return pulumi.get(self, "cert")

    @property
    @pulumi.getter(name="certSerialNumber")
    def cert_serial_number(self) -> pulumi.Output[str]:
        """
        Serial number, as extracted from the certificate.
        """
        return pulumi.get(self, "cert_serial_number")

    @property
    @pulumi.getter(name="commonName")
    def common_name(self) -> pulumi.Output[str]:
        """
        User supplied name. Constrained to [a-zA-Z.-_ ]+.
        """
        return pulumi.get(self, "common_name")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The time when the certificate was created in RFC 3339 format, for example *2012-11-15T16:19:00.094Z*
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="expirationTime")
    def expiration_time(self) -> pulumi.Output[str]:
        """
        The time when the certificate expires in RFC 3339 format, for example *2012-11-15T16:19:00.094Z*.
        """
        return pulumi.get(self, "expiration_time")

    @property
    @pulumi.getter
    def instance(self) -> pulumi.Output[str]:
        """
        Name of the database instance.
        """
        return pulumi.get(self, "instance")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        This is always *sql#sslCert*.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        The URI of this resource.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="sha1Fingerprint")
    def sha1_fingerprint(self) -> pulumi.Output[str]:
        """
        Sha1 Fingerprint.
        """
        return pulumi.get(self, "sha1_fingerprint")

