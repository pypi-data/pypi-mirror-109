# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *

__all__ = ['CryptoKeyVersionArgs', 'CryptoKeyVersion']

@pulumi.input_type
class CryptoKeyVersionArgs:
    def __init__(__self__, *,
                 crypto_key_id: pulumi.Input[str],
                 key_ring_id: pulumi.Input[str],
                 location: pulumi.Input[str],
                 project: pulumi.Input[str],
                 external_protection_level_options: Optional[pulumi.Input['ExternalProtectionLevelOptionsArgs']] = None,
                 state: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a CryptoKeyVersion resource.
        :param pulumi.Input['ExternalProtectionLevelOptionsArgs'] external_protection_level_options: ExternalProtectionLevelOptions stores a group of additional fields for configuring a CryptoKeyVersion that are specific to the EXTERNAL protection level.
        :param pulumi.Input[str] state: The current state of the CryptoKeyVersion.
        """
        pulumi.set(__self__, "crypto_key_id", crypto_key_id)
        pulumi.set(__self__, "key_ring_id", key_ring_id)
        pulumi.set(__self__, "location", location)
        pulumi.set(__self__, "project", project)
        if external_protection_level_options is not None:
            pulumi.set(__self__, "external_protection_level_options", external_protection_level_options)
        if state is not None:
            pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter(name="cryptoKeyId")
    def crypto_key_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "crypto_key_id")

    @crypto_key_id.setter
    def crypto_key_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "crypto_key_id", value)

    @property
    @pulumi.getter(name="keyRingId")
    def key_ring_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key_ring_id")

    @key_ring_id.setter
    def key_ring_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_ring_id", value)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Input[str]:
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: pulumi.Input[str]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def project(self) -> pulumi.Input[str]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: pulumi.Input[str]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="externalProtectionLevelOptions")
    def external_protection_level_options(self) -> Optional[pulumi.Input['ExternalProtectionLevelOptionsArgs']]:
        """
        ExternalProtectionLevelOptions stores a group of additional fields for configuring a CryptoKeyVersion that are specific to the EXTERNAL protection level.
        """
        return pulumi.get(self, "external_protection_level_options")

    @external_protection_level_options.setter
    def external_protection_level_options(self, value: Optional[pulumi.Input['ExternalProtectionLevelOptionsArgs']]):
        pulumi.set(self, "external_protection_level_options", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        The current state of the CryptoKeyVersion.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)


class CryptoKeyVersion(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 crypto_key_id: Optional[pulumi.Input[str]] = None,
                 external_protection_level_options: Optional[pulumi.Input[pulumi.InputType['ExternalProtectionLevelOptionsArgs']]] = None,
                 key_ring_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a new CryptoKeyVersion in a CryptoKey. The server will assign the next sequential id. If unset, state will be set to ENABLED.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ExternalProtectionLevelOptionsArgs']] external_protection_level_options: ExternalProtectionLevelOptions stores a group of additional fields for configuring a CryptoKeyVersion that are specific to the EXTERNAL protection level.
        :param pulumi.Input[str] state: The current state of the CryptoKeyVersion.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CryptoKeyVersionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a new CryptoKeyVersion in a CryptoKey. The server will assign the next sequential id. If unset, state will be set to ENABLED.

        :param str resource_name: The name of the resource.
        :param CryptoKeyVersionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CryptoKeyVersionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 crypto_key_id: Optional[pulumi.Input[str]] = None,
                 external_protection_level_options: Optional[pulumi.Input[pulumi.InputType['ExternalProtectionLevelOptionsArgs']]] = None,
                 key_ring_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
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
            __props__ = CryptoKeyVersionArgs.__new__(CryptoKeyVersionArgs)

            if crypto_key_id is None and not opts.urn:
                raise TypeError("Missing required property 'crypto_key_id'")
            __props__.__dict__["crypto_key_id"] = crypto_key_id
            __props__.__dict__["external_protection_level_options"] = external_protection_level_options
            if key_ring_id is None and not opts.urn:
                raise TypeError("Missing required property 'key_ring_id'")
            __props__.__dict__["key_ring_id"] = key_ring_id
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__.__dict__["location"] = location
            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            __props__.__dict__["state"] = state
            __props__.__dict__["algorithm"] = None
            __props__.__dict__["attestation"] = None
            __props__.__dict__["create_time"] = None
            __props__.__dict__["destroy_event_time"] = None
            __props__.__dict__["destroy_time"] = None
            __props__.__dict__["generate_time"] = None
            __props__.__dict__["import_failure_reason"] = None
            __props__.__dict__["import_job"] = None
            __props__.__dict__["import_time"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["protection_level"] = None
        super(CryptoKeyVersion, __self__).__init__(
            'google-native:cloudkms/v1:CryptoKeyVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'CryptoKeyVersion':
        """
        Get an existing CryptoKeyVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = CryptoKeyVersionArgs.__new__(CryptoKeyVersionArgs)

        __props__.__dict__["algorithm"] = None
        __props__.__dict__["attestation"] = None
        __props__.__dict__["create_time"] = None
        __props__.__dict__["destroy_event_time"] = None
        __props__.__dict__["destroy_time"] = None
        __props__.__dict__["external_protection_level_options"] = None
        __props__.__dict__["generate_time"] = None
        __props__.__dict__["import_failure_reason"] = None
        __props__.__dict__["import_job"] = None
        __props__.__dict__["import_time"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["protection_level"] = None
        __props__.__dict__["state"] = None
        return CryptoKeyVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def algorithm(self) -> pulumi.Output[str]:
        """
        The CryptoKeyVersionAlgorithm that this CryptoKeyVersion supports.
        """
        return pulumi.get(self, "algorithm")

    @property
    @pulumi.getter
    def attestation(self) -> pulumi.Output['outputs.KeyOperationAttestationResponse']:
        """
        Statement that was generated and signed by the HSM at key creation time. Use this statement to verify attributes of the key as stored on the HSM, independently of Google. Only provided for key versions with protection_level HSM.
        """
        return pulumi.get(self, "attestation")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The time at which this CryptoKeyVersion was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="destroyEventTime")
    def destroy_event_time(self) -> pulumi.Output[str]:
        """
        The time this CryptoKeyVersion's key material was destroyed. Only present if state is DESTROYED.
        """
        return pulumi.get(self, "destroy_event_time")

    @property
    @pulumi.getter(name="destroyTime")
    def destroy_time(self) -> pulumi.Output[str]:
        """
        The time this CryptoKeyVersion's key material is scheduled for destruction. Only present if state is DESTROY_SCHEDULED.
        """
        return pulumi.get(self, "destroy_time")

    @property
    @pulumi.getter(name="externalProtectionLevelOptions")
    def external_protection_level_options(self) -> pulumi.Output['outputs.ExternalProtectionLevelOptionsResponse']:
        """
        ExternalProtectionLevelOptions stores a group of additional fields for configuring a CryptoKeyVersion that are specific to the EXTERNAL protection level.
        """
        return pulumi.get(self, "external_protection_level_options")

    @property
    @pulumi.getter(name="generateTime")
    def generate_time(self) -> pulumi.Output[str]:
        """
        The time this CryptoKeyVersion's key material was generated.
        """
        return pulumi.get(self, "generate_time")

    @property
    @pulumi.getter(name="importFailureReason")
    def import_failure_reason(self) -> pulumi.Output[str]:
        """
        The root cause of an import failure. Only present if state is IMPORT_FAILED.
        """
        return pulumi.get(self, "import_failure_reason")

    @property
    @pulumi.getter(name="importJob")
    def import_job(self) -> pulumi.Output[str]:
        """
        The name of the ImportJob used to import this CryptoKeyVersion. Only present if the underlying key material was imported.
        """
        return pulumi.get(self, "import_job")

    @property
    @pulumi.getter(name="importTime")
    def import_time(self) -> pulumi.Output[str]:
        """
        The time at which this CryptoKeyVersion's key material was imported.
        """
        return pulumi.get(self, "import_time")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name for this CryptoKeyVersion in the format `projects/*/locations/*/keyRings/*/cryptoKeys/*/cryptoKeyVersions/*`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="protectionLevel")
    def protection_level(self) -> pulumi.Output[str]:
        """
        The ProtectionLevel describing how crypto operations are performed with this CryptoKeyVersion.
        """
        return pulumi.get(self, "protection_level")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current state of the CryptoKeyVersion.
        """
        return pulumi.get(self, "state")

