# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from oe_geoutils.data.models import OpenbaarDomeinAbstract
from oe_geoutils.data.models.locatie_element import LocatieElement


class OpenbaarDomein(LocatieElement, OpenbaarDomeinAbstract):
    __tablename__ = 'openbaredomeinen'
    id = Column(Integer, ForeignKey('locatie_elementen.id'), primary_key=True)


