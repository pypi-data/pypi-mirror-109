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

__all__ = ['JobArgs', 'Job']

@pulumi.input_type
class JobArgs:
    def __init__(__self__, *,
                 location: pulumi.Input[str],
                 project: pulumi.Input[str],
                 config: Optional[pulumi.Input['JobConfigArgs']] = None,
                 input_uri: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 output_uri: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 template_id: Optional[pulumi.Input[str]] = None,
                 ttl_after_completion_days: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a Job resource.
        :param pulumi.Input['JobConfigArgs'] config: The configuration for this job.
        :param pulumi.Input[str] input_uri: Input only. Specify the `input_uri` to populate empty `uri` fields in each element of `Job.config.inputs` or `JobTemplate.config.inputs` when using template. URI of the media. Input files must be at least 5 seconds in duration and stored in Cloud Storage (for example, `gs://bucket/inputs/file.mp4`).
        :param pulumi.Input[str] name: The resource name of the job. Format: `projects/{project}/locations/{location}/jobs/{job}`
        :param pulumi.Input[str] output_uri: Input only. Specify the `output_uri` to populate an empty `Job.config.output.uri` or `JobTemplate.config.output.uri` when using template. URI for the output file(s). For example, `gs://my-bucket/outputs/`.
        :param pulumi.Input[int] priority: Specify the priority of the job. Enter a value between 0 and 100, where 0 is the lowest priority and 100 is the highest priority. The default is 0.
        :param pulumi.Input[str] template_id: Input only. Specify the `template_id` to use for populating `Job.config`. The default is `preset/web-hd`. Preset Transcoder templates: - `preset/{preset_id}` - User defined JobTemplate: `{job_template_id}`
        :param pulumi.Input[int] ttl_after_completion_days: Job time to live value in days, which will be effective after job completion. Job should be deleted automatically after the given TTL. Enter a value between 1 and 90. The default is 30.
        """
        pulumi.set(__self__, "location", location)
        pulumi.set(__self__, "project", project)
        if config is not None:
            pulumi.set(__self__, "config", config)
        if input_uri is not None:
            pulumi.set(__self__, "input_uri", input_uri)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if output_uri is not None:
            pulumi.set(__self__, "output_uri", output_uri)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if template_id is not None:
            pulumi.set(__self__, "template_id", template_id)
        if ttl_after_completion_days is not None:
            pulumi.set(__self__, "ttl_after_completion_days", ttl_after_completion_days)

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
    @pulumi.getter
    def config(self) -> Optional[pulumi.Input['JobConfigArgs']]:
        """
        The configuration for this job.
        """
        return pulumi.get(self, "config")

    @config.setter
    def config(self, value: Optional[pulumi.Input['JobConfigArgs']]):
        pulumi.set(self, "config", value)

    @property
    @pulumi.getter(name="inputUri")
    def input_uri(self) -> Optional[pulumi.Input[str]]:
        """
        Input only. Specify the `input_uri` to populate empty `uri` fields in each element of `Job.config.inputs` or `JobTemplate.config.inputs` when using template. URI of the media. Input files must be at least 5 seconds in duration and stored in Cloud Storage (for example, `gs://bucket/inputs/file.mp4`).
        """
        return pulumi.get(self, "input_uri")

    @input_uri.setter
    def input_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "input_uri", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The resource name of the job. Format: `projects/{project}/locations/{location}/jobs/{job}`
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="outputUri")
    def output_uri(self) -> Optional[pulumi.Input[str]]:
        """
        Input only. Specify the `output_uri` to populate an empty `Job.config.output.uri` or `JobTemplate.config.output.uri` when using template. URI for the output file(s). For example, `gs://my-bucket/outputs/`.
        """
        return pulumi.get(self, "output_uri")

    @output_uri.setter
    def output_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "output_uri", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[int]]:
        """
        Specify the priority of the job. Enter a value between 0 and 100, where 0 is the lowest priority and 100 is the highest priority. The default is 0.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter(name="templateId")
    def template_id(self) -> Optional[pulumi.Input[str]]:
        """
        Input only. Specify the `template_id` to use for populating `Job.config`. The default is `preset/web-hd`. Preset Transcoder templates: - `preset/{preset_id}` - User defined JobTemplate: `{job_template_id}`
        """
        return pulumi.get(self, "template_id")

    @template_id.setter
    def template_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_id", value)

    @property
    @pulumi.getter(name="ttlAfterCompletionDays")
    def ttl_after_completion_days(self) -> Optional[pulumi.Input[int]]:
        """
        Job time to live value in days, which will be effective after job completion. Job should be deleted automatically after the given TTL. Enter a value between 1 and 90. The default is 30.
        """
        return pulumi.get(self, "ttl_after_completion_days")

    @ttl_after_completion_days.setter
    def ttl_after_completion_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ttl_after_completion_days", value)


class Job(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config: Optional[pulumi.Input[pulumi.InputType['JobConfigArgs']]] = None,
                 input_uri: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 output_uri: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 template_id: Optional[pulumi.Input[str]] = None,
                 ttl_after_completion_days: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Creates a job in the specified region.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['JobConfigArgs']] config: The configuration for this job.
        :param pulumi.Input[str] input_uri: Input only. Specify the `input_uri` to populate empty `uri` fields in each element of `Job.config.inputs` or `JobTemplate.config.inputs` when using template. URI of the media. Input files must be at least 5 seconds in duration and stored in Cloud Storage (for example, `gs://bucket/inputs/file.mp4`).
        :param pulumi.Input[str] name: The resource name of the job. Format: `projects/{project}/locations/{location}/jobs/{job}`
        :param pulumi.Input[str] output_uri: Input only. Specify the `output_uri` to populate an empty `Job.config.output.uri` or `JobTemplate.config.output.uri` when using template. URI for the output file(s). For example, `gs://my-bucket/outputs/`.
        :param pulumi.Input[int] priority: Specify the priority of the job. Enter a value between 0 and 100, where 0 is the lowest priority and 100 is the highest priority. The default is 0.
        :param pulumi.Input[str] template_id: Input only. Specify the `template_id` to use for populating `Job.config`. The default is `preset/web-hd`. Preset Transcoder templates: - `preset/{preset_id}` - User defined JobTemplate: `{job_template_id}`
        :param pulumi.Input[int] ttl_after_completion_days: Job time to live value in days, which will be effective after job completion. Job should be deleted automatically after the given TTL. Enter a value between 1 and 90. The default is 30.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: JobArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a job in the specified region.

        :param str resource_name: The name of the resource.
        :param JobArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(JobArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config: Optional[pulumi.Input[pulumi.InputType['JobConfigArgs']]] = None,
                 input_uri: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 output_uri: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 template_id: Optional[pulumi.Input[str]] = None,
                 ttl_after_completion_days: Optional[pulumi.Input[int]] = None,
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
            __props__ = JobArgs.__new__(JobArgs)

            __props__.__dict__["config"] = config
            __props__.__dict__["input_uri"] = input_uri
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["output_uri"] = output_uri
            __props__.__dict__["priority"] = priority
            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            __props__.__dict__["template_id"] = template_id
            __props__.__dict__["ttl_after_completion_days"] = ttl_after_completion_days
            __props__.__dict__["create_time"] = None
            __props__.__dict__["end_time"] = None
            __props__.__dict__["failure_details"] = None
            __props__.__dict__["failure_reason"] = None
            __props__.__dict__["origin_uri"] = None
            __props__.__dict__["progress"] = None
            __props__.__dict__["start_time"] = None
            __props__.__dict__["state"] = None
        super(Job, __self__).__init__(
            'google-native:transcoder/v1beta1:Job',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Job':
        """
        Get an existing Job resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = JobArgs.__new__(JobArgs)

        __props__.__dict__["config"] = None
        __props__.__dict__["create_time"] = None
        __props__.__dict__["end_time"] = None
        __props__.__dict__["failure_details"] = None
        __props__.__dict__["failure_reason"] = None
        __props__.__dict__["input_uri"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["origin_uri"] = None
        __props__.__dict__["output_uri"] = None
        __props__.__dict__["priority"] = None
        __props__.__dict__["progress"] = None
        __props__.__dict__["start_time"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["template_id"] = None
        __props__.__dict__["ttl_after_completion_days"] = None
        return Job(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def config(self) -> pulumi.Output['outputs.JobConfigResponse']:
        """
        The configuration for this job.
        """
        return pulumi.get(self, "config")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> pulumi.Output[str]:
        """
        The time the job was created.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> pulumi.Output[str]:
        """
        The time the transcoding finished.
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter(name="failureDetails")
    def failure_details(self) -> pulumi.Output[Sequence['outputs.FailureDetailResponse']]:
        """
        List of failure details. This property may contain additional information about the failure when `failure_reason` is present. *Note*: This feature is not yet available.
        """
        return pulumi.get(self, "failure_details")

    @property
    @pulumi.getter(name="failureReason")
    def failure_reason(self) -> pulumi.Output[str]:
        """
        A description of the reason for the failure. This property is always present when `state` is `FAILED`.
        """
        return pulumi.get(self, "failure_reason")

    @property
    @pulumi.getter(name="inputUri")
    def input_uri(self) -> pulumi.Output[str]:
        """
        Input only. Specify the `input_uri` to populate empty `uri` fields in each element of `Job.config.inputs` or `JobTemplate.config.inputs` when using template. URI of the media. Input files must be at least 5 seconds in duration and stored in Cloud Storage (for example, `gs://bucket/inputs/file.mp4`).
        """
        return pulumi.get(self, "input_uri")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name of the job. Format: `projects/{project}/locations/{location}/jobs/{job}`
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="originUri")
    def origin_uri(self) -> pulumi.Output['outputs.OriginUriResponse']:
        """
        The origin URI. *Note*: This feature is not yet available.
        """
        return pulumi.get(self, "origin_uri")

    @property
    @pulumi.getter(name="outputUri")
    def output_uri(self) -> pulumi.Output[str]:
        """
        Input only. Specify the `output_uri` to populate an empty `Job.config.output.uri` or `JobTemplate.config.output.uri` when using template. URI for the output file(s). For example, `gs://my-bucket/outputs/`.
        """
        return pulumi.get(self, "output_uri")

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Output[int]:
        """
        Specify the priority of the job. Enter a value between 0 and 100, where 0 is the lowest priority and 100 is the highest priority. The default is 0.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter
    def progress(self) -> pulumi.Output['outputs.ProgressResponse']:
        """
        Estimated fractional progress, from `0` to `1` for each step. *Note*: This feature is not yet available.
        """
        return pulumi.get(self, "progress")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Output[str]:
        """
        The time the transcoding started.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current state of the job.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="templateId")
    def template_id(self) -> pulumi.Output[str]:
        """
        Input only. Specify the `template_id` to use for populating `Job.config`. The default is `preset/web-hd`. Preset Transcoder templates: - `preset/{preset_id}` - User defined JobTemplate: `{job_template_id}`
        """
        return pulumi.get(self, "template_id")

    @property
    @pulumi.getter(name="ttlAfterCompletionDays")
    def ttl_after_completion_days(self) -> pulumi.Output[int]:
        """
        Job time to live value in days, which will be effective after job completion. Job should be deleted automatically after the given TTL. Enter a value between 1 and 90. The default is 30.
        """
        return pulumi.get(self, "ttl_after_completion_days")

