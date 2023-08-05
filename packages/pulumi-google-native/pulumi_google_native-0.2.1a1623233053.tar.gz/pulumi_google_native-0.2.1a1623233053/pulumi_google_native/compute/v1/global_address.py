# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['GlobalAddressArgs', 'GlobalAddress']

@pulumi.input_type
class GlobalAddressArgs:
    def __init__(__self__, *,
                 project: pulumi.Input[str],
                 address: Optional[pulumi.Input[str]] = None,
                 address_type: Optional[pulumi.Input[str]] = None,
                 creation_timestamp: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_version: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 network_tier: Optional[pulumi.Input[str]] = None,
                 prefix_length: Optional[pulumi.Input[int]] = None,
                 purpose: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 self_link: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 subnetwork: Optional[pulumi.Input[str]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a GlobalAddress resource.
        :param pulumi.Input[str] address: The static IP address represented by this resource.
        :param pulumi.Input[str] address_type: The type of address to reserve, either INTERNAL or EXTERNAL. If unspecified, defaults to EXTERNAL.
        :param pulumi.Input[str] creation_timestamp: [Output Only] Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource. Provide this field when you create the resource.
        :param pulumi.Input[str] id: [Output Only] The unique identifier for the resource. This identifier is defined by the server.
        :param pulumi.Input[str] ip_version: The IP version that will be used by this address. Valid options are IPV4 or IPV6. This can only be specified for a global address.
        :param pulumi.Input[str] kind: [Output Only] Type of the resource. Always compute#address for addresses.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?`. The first character must be a lowercase letter, and all following characters (except for the last character) must be a dash, lowercase letter, or digit. The last character must be a lowercase letter or digit.
        :param pulumi.Input[str] network: The URL of the network in which to reserve the address. This field can only be used with INTERNAL type with the VPC_PEERING purpose.
        :param pulumi.Input[str] network_tier: This signifies the networking tier used for configuring this address and can only take the following values: PREMIUM or STANDARD. Global forwarding rules can only be Premium Tier. Regional forwarding rules can be either Premium or Standard Tier. Standard Tier addresses applied to regional forwarding rules can be used with any external load balancer. Regional forwarding rules in Premium Tier can only be used with a network load balancer.
               
               If this field is not specified, it is assumed to be PREMIUM.
        :param pulumi.Input[int] prefix_length: The prefix length if the resource represents an IP range.
        :param pulumi.Input[str] purpose: The purpose of this resource, which can be one of the following values:  
               - `GCE_ENDPOINT` for addresses that are used by VM instances, alias IP ranges, internal load balancers, and similar resources. 
               - `DNS_RESOLVER` for a DNS resolver address in a subnetwork 
               - `VPC_PEERING` for addresses that are reserved for VPC peer networks. 
               - `NAT_AUTO` for addresses that are external IP addresses automatically reserved for Cloud NAT. 
               - `IPSEC_INTERCONNECT` for addresses created from a private IP range that are reserved for a VLAN attachment in an IPsec-encrypted Cloud Interconnect configuration. These addresses are regional resources.
        :param pulumi.Input[str] region: [Output Only] The URL of the region where a regional address resides. For regional addresses, you must specify the region as a path parameter in the HTTP request URL. This field is not applicable to global addresses.
        :param pulumi.Input[str] self_link: [Output Only] Server-defined URL for the resource.
        :param pulumi.Input[str] status: [Output Only] The status of the address, which can be one of RESERVING, RESERVED, or IN_USE. An address that is RESERVING is currently in the process of being reserved. A RESERVED address is currently reserved and available to use. An IN_USE address is currently being used by another resource and is not available.
        :param pulumi.Input[str] subnetwork: The URL of the subnetwork in which to reserve the address. If an IP address is specified, it must be within the subnetwork's IP range. This field can only be used with INTERNAL type with a GCE_ENDPOINT or DNS_RESOLVER purpose.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] users: [Output Only] The URLs of the resources that are using this address.
        """
        pulumi.set(__self__, "project", project)
        if address is not None:
            pulumi.set(__self__, "address", address)
        if address_type is not None:
            pulumi.set(__self__, "address_type", address_type)
        if creation_timestamp is not None:
            pulumi.set(__self__, "creation_timestamp", creation_timestamp)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if ip_version is not None:
            pulumi.set(__self__, "ip_version", ip_version)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if network is not None:
            pulumi.set(__self__, "network", network)
        if network_tier is not None:
            pulumi.set(__self__, "network_tier", network_tier)
        if prefix_length is not None:
            pulumi.set(__self__, "prefix_length", prefix_length)
        if purpose is not None:
            pulumi.set(__self__, "purpose", purpose)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if request_id is not None:
            pulumi.set(__self__, "request_id", request_id)
        if self_link is not None:
            pulumi.set(__self__, "self_link", self_link)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if subnetwork is not None:
            pulumi.set(__self__, "subnetwork", subnetwork)
        if users is not None:
            pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter
    def project(self) -> pulumi.Input[str]:
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: pulumi.Input[str]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter
    def address(self) -> Optional[pulumi.Input[str]]:
        """
        The static IP address represented by this resource.
        """
        return pulumi.get(self, "address")

    @address.setter
    def address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address", value)

    @property
    @pulumi.getter(name="addressType")
    def address_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of address to reserve, either INTERNAL or EXTERNAL. If unspecified, defaults to EXTERNAL.
        """
        return pulumi.get(self, "address_type")

    @address_type.setter
    def address_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address_type", value)

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> Optional[pulumi.Input[str]]:
        """
        [Output Only] Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, "creation_timestamp")

    @creation_timestamp.setter
    def creation_timestamp(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "creation_timestamp", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        An optional description of this resource. Provide this field when you create the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        [Output Only] The unique identifier for the resource. This identifier is defined by the server.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter(name="ipVersion")
    def ip_version(self) -> Optional[pulumi.Input[str]]:
        """
        The IP version that will be used by this address. Valid options are IPV4 or IPV6. This can only be specified for a global address.
        """
        return pulumi.get(self, "ip_version")

    @ip_version.setter
    def ip_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_version", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        [Output Only] Type of the resource. Always compute#address for addresses.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?`. The first character must be a lowercase letter, and all following characters (except for the last character) must be a dash, lowercase letter, or digit. The last character must be a lowercase letter or digit.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def network(self) -> Optional[pulumi.Input[str]]:
        """
        The URL of the network in which to reserve the address. This field can only be used with INTERNAL type with the VPC_PEERING purpose.
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter(name="networkTier")
    def network_tier(self) -> Optional[pulumi.Input[str]]:
        """
        This signifies the networking tier used for configuring this address and can only take the following values: PREMIUM or STANDARD. Global forwarding rules can only be Premium Tier. Regional forwarding rules can be either Premium or Standard Tier. Standard Tier addresses applied to regional forwarding rules can be used with any external load balancer. Regional forwarding rules in Premium Tier can only be used with a network load balancer.

        If this field is not specified, it is assumed to be PREMIUM.
        """
        return pulumi.get(self, "network_tier")

    @network_tier.setter
    def network_tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_tier", value)

    @property
    @pulumi.getter(name="prefixLength")
    def prefix_length(self) -> Optional[pulumi.Input[int]]:
        """
        The prefix length if the resource represents an IP range.
        """
        return pulumi.get(self, "prefix_length")

    @prefix_length.setter
    def prefix_length(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "prefix_length", value)

    @property
    @pulumi.getter
    def purpose(self) -> Optional[pulumi.Input[str]]:
        """
        The purpose of this resource, which can be one of the following values:  
        - `GCE_ENDPOINT` for addresses that are used by VM instances, alias IP ranges, internal load balancers, and similar resources. 
        - `DNS_RESOLVER` for a DNS resolver address in a subnetwork 
        - `VPC_PEERING` for addresses that are reserved for VPC peer networks. 
        - `NAT_AUTO` for addresses that are external IP addresses automatically reserved for Cloud NAT. 
        - `IPSEC_INTERCONNECT` for addresses created from a private IP range that are reserved for a VLAN attachment in an IPsec-encrypted Cloud Interconnect configuration. These addresses are regional resources.
        """
        return pulumi.get(self, "purpose")

    @purpose.setter
    def purpose(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "purpose", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        [Output Only] The URL of the region where a regional address resides. For regional addresses, you must specify the region as a path parameter in the HTTP request URL. This field is not applicable to global addresses.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="requestId")
    def request_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "request_id")

    @request_id.setter
    def request_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "request_id", value)

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> Optional[pulumi.Input[str]]:
        """
        [Output Only] Server-defined URL for the resource.
        """
        return pulumi.get(self, "self_link")

    @self_link.setter
    def self_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "self_link", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        [Output Only] The status of the address, which can be one of RESERVING, RESERVED, or IN_USE. An address that is RESERVING is currently in the process of being reserved. A RESERVED address is currently reserved and available to use. An IN_USE address is currently being used by another resource and is not available.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def subnetwork(self) -> Optional[pulumi.Input[str]]:
        """
        The URL of the subnetwork in which to reserve the address. If an IP address is specified, it must be within the subnetwork's IP range. This field can only be used with INTERNAL type with a GCE_ENDPOINT or DNS_RESOLVER purpose.
        """
        return pulumi.get(self, "subnetwork")

    @subnetwork.setter
    def subnetwork(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnetwork", value)

    @property
    @pulumi.getter
    def users(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        [Output Only] The URLs of the resources that are using this address.
        """
        return pulumi.get(self, "users")

    @users.setter
    def users(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "users", value)


class GlobalAddress(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address: Optional[pulumi.Input[str]] = None,
                 address_type: Optional[pulumi.Input[str]] = None,
                 creation_timestamp: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_version: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 network_tier: Optional[pulumi.Input[str]] = None,
                 prefix_length: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 purpose: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 self_link: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 subnetwork: Optional[pulumi.Input[str]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Creates an address resource in the specified project by using the data included in the request.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address: The static IP address represented by this resource.
        :param pulumi.Input[str] address_type: The type of address to reserve, either INTERNAL or EXTERNAL. If unspecified, defaults to EXTERNAL.
        :param pulumi.Input[str] creation_timestamp: [Output Only] Creation timestamp in RFC3339 text format.
        :param pulumi.Input[str] description: An optional description of this resource. Provide this field when you create the resource.
        :param pulumi.Input[str] id: [Output Only] The unique identifier for the resource. This identifier is defined by the server.
        :param pulumi.Input[str] ip_version: The IP version that will be used by this address. Valid options are IPV4 or IPV6. This can only be specified for a global address.
        :param pulumi.Input[str] kind: [Output Only] Type of the resource. Always compute#address for addresses.
        :param pulumi.Input[str] name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?`. The first character must be a lowercase letter, and all following characters (except for the last character) must be a dash, lowercase letter, or digit. The last character must be a lowercase letter or digit.
        :param pulumi.Input[str] network: The URL of the network in which to reserve the address. This field can only be used with INTERNAL type with the VPC_PEERING purpose.
        :param pulumi.Input[str] network_tier: This signifies the networking tier used for configuring this address and can only take the following values: PREMIUM or STANDARD. Global forwarding rules can only be Premium Tier. Regional forwarding rules can be either Premium or Standard Tier. Standard Tier addresses applied to regional forwarding rules can be used with any external load balancer. Regional forwarding rules in Premium Tier can only be used with a network load balancer.
               
               If this field is not specified, it is assumed to be PREMIUM.
        :param pulumi.Input[int] prefix_length: The prefix length if the resource represents an IP range.
        :param pulumi.Input[str] purpose: The purpose of this resource, which can be one of the following values:  
               - `GCE_ENDPOINT` for addresses that are used by VM instances, alias IP ranges, internal load balancers, and similar resources. 
               - `DNS_RESOLVER` for a DNS resolver address in a subnetwork 
               - `VPC_PEERING` for addresses that are reserved for VPC peer networks. 
               - `NAT_AUTO` for addresses that are external IP addresses automatically reserved for Cloud NAT. 
               - `IPSEC_INTERCONNECT` for addresses created from a private IP range that are reserved for a VLAN attachment in an IPsec-encrypted Cloud Interconnect configuration. These addresses are regional resources.
        :param pulumi.Input[str] region: [Output Only] The URL of the region where a regional address resides. For regional addresses, you must specify the region as a path parameter in the HTTP request URL. This field is not applicable to global addresses.
        :param pulumi.Input[str] self_link: [Output Only] Server-defined URL for the resource.
        :param pulumi.Input[str] status: [Output Only] The status of the address, which can be one of RESERVING, RESERVED, or IN_USE. An address that is RESERVING is currently in the process of being reserved. A RESERVED address is currently reserved and available to use. An IN_USE address is currently being used by another resource and is not available.
        :param pulumi.Input[str] subnetwork: The URL of the subnetwork in which to reserve the address. If an IP address is specified, it must be within the subnetwork's IP range. This field can only be used with INTERNAL type with a GCE_ENDPOINT or DNS_RESOLVER purpose.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] users: [Output Only] The URLs of the resources that are using this address.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GlobalAddressArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates an address resource in the specified project by using the data included in the request.

        :param str resource_name: The name of the resource.
        :param GlobalAddressArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GlobalAddressArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address: Optional[pulumi.Input[str]] = None,
                 address_type: Optional[pulumi.Input[str]] = None,
                 creation_timestamp: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_version: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 network_tier: Optional[pulumi.Input[str]] = None,
                 prefix_length: Optional[pulumi.Input[int]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 purpose: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 request_id: Optional[pulumi.Input[str]] = None,
                 self_link: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 subnetwork: Optional[pulumi.Input[str]] = None,
                 users: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
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
            __props__ = GlobalAddressArgs.__new__(GlobalAddressArgs)

            __props__.__dict__["address"] = address
            __props__.__dict__["address_type"] = address_type
            __props__.__dict__["creation_timestamp"] = creation_timestamp
            __props__.__dict__["description"] = description
            __props__.__dict__["id"] = id
            __props__.__dict__["ip_version"] = ip_version
            __props__.__dict__["kind"] = kind
            __props__.__dict__["name"] = name
            __props__.__dict__["network"] = network
            __props__.__dict__["network_tier"] = network_tier
            __props__.__dict__["prefix_length"] = prefix_length
            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            __props__.__dict__["purpose"] = purpose
            __props__.__dict__["region"] = region
            __props__.__dict__["request_id"] = request_id
            __props__.__dict__["self_link"] = self_link
            __props__.__dict__["status"] = status
            __props__.__dict__["subnetwork"] = subnetwork
            __props__.__dict__["users"] = users
        super(GlobalAddress, __self__).__init__(
            'google-native:compute/v1:GlobalAddress',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'GlobalAddress':
        """
        Get an existing GlobalAddress resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = GlobalAddressArgs.__new__(GlobalAddressArgs)

        __props__.__dict__["address"] = None
        __props__.__dict__["address_type"] = None
        __props__.__dict__["creation_timestamp"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["ip_version"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["network"] = None
        __props__.__dict__["network_tier"] = None
        __props__.__dict__["prefix_length"] = None
        __props__.__dict__["purpose"] = None
        __props__.__dict__["region"] = None
        __props__.__dict__["self_link"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["subnetwork"] = None
        __props__.__dict__["users"] = None
        return GlobalAddress(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def address(self) -> pulumi.Output[str]:
        """
        The static IP address represented by this resource.
        """
        return pulumi.get(self, "address")

    @property
    @pulumi.getter(name="addressType")
    def address_type(self) -> pulumi.Output[str]:
        """
        The type of address to reserve, either INTERNAL or EXTERNAL. If unspecified, defaults to EXTERNAL.
        """
        return pulumi.get(self, "address_type")

    @property
    @pulumi.getter(name="creationTimestamp")
    def creation_timestamp(self) -> pulumi.Output[str]:
        """
        [Output Only] Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, "creation_timestamp")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        An optional description of this resource. Provide this field when you create the resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="ipVersion")
    def ip_version(self) -> pulumi.Output[str]:
        """
        The IP version that will be used by this address. Valid options are IPV4 or IPV6. This can only be specified for a global address.
        """
        return pulumi.get(self, "ip_version")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        [Output Only] Type of the resource. Always compute#address for addresses.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?`. The first character must be a lowercase letter, and all following characters (except for the last character) must be a dash, lowercase letter, or digit. The last character must be a lowercase letter or digit.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def network(self) -> pulumi.Output[str]:
        """
        The URL of the network in which to reserve the address. This field can only be used with INTERNAL type with the VPC_PEERING purpose.
        """
        return pulumi.get(self, "network")

    @property
    @pulumi.getter(name="networkTier")
    def network_tier(self) -> pulumi.Output[str]:
        """
        This signifies the networking tier used for configuring this address and can only take the following values: PREMIUM or STANDARD. Global forwarding rules can only be Premium Tier. Regional forwarding rules can be either Premium or Standard Tier. Standard Tier addresses applied to regional forwarding rules can be used with any external load balancer. Regional forwarding rules in Premium Tier can only be used with a network load balancer.

        If this field is not specified, it is assumed to be PREMIUM.
        """
        return pulumi.get(self, "network_tier")

    @property
    @pulumi.getter(name="prefixLength")
    def prefix_length(self) -> pulumi.Output[int]:
        """
        The prefix length if the resource represents an IP range.
        """
        return pulumi.get(self, "prefix_length")

    @property
    @pulumi.getter
    def purpose(self) -> pulumi.Output[str]:
        """
        The purpose of this resource, which can be one of the following values:  
        - `GCE_ENDPOINT` for addresses that are used by VM instances, alias IP ranges, internal load balancers, and similar resources. 
        - `DNS_RESOLVER` for a DNS resolver address in a subnetwork 
        - `VPC_PEERING` for addresses that are reserved for VPC peer networks. 
        - `NAT_AUTO` for addresses that are external IP addresses automatically reserved for Cloud NAT. 
        - `IPSEC_INTERCONNECT` for addresses created from a private IP range that are reserved for a VLAN attachment in an IPsec-encrypted Cloud Interconnect configuration. These addresses are regional resources.
        """
        return pulumi.get(self, "purpose")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        [Output Only] The URL of the region where a regional address resides. For regional addresses, you must specify the region as a path parameter in the HTTP request URL. This field is not applicable to global addresses.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        [Output Only] Server-defined URL for the resource.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        [Output Only] The status of the address, which can be one of RESERVING, RESERVED, or IN_USE. An address that is RESERVING is currently in the process of being reserved. A RESERVED address is currently reserved and available to use. An IN_USE address is currently being used by another resource and is not available.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def subnetwork(self) -> pulumi.Output[str]:
        """
        The URL of the subnetwork in which to reserve the address. If an IP address is specified, it must be within the subnetwork's IP range. This field can only be used with INTERNAL type with a GCE_ENDPOINT or DNS_RESOLVER purpose.
        """
        return pulumi.get(self, "subnetwork")

    @property
    @pulumi.getter
    def users(self) -> pulumi.Output[Sequence[str]]:
        """
        [Output Only] The URLs of the resources that are using this address.
        """
        return pulumi.get(self, "users")

