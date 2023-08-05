# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'InstanceMessageArgs',
    'MemcacheParametersArgs',
    'NodeConfigArgs',
]

@pulumi.input_type
class InstanceMessageArgs:
    def __init__(__self__, *,
                 code: Optional[pulumi.Input[str]] = None,
                 message: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] code: A code that correspond to one type of user-facing message.
        :param pulumi.Input[str] message: Message on memcached instance which will be exposed to users.
        """
        if code is not None:
            pulumi.set(__self__, "code", code)
        if message is not None:
            pulumi.set(__self__, "message", message)

    @property
    @pulumi.getter
    def code(self) -> Optional[pulumi.Input[str]]:
        """
        A code that correspond to one type of user-facing message.
        """
        return pulumi.get(self, "code")

    @code.setter
    def code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "code", value)

    @property
    @pulumi.getter
    def message(self) -> Optional[pulumi.Input[str]]:
        """
        Message on memcached instance which will be exposed to users.
        """
        return pulumi.get(self, "message")

    @message.setter
    def message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "message", value)


@pulumi.input_type
class MemcacheParametersArgs:
    def __init__(__self__, *,
                 params: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The unique ID associated with this set of parameters. Users can use this id to determine if the parameters associated with the instance differ from the parameters associated with the nodes. A discrepancy between parameter ids can inform users that they may need to take action to apply parameters on nodes.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] params: User defined set of parameters to use in the memcached process.
        """
        if params is not None:
            pulumi.set(__self__, "params", params)

    @property
    @pulumi.getter
    def params(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        User defined set of parameters to use in the memcached process.
        """
        return pulumi.get(self, "params")

    @params.setter
    def params(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "params", value)


@pulumi.input_type
class NodeConfigArgs:
    def __init__(__self__, *,
                 cpu_count: Optional[pulumi.Input[int]] = None,
                 memory_size_mb: Optional[pulumi.Input[int]] = None):
        """
        Configuration for a Memcached Node.
        :param pulumi.Input[int] cpu_count: Required. Number of cpus per Memcached node.
        :param pulumi.Input[int] memory_size_mb: Required. Memory size in MiB for each Memcached node.
        """
        if cpu_count is not None:
            pulumi.set(__self__, "cpu_count", cpu_count)
        if memory_size_mb is not None:
            pulumi.set(__self__, "memory_size_mb", memory_size_mb)

    @property
    @pulumi.getter(name="cpuCount")
    def cpu_count(self) -> Optional[pulumi.Input[int]]:
        """
        Required. Number of cpus per Memcached node.
        """
        return pulumi.get(self, "cpu_count")

    @cpu_count.setter
    def cpu_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "cpu_count", value)

    @property
    @pulumi.getter(name="memorySizeMb")
    def memory_size_mb(self) -> Optional[pulumi.Input[int]]:
        """
        Required. Memory size in MiB for each Memcached node.
        """
        return pulumi.get(self, "memory_size_mb")

    @memory_size_mb.setter
    def memory_size_mb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "memory_size_mb", value)


