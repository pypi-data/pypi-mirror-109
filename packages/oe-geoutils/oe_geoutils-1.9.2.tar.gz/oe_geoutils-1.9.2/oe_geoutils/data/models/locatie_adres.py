# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from oe_geoutils.data.models import LocatieAdresAbstract
from oe_geoutils.data.models.locatie_element import LocatieElement


class LocatieAdres(LocatieElement, LocatieAdresAbstract):
    __tablename__ = 'locatieadressen'
    id = Column(Integer, ForeignKey('locatie_elementen.id'), primary_key=True)