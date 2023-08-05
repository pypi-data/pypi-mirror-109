# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GoogleCloudRetailV2betaImageResponse',
    'GoogleCloudRetailV2betaPriceInfoResponse',
]

@pulumi.output_type
class GoogleCloudRetailV2betaImageResponse(dict):
    """
    Product thumbnail/detail image.
    """
    def __init__(__self__, *,
                 height: int,
                 uri: str,
                 width: int):
        """
        Product thumbnail/detail image.
        :param int height: Height of the image in number of pixels. This field must be nonnegative. Otherwise, an INVALID_ARGUMENT error is returned.
        :param str uri: Required. URI of the image. This field must be a valid UTF-8 encoded URI with a length limit of 5,000 characters. Otherwise, an INVALID_ARGUMENT error is returned. Google Merchant Center property [image_link](https://support.google.com/merchants/answer/6324350). Schema.org property [Product.image](https://schema.org/image).
        :param int width: Width of the image in number of pixels. This field must be nonnegative. Otherwise, an INVALID_ARGUMENT error is returned.
        """
        pulumi.set(__self__, "height", height)
        pulumi.set(__self__, "uri", uri)
        pulumi.set(__self__, "width", width)

    @property
    @pulumi.getter
    def height(self) -> int:
        """
        Height of the image in number of pixels. This field must be nonnegative. Otherwise, an INVALID_ARGUMENT error is returned.
        """
        return pulumi.get(self, "height")

    @property
    @pulumi.getter
    def uri(self) -> str:
        """
        Required. URI of the image. This field must be a valid UTF-8 encoded URI with a length limit of 5,000 characters. Otherwise, an INVALID_ARGUMENT error is returned. Google Merchant Center property [image_link](https://support.google.com/merchants/answer/6324350). Schema.org property [Product.image](https://schema.org/image).
        """
        return pulumi.get(self, "uri")

    @property
    @pulumi.getter
    def width(self) -> int:
        """
        Width of the image in number of pixels. This field must be nonnegative. Otherwise, an INVALID_ARGUMENT error is returned.
        """
        return pulumi.get(self, "width")


@pulumi.output_type
class GoogleCloudRetailV2betaPriceInfoResponse(dict):
    """
    The price information of a Product.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "currencyCode":
            suggest = "currency_code"
        elif key == "originalPrice":
            suggest = "original_price"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GoogleCloudRetailV2betaPriceInfoResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GoogleCloudRetailV2betaPriceInfoResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GoogleCloudRetailV2betaPriceInfoResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cost: float,
                 currency_code: str,
                 original_price: float,
                 price: float):
        """
        The price information of a Product.
        :param float cost: The costs associated with the sale of a particular product. Used for gross profit reporting. * Profit = price - cost Google Merchant Center property [cost_of_goods_sold](https://support.google.com/merchants/answer/9017895).
        :param str currency_code: The 3-letter currency code defined in [ISO 4217](https://www.iso.org/iso-4217-currency-codes.html). If this field is an unrecognizable currency code, an INVALID_ARGUMENT error is returned.
        :param float original_price: Price of the product without any discount. If zero, by default set to be the price.
        :param float price: Price of the product. Google Merchant Center property [price](https://support.google.com/merchants/answer/6324371). Schema.org property [Offer.priceSpecification](https://schema.org/priceSpecification).
        """
        pulumi.set(__self__, "cost", cost)
        pulumi.set(__self__, "currency_code", currency_code)
        pulumi.set(__self__, "original_price", original_price)
        pulumi.set(__self__, "price", price)

    @property
    @pulumi.getter
    def cost(self) -> float:
        """
        The costs associated with the sale of a particular product. Used for gross profit reporting. * Profit = price - cost Google Merchant Center property [cost_of_goods_sold](https://support.google.com/merchants/answer/9017895).
        """
        return pulumi.get(self, "cost")

    @property
    @pulumi.getter(name="currencyCode")
    def currency_code(self) -> str:
        """
        The 3-letter currency code defined in [ISO 4217](https://www.iso.org/iso-4217-currency-codes.html). If this field is an unrecognizable currency code, an INVALID_ARGUMENT error is returned.
        """
        return pulumi.get(self, "currency_code")

    @property
    @pulumi.getter(name="originalPrice")
    def original_price(self) -> float:
        """
        Price of the product without any discount. If zero, by default set to be the price.
        """
        return pulumi.get(self, "original_price")

    @property
    @pulumi.getter
    def price(self) -> float:
        """
        Price of the product. Google Merchant Center property [price](https://support.google.com/merchants/answer/6324371). Schema.org property [Offer.priceSpecification](https://schema.org/priceSpecification).
        """
        return pulumi.get(self, "price")


