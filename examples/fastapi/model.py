from __future__ import annotations

from pydantic import BaseModel, Field


class NewbornItem(BaseModel):
    surname: str = Field(..., description="The newborn's surname, eg: Reid")
    givenNames: str = Field(..., description="The newborn's given names, eg: Mathew David")
    sex: str = Field(..., description="The newborn's sex, eg: M, F or U")
    dateOfBirth: str = Field(..., description="The newborn's date of birth, eg: 17/03/2021")
    birthOrder: str = Field(..., description="The newborn's birth order, eg: 1")
    indigenousStatus: str = Field(..., description="The newborn's indigenous status, eg: 14")
    uniqueId: str = Field(..., description="The newborn's unique birth event id, eg: 20474417")


class Address(BaseModel):
    suburb: str = Field(..., description="The address suburb (Australia Only), eg: Watson")
    postcode: str = Field(..., description="The address postcode (Australia Only), eg: 2602")
    street1: str = Field(
        ...,
        description="The address street name line 1 (Australia Only), eg: 49 Aspinall St",
    )
    street2: str = Field(
        ..., description="The address street name line 2 (Australia Only), eg: Suite 1"
    )


class Parent(BaseModel):
    surname: str | None = Field(..., description="The mother's surname, eg: Mcdermott")
    givenNames: str = Field(..., description="The mother's given names, eg: Sarah Lousie")
    mailAddress: Address
    residentialAddress: Address
    mobile: str = Field(..., description="The mother's mobile phone number, eg: 0400182545")
    homePhone: str = Field(..., description="The mother's home phone number, eg: 0245458450")
    email: str = Field(..., description="The mother's email address, eg: jesse6565656565@gmail.com")
    hospital: str = Field(..., description="The hospital where the birth took place, eg: ACTCC")
    dateReceived: str = Field(
        ..., description="The date the birth event was received, eg: 17/03/2021"
    )
    personId: str = Field(..., description="The mother's personId, eg: 123456789")


class Model(BaseModel):
    parent: Parent
    newborn: list[NewbornItem]
