# -*- coding: utf-8 -*-
"""
Validates cadaster parcel in Flanders
"""

import re

import colander
from colander import null

from oe_utils.validation import OEStrippedStringSchemaNode


class CadasterSchemaNode(colander.MappingSchema):

    afdeling = OEStrippedStringSchemaNode(
        validator=colander.Length(1, 50),
        missing=None
    )

    sectie = OEStrippedStringSchemaNode(
        validator=colander.Length(1, 50),
        missing=None
    )

    perceel = OEStrippedStringSchemaNode(
        validator=colander.Length(1, 50),
        missing=None
    )

    capakey = OEStrippedStringSchemaNode(
        validator=colander.Length(1, 50)
    )

    @staticmethod
    def preparer(parcel):
        if parcel is None or not parcel:
            return null  # pragma: no cover
        return parcel

    @staticmethod
    def validator(node, parcel):
        capakey = parcel.get('capakey', None)
        match = False
        if capakey:
            match = re.match(
                r"^[0-9]{5}[A-Z]{1}([0-9]{4})\/([0-9]{2})([A-Z\_]{1})([0-9]{3})$",
                capakey
            )
        if not capakey or not match:
            raise colander.Invalid(
                    node,
                    'Ongeldige capakey'
            )
