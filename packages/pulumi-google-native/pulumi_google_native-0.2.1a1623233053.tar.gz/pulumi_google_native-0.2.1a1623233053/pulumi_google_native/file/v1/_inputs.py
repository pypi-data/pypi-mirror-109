# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'FileShareConfigArgs',
    'NetworkConfigArgs',
    'NfsExportOptionsArgs',
]

@pulumi.input_type
class FileShareConfigArgs:
    def __init__(__self__, *,
                 capacity_gb: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 nfs_export_options: Optional[pulumi.Input[Sequence[pulumi.Input['NfsExportOptionsArgs']]]] = None,
                 source_backup: Optional[pulumi.Input[str]] = None):
        """
        File share configuration for the instance.
        :param pulumi.Input[str] capacity_gb: File share capacity in gigabytes (GB). Cloud Filestore defines 1 GB as 1024^3 bytes.
        :param pulumi.Input[str] name: The name of the file share (must be 16 characters or less).
        :param pulumi.Input[Sequence[pulumi.Input['NfsExportOptionsArgs']]] nfs_export_options: Nfs Export Options. There is a limit of 10 export options per file share.
        :param pulumi.Input[str] source_backup: The resource name of the backup, in the format projects/{project_number}/locations/{location_id}/backups/{backup_id}, that this file share has been restored from.
        """
        if capacity_gb is not None:
            pulumi.set(__self__, "capacity_gb", capacity_gb)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if nfs_export_options is not None:
            pulumi.set(__self__, "nfs_export_options", nfs_export_options)
        if source_backup is not None:
            pulumi.set(__self__, "source_backup", source_backup)

    @property
    @pulumi.getter(name="capacityGb")
    def capacity_gb(self) -> Optional[pulumi.Input[str]]:
        """
        File share capacity in gigabytes (GB). Cloud Filestore defines 1 GB as 1024^3 bytes.
        """
        return pulumi.get(self, "capacity_gb")

    @capacity_gb.setter
    def capacity_gb(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "capacity_gb", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the file share (must be 16 characters or less).
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="nfsExportOptions")
    def nfs_export_options(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NfsExportOptionsArgs']]]]:
        """
        Nfs Export Options. There is a limit of 10 export options per file share.
        """
        return pulumi.get(self, "nfs_export_options")

    @nfs_export_options.setter
    def nfs_export_options(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NfsExportOptionsArgs']]]]):
        pulumi.set(self, "nfs_export_options", value)

    @property
    @pulumi.getter(name="sourceBackup")
    def source_backup(self) -> Optional[pulumi.Input[str]]:
        """
        The resource name of the backup, in the format projects/{project_number}/locations/{location_id}/backups/{backup_id}, that this file share has been restored from.
        """
        return pulumi.get(self, "source_backup")

    @source_backup.setter
    def source_backup(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_backup", value)


@pulumi.input_type
class NetworkConfigArgs:
    def __init__(__self__, *,
                 modes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 reserved_ip_range: Optional[pulumi.Input[str]] = None):
        """
        Network configuration for the instance.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] modes: Internet protocol versions for which the instance has IP addresses assigned. For this version, only MODE_IPV4 is supported.
        :param pulumi.Input[str] network: The name of the Google Compute Engine [VPC network](/compute/docs/networks-and-firewalls#networks) to which the instance is connected.
        :param pulumi.Input[str] reserved_ip_range: A /29 CIDR block in one of the [internal IP address ranges](https://www.arin.net/knowledge/address_filters.html) that identifies the range of IP addresses reserved for this instance. For example, 10.0.0.0/29 or 192.168.0.0/29. The range you specify can't overlap with either existing subnets or assigned IP address ranges for other Cloud Filestore instances in the selected VPC network.
        """
        if modes is not None:
            pulumi.set(__self__, "modes", modes)
        if network is not None:
            pulumi.set(__self__, "network", network)
        if reserved_ip_range is not None:
            pulumi.set(__self__, "reserved_ip_range", reserved_ip_range)

    @property
    @pulumi.getter
    def modes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Internet protocol versions for which the instance has IP addresses assigned. For this version, only MODE_IPV4 is supported.
        """
        return pulumi.get(self, "modes")

    @modes.setter
    def modes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "modes", value)

    @property
    @pulumi.getter
    def network(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Google Compute Engine [VPC network](/compute/docs/networks-and-firewalls#networks) to which the instance is connected.
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter(name="reservedIpRange")
    def reserved_ip_range(self) -> Optional[pulumi.Input[str]]:
        """
        A /29 CIDR block in one of the [internal IP address ranges](https://www.arin.net/knowledge/address_filters.html) that identifies the range of IP addresses reserved for this instance. For example, 10.0.0.0/29 or 192.168.0.0/29. The range you specify can't overlap with either existing subnets or assigned IP address ranges for other Cloud Filestore instances in the selected VPC network.
        """
        return pulumi.get(self, "reserved_ip_range")

    @reserved_ip_range.setter
    def reserved_ip_range(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "reserved_ip_range", value)


@pulumi.input_type
class NfsExportOptionsArgs:
    def __init__(__self__, *,
                 access_mode: Optional[pulumi.Input[str]] = None,
                 anon_gid: Optional[pulumi.Input[str]] = None,
                 anon_uid: Optional[pulumi.Input[str]] = None,
                 ip_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 squash_mode: Optional[pulumi.Input[str]] = None):
        """
        NFS export options specifications.
        :param pulumi.Input[str] access_mode: Either READ_ONLY, for allowing only read requests on the exported directory, or READ_WRITE, for allowing both read and write requests. The default is READ_WRITE.
        :param pulumi.Input[str] anon_gid: An integer representing the anonymous group id with a default value of 65534. Anon_gid may only be set with squash_mode of ROOT_SQUASH. An error will be returned if this field is specified for other squash_mode settings.
        :param pulumi.Input[str] anon_uid: An integer representing the anonymous user id with a default value of 65534. Anon_uid may only be set with squash_mode of ROOT_SQUASH. An error will be returned if this field is specified for other squash_mode settings.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_ranges: List of either an IPv4 addresses in the format {octet 1}.{octet 2}.{octet 3}.{octet 4} or CIDR ranges in the format {octet 1}.{octet 2}.{octet 3}.{octet 4}/{mask size} which may mount the file share. Overlapping IP ranges are not allowed, both within and across NfsExportOptions. An error will be returned. The limit is 64 IP ranges/addresses for each FileShareConfig among all NfsExportOptions.
        :param pulumi.Input[str] squash_mode: Either NO_ROOT_SQUASH, for allowing root access on the exported directory, or ROOT_SQUASH, for not allowing root access. The default is NO_ROOT_SQUASH.
        """
        if access_mode is not None:
            pulumi.set(__self__, "access_mode", access_mode)
        if anon_gid is not None:
            pulumi.set(__self__, "anon_gid", anon_gid)
        if anon_uid is not None:
            pulumi.set(__self__, "anon_uid", anon_uid)
        if ip_ranges is not None:
            pulumi.set(__self__, "ip_ranges", ip_ranges)
        if squash_mode is not None:
            pulumi.set(__self__, "squash_mode", squash_mode)

    @property
    @pulumi.getter(name="accessMode")
    def access_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Either READ_ONLY, for allowing only read requests on the exported directory, or READ_WRITE, for allowing both read and write requests. The default is READ_WRITE.
        """
        return pulumi.get(self, "access_mode")

    @access_mode.setter
    def access_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_mode", value)

    @property
    @pulumi.getter(name="anonGid")
    def anon_gid(self) -> Optional[pulumi.Input[str]]:
        """
        An integer representing the anonymous group id with a default value of 65534. Anon_gid may only be set with squash_mode of ROOT_SQUASH. An error will be returned if this field is specified for other squash_mode settings.
        """
        return pulumi.get(self, "anon_gid")

    @anon_gid.setter
    def anon_gid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "anon_gid", value)

    @property
    @pulumi.getter(name="anonUid")
    def anon_uid(self) -> Optional[pulumi.Input[str]]:
        """
        An integer representing the anonymous user id with a default value of 65534. Anon_uid may only be set with squash_mode of ROOT_SQUASH. An error will be returned if this field is specified for other squash_mode settings.
        """
        return pulumi.get(self, "anon_uid")

    @anon_uid.setter
    def anon_uid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "anon_uid", value)

    @property
    @pulumi.getter(name="ipRanges")
    def ip_ranges(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of either an IPv4 addresses in the format {octet 1}.{octet 2}.{octet 3}.{octet 4} or CIDR ranges in the format {octet 1}.{octet 2}.{octet 3}.{octet 4}/{mask size} which may mount the file share. Overlapping IP ranges are not allowed, both within and across NfsExportOptions. An error will be returned. The limit is 64 IP ranges/addresses for each FileShareConfig among all NfsExportOptions.
        """
        return pulumi.get(self, "ip_ranges")

    @ip_ranges.setter
    def ip_ranges(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ip_ranges", value)

    @property
    @pulumi.getter(name="squashMode")
    def squash_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Either NO_ROOT_SQUASH, for allowing root access on the exported directory, or ROOT_SQUASH, for not allowing root access. The default is NO_ROOT_SQUASH.
        """
        return pulumi.get(self, "squash_mode")

    @squash_mode.setter
    def squash_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "squash_mode", value)


