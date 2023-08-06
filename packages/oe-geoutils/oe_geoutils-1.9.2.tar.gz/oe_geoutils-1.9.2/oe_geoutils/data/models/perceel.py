# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from oe_geoutils.data.models import PerceelAbstract
from oe_geoutils.data.models.locatie_element import LocatieElement


class Perceel(LocatieElement, PerceelAbstract):
    __tablename__ = 'percelen'
    id = Column(Integer, ForeignKey('locatie_elementen.id'), primary_key=True)
