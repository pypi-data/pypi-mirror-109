# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GoogleFirestoreAdminV1beta1IndexFieldResponse',
]

@pulumi.output_type
class GoogleFirestoreAdminV1beta1IndexFieldResponse(dict):
    """
    A field of an index.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "fieldPath":
            suggest = "field_path"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GoogleFirestoreAdminV1beta1IndexFieldResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GoogleFirestoreAdminV1beta1IndexFieldResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GoogleFirestoreAdminV1beta1IndexFieldResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 field_path: str,
                 mode: str):
        """
        A field of an index.
        :param str field_path: The path of the field. Must match the field path specification described by google.firestore.v1beta1.Document.fields. Special field path `__name__` may be used by itself or at the end of a path. `__type__` may be used only at the end of path.
        :param str mode: The field's mode.
        """
        pulumi.set(__self__, "field_path", field_path)
        pulumi.set(__self__, "mode", mode)

    @property
    @pulumi.getter(name="fieldPath")
    def field_path(self) -> str:
        """
        The path of the field. Must match the field path specification described by google.firestore.v1beta1.Document.fields. Special field path `__name__` may be used by itself or at the end of a path. `__type__` may be used only at the end of path.
        """
        return pulumi.get(self, "field_path")

    @property
    @pulumi.getter
    def mode(self) -> str:
        """
        The field's mode.
        """
        return pulumi.get(self, "mode")


