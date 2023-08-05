# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = ['ChannelArgs', 'Channel']

@pulumi.input_type
class ChannelArgs:
    def __init__(__self__, *,
                 channel_id: pulumi.Input[str],
                 project: pulumi.Input[str],
                 site_id: pulumi.Input[str],
                 expire_time: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 retained_release_count: Optional[pulumi.Input[int]] = None,
                 ttl: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Channel resource.
        :param pulumi.Input[str] expire_time: The time at which the channel will be automatically deleted. If null, the channel will not be automatically deleted. This field is present in the output whether it's set directly or via the `ttl` field.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Text labels used for extra metadata and/or filtering.
        :param pulumi.Input[str] name: The fully-qualified resource name for the channel, in the format: sites/ SITE_ID/channels/CHANNEL_ID
        :param pulumi.Input[int] retained_release_count: The number of previous releases to retain on the channel for rollback or other purposes. Must be a number between 1-100. Defaults to 10 for new channels.
        :param pulumi.Input[str] ttl: Input only. A time-to-live for this channel. Sets `expire_time` to the provided duration past the time of the request.
        """
        pulumi.set(__self__, "channel_id", channel_id)
        pulumi.set(__self__, "project", project)
        pulumi.set(__self__, "site_id", site_id)
        if expire_time is not None:
            pulumi.set(__self__, "expire_time", expire_time)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if retained_release_count is not None:
            pulumi.set(__self__, "retained_release_count", retained_release_count)
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)

    @property
    @pulumi.getter(name="channelId")
    def channel_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "channel_id")

    @channel_id.setter
    def channel_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "channel_id", value)

    @property
    @pulumi.getter
    def project(self) -> pulumi.Input[str]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: pulumi.Input[str]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="siteId")
    def site_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "site_id")

    @site_id.setter
    def site_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "site_id", value)

    @property
    @pulumi.getter(name="expireTime")
    def expire_time(self) -> Optional[pulumi.Input[str]]:
        """
        The time at which the channel will be automatically deleted. If null, the channel will not be automatically deleted. This field is present in the output whether it's set directly or via the `ttl` field.
        """
        return pulumi.get(self, "expire_time")

    @expire_time.setter
    def expire_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expire_time", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Text labels used for extra metadata and/or filtering.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The fully-qualified resource name for the channel, in the format: sites/ SITE_ID/channels/CHANNEL_ID
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="retainedReleaseCount")
    def retained_release_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of previous releases to retain on the channel for rollback or other purposes. Must be a number between 1-100. Defaults to 10 for new channels.
        """
        return pulumi.get(self, "retained_release_count")

    @retained_release_count.setter
    def retained_release_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "retained_release_count", value)

    @property
    @pulumi.getter
    def ttl(self) -> Optional[pulumi.Input[str]]:
        """
        Input only. A time-to-live for this channel. Sets `expire_time` to the provided duration past the time of the request.
        """
        return pulumi.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ttl", value)


class Channel(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 channel_id: Optional[pulumi.Input[str]] = None,
                 expire_time: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 retained_release_count: Optional[pulumi.Input[int]] = None,
                 site_id: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a new channel in the specified site.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] expire_time: The time at which the channel will be automatically deleted. If null, the channel will not be automatically deleted. This field is present in the output whether it's set directly or via the `ttl` field.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Text labels used for extra metadata and/or filtering.
        :param pulumi.Input[str] name: The fully-qualified resource name for the channel, in the format: sites/ SITE_ID/channels/CHANNEL_ID
        :param pulumi.Input[int] retained_release_count: The number of previous releases to retain on the channel for rollback or other purposes. Must be a number between 1-100. Defaults to 10 for new channels.
        :param pulumi.Input[str] ttl: Input only. A time-to-live for this channel. Sets `expire_time` to the provided duration past the time of the request.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ChannelArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a new channel in the specified site.

        :param str resource_name: The name of the resource.
        :param ChannelArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ChannelArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 channel_id: Optional[pulumi.Input[str]] = None,
                 expire_time: Optional[pulumi.Input[str]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 retained_release_count: Optional[pulumi.Input[int]] = None,
                 site_id: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[str]] = None,
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
            __props__ = ChannelArgs.__new__(ChannelArgs)

            if channel_id is None and not opts.urn:
                raise TypeError("Missing required property 'channel_id'")
            __props__.__dict__["channel_id"] = channel_id
            __props__.__dict__["expire_time"] = expire_time
            __props__.__dict__["labels"] = labels
            __props__.__dict__["name"] = name
            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            __props__.__dict__["retained_release_count"] = retained_release_count
            if site_id is None and not opts.urn:
                raise TypeError("Missing required property 'site_id'")
            __props__.__dict__["site_id"] = site_id
            __props__.__dict__["ttl"] = ttl
            __props__.__dict__["create_time"] = None
            __props__.__dict__["release"] = None
            __props__.__dict__["update_time"] = None
            __props__.__dict__["url"] = None
        super(Channel, __self__).__init__(
            'google-native:firebasehosting/v1beta1:Channel',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Channel':
        """
        Get an existing Channel resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ChannelArgs.__new__(ChannelArgs)

        __props__.__dict__["create_time"] = None
        __props__.__dict__["expire_time"] = None
        __props__.__dict__["labels"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["release"] = None
        __props__.__dict__["retained_release_count"] = None
        __props__.__dict__["ttl"] = None
        __props__.__dict__["update_time"] = None
        __props__.__dict__["url"] = None
        return Channel(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The time at which the channel was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="expireTime")
    def expire_time(self) -> pulumi.Output[str]:
        """
        The time at which the channel will be automatically deleted. If null, the channel will not be automatically deleted. This field is present in the output whether it's set directly or via the `ttl` field.
        """
        return pulumi.get(self, "expire_time")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Text labels used for extra metadata and/or filtering.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The fully-qualified resource name for the channel, in the format: sites/ SITE_ID/channels/CHANNEL_ID
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def release(self) -> pulumi.Output['outputs.ReleaseResponse']:
        """
        The current release for the channel, if any.
        """
        return pulumi.get(self, "release")

    @property
    @pulumi.getter(name="retainedReleaseCount")
    def retained_release_count(self) -> pulumi.Output[int]:
        """
        The number of previous releases to retain on the channel for rollback or other purposes. Must be a number between 1-100. Defaults to 10 for new channels.
        """
        return pulumi.get(self, "retained_release_count")

    @property
    @pulumi.getter
    def ttl(self) -> pulumi.Output[str]:
        """
        Input only. A time-to-live for this channel. Sets `expire_time` to the provided duration past the time of the request.
        """
        return pulumi.get(self, "ttl")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> pulumi.Output[str]:
        """
        The time at which the channel was last updated.
        """
        return pulumi.get(self, "update_time")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[str]:
        """
        The URL at which the content of this channel's current release can be viewed. This URL is a Firebase-provided subdomain of `web.app`. The content of this channel's current release can also be viewed at the Firebase-provided subdomain of `firebaseapp.com`. If this channel is the `live` channel for the Hosting site, then the content of this channel's current release can also be viewed at any connected custom domains.
        """
        return pulumi.get(self, "url")

