# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from .device import *
from .group import *
from .membership import *
from ._inputs import *
from . import outputs

def _register_module():
    import pulumi
    from ... import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "google-native:cloudidentity/v1:Device":
                return Device(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "google-native:cloudidentity/v1:Group":
                return Group(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "google-native:cloudidentity/v1:Membership":
                return Membership(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("google-native", "cloudidentity/v1", _module_instance)

_register_module()
