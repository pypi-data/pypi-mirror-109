# -*- coding: utf-8 -*-
"""
Deze module mapt binnenkomende json objecten naar database objecten.
"""
from oe_geoutils.data.models.locatie_adres import LocatieAdres
from oe_geoutils.data.models.locatie_element import LocatieElement
from oe_geoutils.data.models.openbaar_domein import OpenbaarDomein
from oe_geoutils.data.models.perceel import Perceel
from oe_geoutils.utils import convert_geojson_to_wktelement


def _map_locatie(
    locatie_json,
    resource,
    locatie_element_cls=LocatieElement,
    perceel_cls=Perceel,
    openbaar_domein_cls=OpenbaarDomein,
    adres_cls=LocatieAdres,
):
    """
    Mapt een locatie_json in json formaat tot de benodigde velden in een resource object

    :param locatie_json: Een dict die de JSON voorstelt die naar onze service
            gezonden werd.
    :param resource: resource object
    :param locatie_element_cls: class to instantiate when a new LocatieElement is needed.
    :param perceel_cls: class to instantiate when a new Perceel is needed.
    :param openbaar_domein_cls: class to instantiate when a new OpenbaarDomein is needed.
    :param adres_cls: class to instantiate when a new LocatieAdres is needed.
    :returns: resource object
    """
    resource.contour = convert_geojson_to_wktelement(locatie_json.get('contour'))
    resource.locatie_elementen = _map_locatie_elementen(
        locatie_json.get('elementen', []),
        resource.locatie_elementen,
        locatie_element_cls=locatie_element_cls,
        perceel_cls=perceel_cls,
        openbaar_domein_cls=openbaar_domein_cls,
        adres_cls=adres_cls
    )
    return resource


def _map_locatie_elementen(
    json_data,
    existing_db_objecten=None,
    locatie_element_cls=LocatieElement,
    perceel_cls=Perceel,
    openbaar_domein_cls=OpenbaarDomein,
    adres_cls=LocatieAdres,
):
    """
    Mapt een locatie_json in json formaat tot de benodigde velden in een resource object

    :param json_data: Een list van locatie element dicts gemaakt volgens de regels van de
       adapters in `oe_geoutils.renderer`
    :param locatie_element_cls: class to instantiate when a new LocatieElement is needed.
    :param perceel_cls: class to instantiate when a new Perceel is needed.
    :param openbaar_domein_cls: class to instantiate when a new OpenbaarDomein is needed.
    :param adres_cls: class to instantiate when a new LocatieAdres is needed.
    :returns: resource object
    """
    elementen = []
    existing_db_objecten = existing_db_objecten or []
    existing = {db_object.id: db_object for db_object in existing_db_objecten}
    for element_json in json_data:
        db_object = existing.get(element_json.get('id'))
        elementen.append(
            _map_locatie_element(
                element_json,
                db_object,
                locatie_element_cls=locatie_element_cls,
                perceel_cls=perceel_cls,
                openbaar_domein_cls=openbaar_domein_cls,
                adres_cls=adres_cls
            )
        )
    return elementen


def _map_locatie_element(
    json_data,
    db_object=None,
    locatie_element_cls=LocatieElement,
    perceel_cls=Perceel,
    openbaar_domein_cls=OpenbaarDomein,
    adres_cls=LocatieAdres,
):
    """
    Mapt de data van json_data naar een db_object.

    :param json_data: Een locatie element dict gemaakt volgens de regels van de
       adapters in `oe_geoutils.renderer`
    :param locatie_element_cls: class to instantiate when a new LocatieElement is needed.
    :param perceel_cls: class to instantiate when a new Perceel is needed.
    :param openbaar_domein_cls: class to instantiate when a new OpenbaarDomein is needed.
    :param adres_cls: class to instantiate when a new LocatieAdres is needed.
    :rtype: list of :class:`oe_geoutils.data.models.locatie_element.LocatieElement`
    """
    type_uri = json_data.get('type')
    if not any(type_uri == element_type.uri for element_type in LocatieElement.Type):
        raise ValueError("Locatie element json heeft geen geldig type.")
    if type_uri == LocatieElement.Type.PERCEEL.uri:
        db_object = db_object or perceel_cls()
        db_object.afdeling = json_data.get('perceel').get('afdeling')
        db_object.sectie = json_data.get('perceel').get('sectie')
        db_object.perceel = json_data.get('perceel').get('perceel')
        db_object.capakey = json_data.get('perceel').get('capakey')
    elif type_uri == LocatieElement.Type.OPENBAAR_DOMEIN.uri:
        db_object = db_object or openbaar_domein_cls()
        db_object.omschrijving = json_data.get('omschrijving')
    elif type_uri == LocatieElement.Type.ADRES.uri:
        db_object = db_object or adres_cls()
        db_object.straat_id = json_data.get('straat_id')
        db_object.straat = json_data.get('straat')
        db_object.huisnummer_id = json_data.get('huisnummer_id')
        db_object.huisnummer = json_data.get('huisnummer')
        db_object.subadres_id = json_data.get('subadres_id')
        db_object.subadres = json_data.get('subadres')
        db_object.postcode = json_data.get('postcode')
        db_object.land = json_data.get('land')
    elif type_uri == LocatieElement.Type.LOCATIE_ELEMENT.uri:
        db_object = db_object or locatie_element_cls()

    db_object.provincie_niscode = json_data.get('provincie').get('niscode')
    db_object.provincie_naam = json_data.get('provincie').get('naam')
    db_object.gemeente_niscode = json_data.get('gemeente').get('niscode')
    db_object.gemeente_naam = json_data.get('gemeente').get('naam')
    db_object.deelgemeente_niscode = json_data.get('deelgemeente', {}).get('niscode')
    db_object.deelgemeente_naam = json_data.get('deelgemeente', {}).get('naam')
    db_object.gemeente_crab_id = json_data.get('gemeente').get('id')
    return db_object
