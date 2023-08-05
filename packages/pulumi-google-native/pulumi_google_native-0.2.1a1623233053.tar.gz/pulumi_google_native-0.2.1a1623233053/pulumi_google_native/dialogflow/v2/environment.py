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

__all__ = ['EnvironmentArgs', 'Environment']

@pulumi.input_type
class EnvironmentArgs:
    def __init__(__self__, *,
                 environment_id: pulumi.Input[str],
                 location: pulumi.Input[str],
                 project: pulumi.Input[str],
                 agent_version: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 fulfillment: Optional[pulumi.Input['GoogleCloudDialogflowV2FulfillmentArgs']] = None,
                 text_to_speech_settings: Optional[pulumi.Input['GoogleCloudDialogflowV2TextToSpeechSettingsArgs']] = None):
        """
        The set of arguments for constructing a Environment resource.
        :param pulumi.Input[str] agent_version: Optional. The agent version loaded into this environment. Supported formats: - `projects//agent/versions/` - `projects//locations//agent/versions/`
        :param pulumi.Input[str] description: Optional. The developer-provided description for this environment. The maximum length is 500 characters. If exceeded, the request is rejected.
        :param pulumi.Input['GoogleCloudDialogflowV2FulfillmentArgs'] fulfillment: Optional. The fulfillment settings to use for this environment.
        :param pulumi.Input['GoogleCloudDialogflowV2TextToSpeechSettingsArgs'] text_to_speech_settings: Optional. Text to speech settings for this environment.
        """
        pulumi.set(__self__, "environment_id", environment_id)
        pulumi.set(__self__, "location", location)
        pulumi.set(__self__, "project", project)
        if agent_version is not None:
            pulumi.set(__self__, "agent_version", agent_version)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if fulfillment is not None:
            pulumi.set(__self__, "fulfillment", fulfillment)
        if text_to_speech_settings is not None:
            pulumi.set(__self__, "text_to_speech_settings", text_to_speech_settings)

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "environment_id")

    @environment_id.setter
    def environment_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "environment_id", value)

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
    @pulumi.getter(name="agentVersion")
    def agent_version(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. The agent version loaded into this environment. Supported formats: - `projects//agent/versions/` - `projects//locations//agent/versions/`
        """
        return pulumi.get(self, "agent_version")

    @agent_version.setter
    def agent_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "agent_version", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. The developer-provided description for this environment. The maximum length is 500 characters. If exceeded, the request is rejected.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def fulfillment(self) -> Optional[pulumi.Input['GoogleCloudDialogflowV2FulfillmentArgs']]:
        """
        Optional. The fulfillment settings to use for this environment.
        """
        return pulumi.get(self, "fulfillment")

    @fulfillment.setter
    def fulfillment(self, value: Optional[pulumi.Input['GoogleCloudDialogflowV2FulfillmentArgs']]):
        pulumi.set(self, "fulfillment", value)

    @property
    @pulumi.getter(name="textToSpeechSettings")
    def text_to_speech_settings(self) -> Optional[pulumi.Input['GoogleCloudDialogflowV2TextToSpeechSettingsArgs']]:
        """
        Optional. Text to speech settings for this environment.
        """
        return pulumi.get(self, "text_to_speech_settings")

    @text_to_speech_settings.setter
    def text_to_speech_settings(self, value: Optional[pulumi.Input['GoogleCloudDialogflowV2TextToSpeechSettingsArgs']]):
        pulumi.set(self, "text_to_speech_settings", value)


class Environment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_version: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 environment_id: Optional[pulumi.Input[str]] = None,
                 fulfillment: Optional[pulumi.Input[pulumi.InputType['GoogleCloudDialogflowV2FulfillmentArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 text_to_speech_settings: Optional[pulumi.Input[pulumi.InputType['GoogleCloudDialogflowV2TextToSpeechSettingsArgs']]] = None,
                 __props__=None):
        """
        Creates an agent environment.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] agent_version: Optional. The agent version loaded into this environment. Supported formats: - `projects//agent/versions/` - `projects//locations//agent/versions/`
        :param pulumi.Input[str] description: Optional. The developer-provided description for this environment. The maximum length is 500 characters. If exceeded, the request is rejected.
        :param pulumi.Input[pulumi.InputType['GoogleCloudDialogflowV2FulfillmentArgs']] fulfillment: Optional. The fulfillment settings to use for this environment.
        :param pulumi.Input[pulumi.InputType['GoogleCloudDialogflowV2TextToSpeechSettingsArgs']] text_to_speech_settings: Optional. Text to speech settings for this environment.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EnvironmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates an agent environment.

        :param str resource_name: The name of the resource.
        :param EnvironmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EnvironmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_version: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 environment_id: Optional[pulumi.Input[str]] = None,
                 fulfillment: Optional[pulumi.Input[pulumi.InputType['GoogleCloudDialogflowV2FulfillmentArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 text_to_speech_settings: Optional[pulumi.Input[pulumi.InputType['GoogleCloudDialogflowV2TextToSpeechSettingsArgs']]] = None,
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
            __props__ = EnvironmentArgs.__new__(EnvironmentArgs)

            __props__.__dict__["agent_version"] = agent_version
            __props__.__dict__["description"] = description
            if environment_id is None and not opts.urn:
                raise TypeError("Missing required property 'environment_id'")
            __props__.__dict__["environment_id"] = environment_id
            __props__.__dict__["fulfillment"] = fulfillment
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__.__dict__["location"] = location
            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            __props__.__dict__["text_to_speech_settings"] = text_to_speech_settings
            __props__.__dict__["name"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["update_time"] = None
        super(Environment, __self__).__init__(
            'google-native:dialogflow/v2:Environment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Environment':
        """
        Get an existing Environment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = EnvironmentArgs.__new__(EnvironmentArgs)

        __props__.__dict__["agent_version"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["fulfillment"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["text_to_speech_settings"] = None
        __props__.__dict__["update_time"] = None
        return Environment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="agentVersion")
    def agent_version(self) -> pulumi.Output[str]:
        """
        Optional. The agent version loaded into this environment. Supported formats: - `projects//agent/versions/` - `projects//locations//agent/versions/`
        """
        return pulumi.get(self, "agent_version")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Optional. The developer-provided description for this environment. The maximum length is 500 characters. If exceeded, the request is rejected.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def fulfillment(self) -> pulumi.Output['outputs.GoogleCloudDialogflowV2FulfillmentResponse']:
        """
        Optional. The fulfillment settings to use for this environment.
        """
        return pulumi.get(self, "fulfillment")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The unique identifier of this agent environment. Supported formats: - `projects//agent/environments/` - `projects//locations//agent/environments/`
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The state of this environment. This field is read-only, i.e., it cannot be set by create and update methods.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="textToSpeechSettings")
    def text_to_speech_settings(self) -> pulumi.Output['outputs.GoogleCloudDialogflowV2TextToSpeechSettingsResponse']:
        """
        Optional. Text to speech settings for this environment.
        """
        return pulumi.get(self, "text_to_speech_settings")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        The last update time of this environment. This field is read-only, i.e., it cannot be set by create and update methods.
        """
        return pulumi.get(self, "update_time")

