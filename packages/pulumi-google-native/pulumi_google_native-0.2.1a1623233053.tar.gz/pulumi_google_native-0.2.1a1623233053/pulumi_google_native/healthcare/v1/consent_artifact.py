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

__all__ = ['ConsentArtifactArgs', 'ConsentArtifact']

@pulumi.input_type
class ConsentArtifactArgs:
    def __init__(__self__, *,
                 consent_store_id: pulumi.Input[str],
                 dataset_id: pulumi.Input[str],
                 location: pulumi.Input[str],
                 project: pulumi.Input[str],
                 consent_content_screenshots: Optional[pulumi.Input[Sequence[pulumi.Input['ImageArgs']]]] = None,
                 consent_content_version: Optional[pulumi.Input[str]] = None,
                 guardian_signature: Optional[pulumi.Input['SignatureArgs']] = None,
                 metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 user_signature: Optional[pulumi.Input['SignatureArgs']] = None,
                 witness_signature: Optional[pulumi.Input['SignatureArgs']] = None):
        """
        The set of arguments for constructing a ConsentArtifact resource.
        :param pulumi.Input[Sequence[pulumi.Input['ImageArgs']]] consent_content_screenshots: Optional. Screenshots, PDFs, or other binary information documenting the user's consent.
        :param pulumi.Input[str] consent_content_version: Optional. An string indicating the version of the consent information shown to the user.
        :param pulumi.Input['SignatureArgs'] guardian_signature: Optional. A signature from a guardian.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] metadata: Optional. Metadata associated with the Consent artifact. For example, the consent locale or user agent version.
        :param pulumi.Input[str] name: Resource name of the Consent artifact, of the form `projects/{project_id}/locations/{location_id}/datasets/{dataset_id}/consentStores/{consent_store_id}/consentArtifacts/{consent_artifact_id}`. Cannot be changed after creation.
        :param pulumi.Input[str] user_id: Required. User's UUID provided by the client.
        :param pulumi.Input['SignatureArgs'] user_signature: Optional. User's signature.
        :param pulumi.Input['SignatureArgs'] witness_signature: Optional. A signature from a witness.
        """
        pulumi.set(__self__, "consent_store_id", consent_store_id)
        pulumi.set(__self__, "dataset_id", dataset_id)
        pulumi.set(__self__, "location", location)
        pulumi.set(__self__, "project", project)
        if consent_content_screenshots is not None:
            pulumi.set(__self__, "consent_content_screenshots", consent_content_screenshots)
        if consent_content_version is not None:
            pulumi.set(__self__, "consent_content_version", consent_content_version)
        if guardian_signature is not None:
            pulumi.set(__self__, "guardian_signature", guardian_signature)
        if metadata is not None:
            pulumi.set(__self__, "metadata", metadata)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if user_id is not None:
            pulumi.set(__self__, "user_id", user_id)
        if user_signature is not None:
            pulumi.set(__self__, "user_signature", user_signature)
        if witness_signature is not None:
            pulumi.set(__self__, "witness_signature", witness_signature)

    @property
    @pulumi.getter(name="consentStoreId")
    def consent_store_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "consent_store_id")

    @consent_store_id.setter
    def consent_store_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "consent_store_id", value)

    @property
    @pulumi.getter(name="datasetId")
    def dataset_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "dataset_id")

    @dataset_id.setter
    def dataset_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "dataset_id", value)

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
    @pulumi.getter(name="consentContentScreenshots")
    def consent_content_screenshots(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ImageArgs']]]]:
        """
        Optional. Screenshots, PDFs, or other binary information documenting the user's consent.
        """
        return pulumi.get(self, "consent_content_screenshots")

    @consent_content_screenshots.setter
    def consent_content_screenshots(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ImageArgs']]]]):
        pulumi.set(self, "consent_content_screenshots", value)

    @property
    @pulumi.getter(name="consentContentVersion")
    def consent_content_version(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. An string indicating the version of the consent information shown to the user.
        """
        return pulumi.get(self, "consent_content_version")

    @consent_content_version.setter
    def consent_content_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "consent_content_version", value)

    @property
    @pulumi.getter(name="guardianSignature")
    def guardian_signature(self) -> Optional[pulumi.Input['SignatureArgs']]:
        """
        Optional. A signature from a guardian.
        """
        return pulumi.get(self, "guardian_signature")

    @guardian_signature.setter
    def guardian_signature(self, value: Optional[pulumi.Input['SignatureArgs']]):
        pulumi.set(self, "guardian_signature", value)

    @property
    @pulumi.getter
    def metadata(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Optional. Metadata associated with the Consent artifact. For example, the consent locale or user agent version.
        """
        return pulumi.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "metadata", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Resource name of the Consent artifact, of the form `projects/{project_id}/locations/{location_id}/datasets/{dataset_id}/consentStores/{consent_store_id}/consentArtifacts/{consent_artifact_id}`. Cannot be changed after creation.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> Optional[pulumi.Input[str]]:
        """
        Required. User's UUID provided by the client.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_id", value)

    @property
    @pulumi.getter(name="userSignature")
    def user_signature(self) -> Optional[pulumi.Input['SignatureArgs']]:
        """
        Optional. User's signature.
        """
        return pulumi.get(self, "user_signature")

    @user_signature.setter
    def user_signature(self, value: Optional[pulumi.Input['SignatureArgs']]):
        pulumi.set(self, "user_signature", value)

    @property
    @pulumi.getter(name="witnessSignature")
    def witness_signature(self) -> Optional[pulumi.Input['SignatureArgs']]:
        """
        Optional. A signature from a witness.
        """
        return pulumi.get(self, "witness_signature")

    @witness_signature.setter
    def witness_signature(self, value: Optional[pulumi.Input['SignatureArgs']]):
        pulumi.set(self, "witness_signature", value)


class ConsentArtifact(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 consent_content_screenshots: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageArgs']]]]] = None,
                 consent_content_version: Optional[pulumi.Input[str]] = None,
                 consent_store_id: Optional[pulumi.Input[str]] = None,
                 dataset_id: Optional[pulumi.Input[str]] = None,
                 guardian_signature: Optional[pulumi.Input[pulumi.InputType['SignatureArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 user_signature: Optional[pulumi.Input[pulumi.InputType['SignatureArgs']]] = None,
                 witness_signature: Optional[pulumi.Input[pulumi.InputType['SignatureArgs']]] = None,
                 __props__=None):
        """
        Creates a new Consent artifact in the parent consent store.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageArgs']]]] consent_content_screenshots: Optional. Screenshots, PDFs, or other binary information documenting the user's consent.
        :param pulumi.Input[str] consent_content_version: Optional. An string indicating the version of the consent information shown to the user.
        :param pulumi.Input[pulumi.InputType['SignatureArgs']] guardian_signature: Optional. A signature from a guardian.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] metadata: Optional. Metadata associated with the Consent artifact. For example, the consent locale or user agent version.
        :param pulumi.Input[str] name: Resource name of the Consent artifact, of the form `projects/{project_id}/locations/{location_id}/datasets/{dataset_id}/consentStores/{consent_store_id}/consentArtifacts/{consent_artifact_id}`. Cannot be changed after creation.
        :param pulumi.Input[str] user_id: Required. User's UUID provided by the client.
        :param pulumi.Input[pulumi.InputType['SignatureArgs']] user_signature: Optional. User's signature.
        :param pulumi.Input[pulumi.InputType['SignatureArgs']] witness_signature: Optional. A signature from a witness.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConsentArtifactArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a new Consent artifact in the parent consent store.

        :param str resource_name: The name of the resource.
        :param ConsentArtifactArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConsentArtifactArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 consent_content_screenshots: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageArgs']]]]] = None,
                 consent_content_version: Optional[pulumi.Input[str]] = None,
                 consent_store_id: Optional[pulumi.Input[str]] = None,
                 dataset_id: Optional[pulumi.Input[str]] = None,
                 guardian_signature: Optional[pulumi.Input[pulumi.InputType['SignatureArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 user_signature: Optional[pulumi.Input[pulumi.InputType['SignatureArgs']]] = None,
                 witness_signature: Optional[pulumi.Input[pulumi.InputType['SignatureArgs']]] = None,
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
            __props__ = ConsentArtifactArgs.__new__(ConsentArtifactArgs)

            __props__.__dict__["consent_content_screenshots"] = consent_content_screenshots
            __props__.__dict__["consent_content_version"] = consent_content_version
            if consent_store_id is None and not opts.urn:
                raise TypeError("Missing required property 'consent_store_id'")
            __props__.__dict__["consent_store_id"] = consent_store_id
            if dataset_id is None and not opts.urn:
                raise TypeError("Missing required property 'dataset_id'")
            __props__.__dict__["dataset_id"] = dataset_id
            __props__.__dict__["guardian_signature"] = guardian_signature
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__.__dict__["location"] = location
            __props__.__dict__["metadata"] = metadata
            __props__.__dict__["name"] = name
            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            __props__.__dict__["user_id"] = user_id
            __props__.__dict__["user_signature"] = user_signature
            __props__.__dict__["witness_signature"] = witness_signature
        super(ConsentArtifact, __self__).__init__(
            'google-native:healthcare/v1:ConsentArtifact',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ConsentArtifact':
        """
        Get an existing ConsentArtifact resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ConsentArtifactArgs.__new__(ConsentArtifactArgs)

        __props__.__dict__["consent_content_screenshots"] = None
        __props__.__dict__["consent_content_version"] = None
        __props__.__dict__["guardian_signature"] = None
        __props__.__dict__["metadata"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["user_id"] = None
        __props__.__dict__["user_signature"] = None
        __props__.__dict__["witness_signature"] = None
        return ConsentArtifact(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="consentContentScreenshots")
    def consent_content_screenshots(self) -> pulumi.Output[Sequence['outputs.ImageResponse']]:
        """
        Optional. Screenshots, PDFs, or other binary information documenting the user's consent.
        """
        return pulumi.get(self, "consent_content_screenshots")

    @property
    @pulumi.getter(name="consentContentVersion")
    def consent_content_version(self) -> pulumi.Output[str]:
        """
        Optional. An string indicating the version of the consent information shown to the user.
        """
        return pulumi.get(self, "consent_content_version")

    @property
    @pulumi.getter(name="guardianSignature")
    def guardian_signature(self) -> pulumi.Output['outputs.SignatureResponse']:
        """
        Optional. A signature from a guardian.
        """
        return pulumi.get(self, "guardian_signature")

    @property
    @pulumi.getter
    def metadata(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Optional. Metadata associated with the Consent artifact. For example, the consent locale or user agent version.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name of the Consent artifact, of the form `projects/{project_id}/locations/{location_id}/datasets/{dataset_id}/consentStores/{consent_store_id}/consentArtifacts/{consent_artifact_id}`. Cannot be changed after creation.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Output[str]:
        """
        Required. User's UUID provided by the client.
        """
        return pulumi.get(self, "user_id")

    @property
    @pulumi.getter(name="userSignature")
    def user_signature(self) -> pulumi.Output['outputs.SignatureResponse']:
        """
        Optional. User's signature.
        """
        return pulumi.get(self, "user_signature")

    @property
    @pulumi.getter(name="witnessSignature")
    def witness_signature(self) -> pulumi.Output['outputs.SignatureResponse']:
        """
        Optional. A signature from a witness.
        """
        return pulumi.get(self, "witness_signature")

