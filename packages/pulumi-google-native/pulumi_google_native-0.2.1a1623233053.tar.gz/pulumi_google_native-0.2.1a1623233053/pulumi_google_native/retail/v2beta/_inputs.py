# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GoogleCloudRetailV2betaImageArgs',
    'GoogleCloudRetailV2betaPriceInfoArgs',
]

@pulumi.input_type
class GoogleCloudRetailV2betaImageArgs:
    def __init__(__self__, *,
                 height: Optional[pulumi.Input[int]] = None,
                 uri: Optional[pulumi.Input[str]] = None,
                 width: Optional[pulumi.Input[int]] = None):
        """
        Product thumbnail/detail image.
        :param pulumi.Input[int] height: Height of the image in number of pixels. This field must be nonnegative. Otherwise, an INVALID_ARGUMENT error is returned.
        :param pulumi.Input[str] uri: Required. URI of the image. This field must be a valid UTF-8 encoded URI with a length limit of 5,000 characters. Otherwise, an INVALID_ARGUMENT error is returned. Google Merchant Center property [image_link](https://support.google.com/merchants/answer/6324350). Schema.org property [Product.image](https://schema.org/image).
        :param pulumi.Input[int] width: Width of the image in number of pixels. This field must be nonnegative. Otherwise, an INVALID_ARGUMENT error is returned.
        """
        if height is not None:
            pulumi.set(__self__, "height", height)
        if uri is not None:
            pulumi.set(__self__, "uri", uri)
        if width is not None:
            pulumi.set(__self__, "width", width)

    @property
    @pulumi.getter
    def height(self) -> Optional[pulumi.Input[int]]:
        """
        Height of the image in number of pixels. This field must be nonnegative. Otherwise, an INVALID_ARGUMENT error is returned.
        """
        return pulumi.get(self, "height")

    @height.setter
    def height(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "height", value)

    @property
    @pulumi.getter
    def uri(self) -> Optional[pulumi.Input[str]]:
        """
        Required. URI of the image. This field must be a valid UTF-8 encoded URI with a length limit of 5,000 characters. Otherwise, an INVALID_ARGUMENT error is returned. Google Merchant Center property [image_link](https://support.google.com/merchants/answer/6324350). Schema.org property [Product.image](https://schema.org/image).
        """
        return pulumi.get(self, "uri")

    @uri.setter
    def uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "uri", value)

    @property
    @pulumi.getter
    def width(self) -> Optional[pulumi.Input[int]]:
        """
        Width of the image in number of pixels. This field must be nonnegative. Otherwise, an INVALID_ARGUMENT error is returned.
        """
        return pulumi.get(self, "width")

    @width.setter
    def width(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "width", value)


@pulumi.input_type
class GoogleCloudRetailV2betaPriceInfoArgs:
    def __init__(__self__, *,
                 cost: Optional[pulumi.Input[float]] = None,
                 currency_code: Optional[pulumi.Input[str]] = None,
                 original_price: Optional[pulumi.Input[float]] = None,
                 price: Optional[pulumi.Input[float]] = None):
        """
        The price information of a Product.
        :param pulumi.Input[float] cost: The costs associated with the sale of a particular product. Used for gross profit reporting. * Profit = price - cost Google Merchant Center property [cost_of_goods_sold](https://support.google.com/merchants/answer/9017895).
        :param pulumi.Input[str] currency_code: The 3-letter currency code defined in [ISO 4217](https://www.iso.org/iso-4217-currency-codes.html). If this field is an unrecognizable currency code, an INVALID_ARGUMENT error is returned.
        :param pulumi.Input[float] original_price: Price of the product without any discount. If zero, by default set to be the price.
        :param pulumi.Input[float] price: Price of the product. Google Merchant Center property [price](https://support.google.com/merchants/answer/6324371). Schema.org property [Offer.priceSpecification](https://schema.org/priceSpecification).
        """
        if cost is not None:
            pulumi.set(__self__, "cost", cost)
        if currency_code is not None:
            pulumi.set(__self__, "currency_code", currency_code)
        if original_price is not None:
            pulumi.set(__self__, "original_price", original_price)
        if price is not None:
            pulumi.set(__self__, "price", price)

    @property
    @pulumi.getter
    def cost(self) -> Optional[pulumi.Input[float]]:
        """
        The costs associated with the sale of a particular product. Used for gross profit reporting. * Profit = price - cost Google Merchant Center property [cost_of_goods_sold](https://support.google.com/merchants/answer/9017895).
        """
        return pulumi.get(self, "cost")

    @cost.setter
    def cost(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "cost", value)

    @property
    @pulumi.getter(name="currencyCode")
    def currency_code(self) -> Optional[pulumi.Input[str]]:
        """
        The 3-letter currency code defined in [ISO 4217](https://www.iso.org/iso-4217-currency-codes.html). If this field is an unrecognizable currency code, an INVALID_ARGUMENT error is returned.
        """
        return pulumi.get(self, "currency_code")

    @currency_code.setter
    def currency_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "currency_code", value)

    @property
    @pulumi.getter(name="originalPrice")
    def original_price(self) -> Optional[pulumi.Input[float]]:
        """
        Price of the product without any discount. If zero, by default set to be the price.
        """
        return pulumi.get(self, "original_price")

    @original_price.setter
    def original_price(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "original_price", value)

    @property
    @pulumi.getter
    def price(self) -> Optional[pulumi.Input[float]]:
        """
        Price of the product. Google Merchant Center property [price](https://support.google.com/merchants/answer/6324371). Schema.org property [Offer.priceSpecification](https://schema.org/priceSpecification).
        """
        return pulumi.get(self, "price")

    @price.setter
    def price(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "price", value)


