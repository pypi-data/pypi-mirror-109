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

__all__ = ['AnnotationArgs', 'Annotation']

@pulumi.input_type
class AnnotationArgs:
    def __init__(__self__, *,
                 annotation_store_id: pulumi.Input[str],
                 dataset_id: pulumi.Input[str],
                 location: pulumi.Input[str],
                 project: pulumi.Input[str],
                 annotation_source: Optional[pulumi.Input['AnnotationSourceArgs']] = None,
                 custom_data: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 image_annotation: Optional[pulumi.Input['ImageAnnotationArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_annotation: Optional[pulumi.Input['ResourceAnnotationArgs']] = None,
                 text_annotation: Optional[pulumi.Input['SensitiveTextAnnotationArgs']] = None):
        """
        The set of arguments for constructing a Annotation resource.
        :param pulumi.Input['AnnotationSourceArgs'] annotation_source: Details of the source.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] custom_data: Additional information for this annotation record, such as annotator and verifier information or study campaign.
        :param pulumi.Input['ImageAnnotationArgs'] image_annotation: Annotations for images. For example, bounding polygons.
        :param pulumi.Input[str] name: Resource name of the Annotation, of the form `projects/{project_id}/locations/{location_id}/datasets/{dataset_id}/annotationStores/{annotation_store_id}/annotations/{annotation_id}`.
        :param pulumi.Input['ResourceAnnotationArgs'] resource_annotation: Annotations for resource. For example, classification tags.
        :param pulumi.Input['SensitiveTextAnnotationArgs'] text_annotation: Annotations for sensitive texts. For example, a range that describes the location of sensitive text.
        """
        pulumi.set(__self__, "annotation_store_id", annotation_store_id)
        pulumi.set(__self__, "dataset_id", dataset_id)
        pulumi.set(__self__, "location", location)
        pulumi.set(__self__, "project", project)
        if annotation_source is not None:
            pulumi.set(__self__, "annotation_source", annotation_source)
        if custom_data is not None:
            pulumi.set(__self__, "custom_data", custom_data)
        if image_annotation is not None:
            pulumi.set(__self__, "image_annotation", image_annotation)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_annotation is not None:
            pulumi.set(__self__, "resource_annotation", resource_annotation)
        if text_annotation is not None:
            pulumi.set(__self__, "text_annotation", text_annotation)

    @property
    @pulumi.getter(name="annotationStoreId")
    def annotation_store_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "annotation_store_id")

    @annotation_store_id.setter
    def annotation_store_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "annotation_store_id", value)

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
    @pulumi.getter(name="annotationSource")
    def annotation_source(self) -> Optional[pulumi.Input['AnnotationSourceArgs']]:
        """
        Details of the source.
        """
        return pulumi.get(self, "annotation_source")

    @annotation_source.setter
    def annotation_source(self, value: Optional[pulumi.Input['AnnotationSourceArgs']]):
        pulumi.set(self, "annotation_source", value)

    @property
    @pulumi.getter(name="customData")
    def custom_data(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Additional information for this annotation record, such as annotator and verifier information or study campaign.
        """
        return pulumi.get(self, "custom_data")

    @custom_data.setter
    def custom_data(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "custom_data", value)

    @property
    @pulumi.getter(name="imageAnnotation")
    def image_annotation(self) -> Optional[pulumi.Input['ImageAnnotationArgs']]:
        """
        Annotations for images. For example, bounding polygons.
        """
        return pulumi.get(self, "image_annotation")

    @image_annotation.setter
    def image_annotation(self, value: Optional[pulumi.Input['ImageAnnotationArgs']]):
        pulumi.set(self, "image_annotation", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Resource name of the Annotation, of the form `projects/{project_id}/locations/{location_id}/datasets/{dataset_id}/annotationStores/{annotation_store_id}/annotations/{annotation_id}`.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceAnnotation")
    def resource_annotation(self) -> Optional[pulumi.Input['ResourceAnnotationArgs']]:
        """
        Annotations for resource. For example, classification tags.
        """
        return pulumi.get(self, "resource_annotation")

    @resource_annotation.setter
    def resource_annotation(self, value: Optional[pulumi.Input['ResourceAnnotationArgs']]):
        pulumi.set(self, "resource_annotation", value)

    @property
    @pulumi.getter(name="textAnnotation")
    def text_annotation(self) -> Optional[pulumi.Input['SensitiveTextAnnotationArgs']]:
        """
        Annotations for sensitive texts. For example, a range that describes the location of sensitive text.
        """
        return pulumi.get(self, "text_annotation")

    @text_annotation.setter
    def text_annotation(self, value: Optional[pulumi.Input['SensitiveTextAnnotationArgs']]):
        pulumi.set(self, "text_annotation", value)


class Annotation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 annotation_source: Optional[pulumi.Input[pulumi.InputType['AnnotationSourceArgs']]] = None,
                 annotation_store_id: Optional[pulumi.Input[str]] = None,
                 custom_data: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 dataset_id: Optional[pulumi.Input[str]] = None,
                 image_annotation: Optional[pulumi.Input[pulumi.InputType['ImageAnnotationArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 resource_annotation: Optional[pulumi.Input[pulumi.InputType['ResourceAnnotationArgs']]] = None,
                 text_annotation: Optional[pulumi.Input[pulumi.InputType['SensitiveTextAnnotationArgs']]] = None,
                 __props__=None):
        """
        Creates a new Annotation record. It is valid to create Annotation objects for the same source more than once since a unique ID is assigned to each record by this service.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AnnotationSourceArgs']] annotation_source: Details of the source.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] custom_data: Additional information for this annotation record, such as annotator and verifier information or study campaign.
        :param pulumi.Input[pulumi.InputType['ImageAnnotationArgs']] image_annotation: Annotations for images. For example, bounding polygons.
        :param pulumi.Input[str] name: Resource name of the Annotation, of the form `projects/{project_id}/locations/{location_id}/datasets/{dataset_id}/annotationStores/{annotation_store_id}/annotations/{annotation_id}`.
        :param pulumi.Input[pulumi.InputType['ResourceAnnotationArgs']] resource_annotation: Annotations for resource. For example, classification tags.
        :param pulumi.Input[pulumi.InputType['SensitiveTextAnnotationArgs']] text_annotation: Annotations for sensitive texts. For example, a range that describes the location of sensitive text.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AnnotationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a new Annotation record. It is valid to create Annotation objects for the same source more than once since a unique ID is assigned to each record by this service.

        :param str resource_name: The name of the resource.
        :param AnnotationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AnnotationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 annotation_source: Optional[pulumi.Input[pulumi.InputType['AnnotationSourceArgs']]] = None,
                 annotation_store_id: Optional[pulumi.Input[str]] = None,
                 custom_data: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 dataset_id: Optional[pulumi.Input[str]] = None,
                 image_annotation: Optional[pulumi.Input[pulumi.InputType['ImageAnnotationArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 resource_annotation: Optional[pulumi.Input[pulumi.InputType['ResourceAnnotationArgs']]] = None,
                 text_annotation: Optional[pulumi.Input[pulumi.InputType['SensitiveTextAnnotationArgs']]] = None,
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
            __props__ = AnnotationArgs.__new__(AnnotationArgs)

            __props__.__dict__["annotation_source"] = annotation_source
            if annotation_store_id is None and not opts.urn:
                raise TypeError("Missing required property 'annotation_store_id'")
            __props__.__dict__["annotation_store_id"] = annotation_store_id
            __props__.__dict__["custom_data"] = custom_data
            if dataset_id is None and not opts.urn:
                raise TypeError("Missing required property 'dataset_id'")
            __props__.__dict__["dataset_id"] = dataset_id
            __props__.__dict__["image_annotation"] = image_annotation
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            __props__.__dict__["resource_annotation"] = resource_annotation
            __props__.__dict__["text_annotation"] = text_annotation
        super(Annotation, __self__).__init__(
            'google-native:healthcare/v1beta1:Annotation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Annotation':
        """
        Get an existing Annotation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AnnotationArgs.__new__(AnnotationArgs)

        __props__.__dict__["annotation_source"] = None
        __props__.__dict__["custom_data"] = None
        __props__.__dict__["image_annotation"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["resource_annotation"] = None
        __props__.__dict__["text_annotation"] = None
        return Annotation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="annotationSource")
    def annotation_source(self) -> pulumi.Output['outputs.AnnotationSourceResponse']:
        """
        Details of the source.
        """
        return pulumi.get(self, "annotation_source")

    @property
    @pulumi.getter(name="customData")
    def custom_data(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Additional information for this annotation record, such as annotator and verifier information or study campaign.
        """
        return pulumi.get(self, "custom_data")

    @property
    @pulumi.getter(name="imageAnnotation")
    def image_annotation(self) -> pulumi.Output['outputs.ImageAnnotationResponse']:
        """
        Annotations for images. For example, bounding polygons.
        """
        return pulumi.get(self, "image_annotation")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name of the Annotation, of the form `projects/{project_id}/locations/{location_id}/datasets/{dataset_id}/annotationStores/{annotation_store_id}/annotations/{annotation_id}`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceAnnotation")
    def resource_annotation(self) -> pulumi.Output['outputs.ResourceAnnotationResponse']:
        """
        Annotations for resource. For example, classification tags.
        """
        return pulumi.get(self, "resource_annotation")

    @property
    @pulumi.getter(name="textAnnotation")
    def text_annotation(self) -> pulumi.Output['outputs.SensitiveTextAnnotationResponse']:
        """
        Annotations for sensitive texts. For example, a range that describes the location of sensitive text.
        """
        return pulumi.get(self, "text_annotation")

