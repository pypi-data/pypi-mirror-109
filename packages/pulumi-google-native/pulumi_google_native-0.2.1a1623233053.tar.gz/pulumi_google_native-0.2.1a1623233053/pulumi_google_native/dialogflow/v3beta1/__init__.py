# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from .agent import *
from .entity_type import *
from .environment import *
from .experiment import *
from .flow import *
from .intent import *
from .page import *
from .security_setting import *
from .session_entity_type import *
from .test_case import *
from .transition_route_group import *
from .version import *
from .webhook import *
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
            if typ == "google-native:dialogflow/v3beta1:Agent":
                return Agent(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "google-native:dialogflow/v3beta1:EntityType":
                return EntityType(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "google-native:dialogflow/v3beta1:Environment":
                return Environment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "google-native:dialogflow/v3beta1:Experiment":
                return Experiment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "google-native:dialogflow/v3beta1:Flow":
                return Flow(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "google-native:dialogflow/v3beta1:Intent":
                return Intent(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "google-native:dialogflow/v3beta1:Page":
                return Page(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "google-native:dialogflow/v3beta1:SecuritySetting":
                return SecuritySetting(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "google-native:dialogflow/v3beta1:SessionEntityType":
                return SessionEntityType(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "google-native:dialogflow/v3beta1:TestCase":
                return TestCase(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "google-native:dialogflow/v3beta1:TransitionRouteGroup":
                return TransitionRouteGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "google-native:dialogflow/v3beta1:Version":
                return Version(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "google-native:dialogflow/v3beta1:Webhook":
                return Webhook(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("google-native", "dialogflow/v3beta1", _module_instance)

_register_module()
