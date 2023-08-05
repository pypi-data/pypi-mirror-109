# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GcsSourceResponse',
    'GlossaryInputConfigResponse',
    'LanguageCodePairResponse',
    'LanguageCodesSetResponse',
]

@pulumi.output_type
class GcsSourceResponse(dict):
    """
    The Google Cloud Storage location for the input content.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "inputUri":
            suggest = "input_uri"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GcsSourceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GcsSourceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GcsSourceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 input_uri: str):
        """
        The Google Cloud Storage location for the input content.
        :param str input_uri: Required. Source data URI. For example, `gs://my_bucket/my_object`.
        """
        pulumi.set(__self__, "input_uri", input_uri)

    @property
    @pulumi.getter(name="inputUri")
    def input_uri(self) -> str:
        """
        Required. Source data URI. For example, `gs://my_bucket/my_object`.
        """
        return pulumi.get(self, "input_uri")


@pulumi.output_type
class GlossaryInputConfigResponse(dict):
    """
    Input configuration for glossaries.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "gcsSource":
            suggest = "gcs_source"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GlossaryInputConfigResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GlossaryInputConfigResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GlossaryInputConfigResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 gcs_source: 'outputs.GcsSourceResponse'):
        """
        Input configuration for glossaries.
        :param 'GcsSourceResponse' gcs_source: Required. Google Cloud Storage location of glossary data. File format is determined based on the filename extension. API returns [google.rpc.Code.INVALID_ARGUMENT] for unsupported URI-s and file formats. Wildcards are not allowed. This must be a single file in one of the following formats: For unidirectional glossaries: - TSV/CSV (`.tsv`/`.csv`): 2 column file, tab- or comma-separated. The first column is source text. The second column is target text. The file must not contain headers. That is, the first row is data, not column names. - TMX (`.tmx`): TMX file with parallel data defining source/target term pairs. For equivalent term sets glossaries: - CSV (`.csv`): Multi-column CSV file defining equivalent glossary terms in multiple languages. See documentation for more information - [glossaries](https://cloud.google.com/translate/docs/advanced/glossary).
        """
        pulumi.set(__self__, "gcs_source", gcs_source)

    @property
    @pulumi.getter(name="gcsSource")
    def gcs_source(self) -> 'outputs.GcsSourceResponse':
        """
        Required. Google Cloud Storage location of glossary data. File format is determined based on the filename extension. API returns [google.rpc.Code.INVALID_ARGUMENT] for unsupported URI-s and file formats. Wildcards are not allowed. This must be a single file in one of the following formats: For unidirectional glossaries: - TSV/CSV (`.tsv`/`.csv`): 2 column file, tab- or comma-separated. The first column is source text. The second column is target text. The file must not contain headers. That is, the first row is data, not column names. - TMX (`.tmx`): TMX file with parallel data defining source/target term pairs. For equivalent term sets glossaries: - CSV (`.csv`): Multi-column CSV file defining equivalent glossary terms in multiple languages. See documentation for more information - [glossaries](https://cloud.google.com/translate/docs/advanced/glossary).
        """
        return pulumi.get(self, "gcs_source")


@pulumi.output_type
class LanguageCodePairResponse(dict):
    """
    Used with unidirectional glossaries.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "sourceLanguageCode":
            suggest = "source_language_code"
        elif key == "targetLanguageCode":
            suggest = "target_language_code"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LanguageCodePairResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LanguageCodePairResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LanguageCodePairResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 source_language_code: str,
                 target_language_code: str):
        """
        Used with unidirectional glossaries.
        :param str source_language_code: Required. The BCP-47 language code of the input text, for example, "en-US". Expected to be an exact match for GlossaryTerm.language_code.
        :param str target_language_code: Required. The BCP-47 language code for translation output, for example, "zh-CN". Expected to be an exact match for GlossaryTerm.language_code.
        """
        pulumi.set(__self__, "source_language_code", source_language_code)
        pulumi.set(__self__, "target_language_code", target_language_code)

    @property
    @pulumi.getter(name="sourceLanguageCode")
    def source_language_code(self) -> str:
        """
        Required. The BCP-47 language code of the input text, for example, "en-US". Expected to be an exact match for GlossaryTerm.language_code.
        """
        return pulumi.get(self, "source_language_code")

    @property
    @pulumi.getter(name="targetLanguageCode")
    def target_language_code(self) -> str:
        """
        Required. The BCP-47 language code for translation output, for example, "zh-CN". Expected to be an exact match for GlossaryTerm.language_code.
        """
        return pulumi.get(self, "target_language_code")


@pulumi.output_type
class LanguageCodesSetResponse(dict):
    """
    Used with equivalent term set glossaries.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "languageCodes":
            suggest = "language_codes"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LanguageCodesSetResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LanguageCodesSetResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LanguageCodesSetResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 language_codes: Sequence[str]):
        """
        Used with equivalent term set glossaries.
        :param Sequence[str] language_codes: The BCP-47 language code(s) for terms defined in the glossary. All entries are unique. The list contains at least two entries. Expected to be an exact match for GlossaryTerm.language_code.
        """
        pulumi.set(__self__, "language_codes", language_codes)

    @property
    @pulumi.getter(name="languageCodes")
    def language_codes(self) -> Sequence[str]:
        """
        The BCP-47 language code(s) for terms defined in the glossary. All entries are unique. The list contains at least two entries. Expected to be an exact match for GlossaryTerm.language_code.
        """
        return pulumi.get(self, "language_codes")


