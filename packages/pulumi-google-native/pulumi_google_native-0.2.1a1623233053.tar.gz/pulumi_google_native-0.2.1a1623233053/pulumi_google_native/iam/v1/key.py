# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['KeyArgs', 'Key']

@pulumi.input_type
class KeyArgs:
    def __init__(__self__, *,
                 project: pulumi.Input[str],
                 service_account_id: pulumi.Input[str],
                 key_algorithm: Optional[pulumi.Input[str]] = None,
                 private_key_type: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Key resource.
        :param pulumi.Input[str] key_algorithm: Which type of key and algorithm to use for the key. The default is currently a 2K RSA key. However this may change in the future.
        :param pulumi.Input[str] private_key_type: The output format of the private key. The default value is `TYPE_GOOGLE_CREDENTIALS_FILE`, which is the Google Credentials File format.
        """
        pulumi.set(__self__, "project", project)
        pulumi.set(__self__, "service_account_id", service_account_id)
        if key_algorithm is not None:
            pulumi.set(__self__, "key_algorithm", key_algorithm)
        if private_key_type is not None:
            pulumi.set(__self__, "private_key_type", private_key_type)

    @property
    @pulumi.getter
    def project(self) -> pulumi.Input[str]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: pulumi.Input[str]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="serviceAccountId")
    def service_account_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "service_account_id")

    @service_account_id.setter
    def service_account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_account_id", value)

    @property
    @pulumi.getter(name="keyAlgorithm")
    def key_algorithm(self) -> Optional[pulumi.Input[str]]:
        """
        Which type of key and algorithm to use for the key. The default is currently a 2K RSA key. However this may change in the future.
        """
        return pulumi.get(self, "key_algorithm")

    @key_algorithm.setter
    def key_algorithm(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_algorithm", value)

    @property
    @pulumi.getter(name="privateKeyType")
    def private_key_type(self) -> Optional[pulumi.Input[str]]:
        """
        The output format of the private key. The default value is `TYPE_GOOGLE_CREDENTIALS_FILE`, which is the Google Credentials File format.
        """
        return pulumi.get(self, "private_key_type")

    @private_key_type.setter
    def private_key_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_key_type", value)


class Key(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 key_algorithm: Optional[pulumi.Input[str]] = None,
                 private_key_type: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service_account_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a ServiceAccountKey.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] key_algorithm: Which type of key and algorithm to use for the key. The default is currently a 2K RSA key. However this may change in the future.
        :param pulumi.Input[str] private_key_type: The output format of the private key. The default value is `TYPE_GOOGLE_CREDENTIALS_FILE`, which is the Google Credentials File format.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: KeyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a ServiceAccountKey.

        :param str resource_name: The name of the resource.
        :param KeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 key_algorithm: Optional[pulumi.Input[str]] = None,
                 private_key_type: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 service_account_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = KeyArgs.__new__(KeyArgs)

            __props__.__dict__["key_algorithm"] = key_algorithm
            __props__.__dict__["private_key_type"] = private_key_type
            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            if service_account_id is None and not opts.urn:
                raise TypeError("Missing required property 'service_account_id'")
            __props__.__dict__["service_account_id"] = service_account_id
            __props__.__dict__["key_origin"] = None
            __props__.__dict__["key_type"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["private_key_data"] = None
            __props__.__dict__["public_key_data"] = None
            __props__.__dict__["valid_after_time"] = None
            __props__.__dict__["valid_before_time"] = None
        super(Key, __self__).__init__(
            'google-native:iam/v1:Key',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Key':
        """
        Get an existing Key resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = KeyArgs.__new__(KeyArgs)

        __props__.__dict__["key_algorithm"] = None
        __props__.__dict__["key_origin"] = None
        __props__.__dict__["key_type"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["private_key_data"] = None
        __props__.__dict__["private_key_type"] = None
        __props__.__dict__["public_key_data"] = None
        __props__.__dict__["valid_after_time"] = None
        __props__.__dict__["valid_before_time"] = None
        return Key(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="keyAlgorithm")
    def key_algorithm(self) -> pulumi.Output[str]:
        """
        Specifies the algorithm (and possibly key size) for the key.
        """
        return pulumi.get(self, "key_algorithm")

    @property
    @pulumi.getter(name="keyOrigin")
    def key_origin(self) -> pulumi.Output[str]:
        """
        The key origin.
        """
        return pulumi.get(self, "key_origin")

    @property
    @pulumi.getter(name="keyType")
    def key_type(self) -> pulumi.Output[str]:
        """
        The key type.
        """
        return pulumi.get(self, "key_type")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name of the service account key in the following format `projects/{PROJECT_ID}/serviceAccounts/{ACCOUNT}/keys/{key}`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateKeyData")
    def private_key_data(self) -> pulumi.Output[str]:
        """
        The private key data. Only provided in `CreateServiceAccountKey` responses. Make sure to keep the private key data secure because it allows for the assertion of the service account identity. When base64 decoded, the private key data can be used to authenticate with Google API client libraries and with gcloud auth activate-service-account.
        """
        return pulumi.get(self, "private_key_data")

    @property
    @pulumi.getter(name="privateKeyType")
    def private_key_type(self) -> pulumi.Output[str]:
        """
        The output format for the private key. Only provided in `CreateServiceAccountKey` responses, not in `GetServiceAccountKey` or `ListServiceAccountKey` responses. Google never exposes system-managed private keys, and never retains user-managed private keys.
        """
        return pulumi.get(self, "private_key_type")

    @property
    @pulumi.getter(name="publicKeyData")
    def public_key_data(self) -> pulumi.Output[str]:
        """
        The public key data. Only provided in `GetServiceAccountKey` responses.
        """
        return pulumi.get(self, "public_key_data")

    @property
    @pulumi.getter(name="validAfterTime")
    def valid_after_time(self) -> pulumi.Output[str]:
        """
        The key can be used after this timestamp.
        """
        return pulumi.get(self, "valid_after_time")

    @property
    @pulumi.getter(name="validBeforeTime")
    def valid_before_time(self) -> pulumi.Output[str]:
        """
        The key can be used before this timestamp. For system-managed key pairs, this timestamp is the end time for the private key signing operation. The public key could still be used for verification for a few hours after this time.
        """
        return pulumi.get(self, "valid_before_time")

