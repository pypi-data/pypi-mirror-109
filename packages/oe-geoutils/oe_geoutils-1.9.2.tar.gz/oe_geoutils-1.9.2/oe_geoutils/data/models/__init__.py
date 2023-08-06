# -*- coding: utf-8 -*-
import enum

from oe_utils.data.models import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


class LocatieElementAbstract(Base):
    """
    A database table configuration object containing information about the location of a resource object.

    This object will not create the db table object.
    To create the table insert following code in the alembic migration file

    `alembic revision -m "<versie>"`


    from alembic import op
    import sqlalchemy as sa


    def upgrade():
        locatie_elementen = op.create_table('locatie_elementen',
                                        sa.Column('id', sa.Integer(), nullable=False),
                                        sa.Column('type', sa.String(length=250), nullable=False),
                                        sa.Column('resource_object_id', sa.Integer(), nullable=False),
                                        sa.Column('provincie_niscode', sa.Integer(), nullable=True),
                                        sa.Column('provincie_naam', sa.String(length=50), nullable=True),
                                        sa.Column('gemeente_niscode', sa.Integer(), nullable=False),
                                        sa.Column('gemeente_naam', sa.String(length=255), nullable=False),
                                        sa.Column('gemeente_crab_id', sa.Integer(), nullable=True),
                                        sa.Column('deelgemeente_niscode', sa.String(length=10), nullable=False),
                                        sa.Column('deelgemeente_naam', sa.String(length=255), nullable=False),
                                        sa.ForeignKeyConstraint(['resource_object_id'],
                                                                ['<resource>.id']),
                                        sa.PrimaryKeyConstraint('id', name='locatie_elementen_pk')
                                        )

        op.execute('GRANT SELECT, INSERT, UPDATE, DELETE ON locatie_elementen TO <user>_dml')
        op.execute('GRANT ALL ON locatie_elementen_id_seq TO <user>_dml')


    def downgrade():
        op.drop_table('locatie_elementen')
    """

    class Type(enum.Enum):
        LOCATIE_ELEMENT = 'LocatieElement'
        PERCEEL = 'LocatieElementPerceel'
        OPENBAAR_DOMEIN = 'LocatieElementOpenbaarDomein'
        ADRES = 'LocatieElementAdres'

        def __init__(self, uri_type):
            super(self.__class__, self).__init__()
            self.uri = 'https://id.erfgoed.net/vocab/ontology#' + uri_type

    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(250))
    resource_object_id = Column(Integer)
    provincie_niscode = Column(Integer, nullable=True)
    provincie_naam = Column(String(50), nullable=True)
    gemeente_niscode = Column(Integer)
    gemeente_naam = Column(String(255))
    gemeente_crab_id = Column(Integer)
    deelgemeente_niscode = Column(String(10))
    deelgemeente_naam = Column(String(255))

    __mapper_args__ = {
        'polymorphic_identity': Type.LOCATIE_ELEMENT.uri,
        'polymorphic_on': type,
        # When an object has a relationship with LocatieElement sa will only
        # retrieve LocatieElement columns when retrieving the initial list. All
        # columns from inheritated classes are usually needed as well though
        # so sa would have to do an extra query per object in the list.
        # This `with_polymorphic` causes sa to immediately fetch all columns,
        # including inherited classes ones, at once.
        'with_polymorphic': '*'
    }


class PerceelAbstract(LocatieElementAbstract):
    """
    A database table configuration object containing information about the location of a resource object.
    Perceel is a subclass of LocatieElement. Therefor the table locatie_elementen described in the class documentation
    of LocatieElement also needs to be created

    This object will not create the db table object.
    To create the table insert following code in the alembic migration file

    `alembic revision -m "<versie>"`


    from alembic import op
    import sqlalchemy as sa

    def upgrade():
        percelen = op.create_table('percelen',
                                sa.Column('id', sa.Integer(), nullable=False),
                                sa.Column('afdeling', sa.String(length=50), nullable=True),
                                sa.Column('sectie', sa.String(length=50), nullable=True),
                                sa.Column('perceel', sa.String(length=50), nullable=True),
                                sa.Column('capakey', sa.String(length=50), nullable=False),
                                sa.ForeignKeyConstraint(['id'], ['locatie_elementen.id']),
                                sa.PrimaryKeyConstraint('id', name='percelen_pk')
                                )

        op.execute('GRANT SELECT, INSERT, UPDATE, DELETE ON percelen TO <user>_dml')


    def downgrade():
        op.drop_table('percelen')
    """
    __abstract__ = True
    afdeling = Column(String(50))
    sectie = Column(String(50))
    perceel = Column(String(50))
    capakey = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': LocatieElementAbstract.Type.PERCEEL.uri,
    }


class OpenbaarDomeinAbstract(LocatieElementAbstract):
    """
    A database table configuration object containing information about the location of a resource object.
    OpenbaarDomein is a subclass of LocatieElement. Therefor the table locatie_elementen described in the
    class documentation of LocatieElement also needs to be created

    This object will not create the db table object.
    To create the table insert following code in the alembic migration file

    `alembic revision -m "<versie>"`


    from alembic import op
    import sqlalchemy as sa

    def upgrade():
        openbaredomeinen = op.create_table('openbaredomeinen',
                                       sa.Column('id', sa.Integer(), nullable=False),
                                       sa.Column('omschrijving', sa.String(length=250), nullable=True),
                                       sa.ForeignKeyConstraint(['id'], ['locatie_elementen.id']),
                                       sa.PrimaryKeyConstraint('id', name='openbaredomeinen_pk')
                                       )

        op.execute('GRANT SELECT, INSERT, UPDATE, DELETE ON openbaredomeinen TO <user>_dml')


    def downgrade():
        op.drop_table('openbaredomeinen')
    """
    __abstract__ = True
    omschrijving = Column(String(250))

    __mapper_args__ = {
        'polymorphic_identity': LocatieElementAbstract.Type.OPENBAAR_DOMEIN.uri,
    }


class LocatieAdresAbstract(LocatieElementAbstract):
    """
    A database table configuration object containing information about the location of a resource object.
    LocatieAdres is a subclass of LocatieElement. Therefor the table locatie_elementen described in the
    class documentation of LocatieElement also needs to be created

    This object will not create the db table object.
    To create the table insert following code in the alembic migration file

    `alembic revision -m "<versie>"`


    from alembic import op
    import sqlalchemy as sa

    def upgrade():
        locatieadressen = op.create_table('locatieadressen',
                                      sa.Column('id', sa.Integer(), nullable=False),
                                      sa.Column('straat_id', sa.Integer(), nullable=True),
                                      sa.Column('straat', sa.String(length=100), nullable=True),
                                      sa.Column('huisnummer_id', sa.Integer(), nullable=True),
                                      sa.Column('huisnummer', sa.String(length=255), nullable=True),
                                      sa.Column('subadres_id', sa.Integer(), nullable=True),
                                      sa.Column('subadres', sa.String(length=20), nullable=True),
                                      sa.Column('postcode', sa.String(length=20), nullable=True),
                                      sa.Column('land', sa.String(length=100), nullable=True),
                                      sa.ForeignKeyConstraint(['id'], ['locatie_elementen.id']),
                                      sa.PrimaryKeyConstraint('id', name='locatieadressen_pk')
                                      )

        op.execute('GRANT SELECT, INSERT, UPDATE, DELETE ON locatieadressen TO <user>_dml')


    def downgrade():
        op.drop_table('locatieadressen')
    """
    __abstract__ = True
    straat_id = Column(Integer)
    straat = Column(String(100))
    huisnummer_id = Column(Integer)
    huisnummer = Column(String(255))
    subadres_id = Column(Integer)
    subadres = Column(String(20))
    postcode = Column(String(20))
    land = Column(String(100))

    __mapper_args__ = {
        'polymorphic_identity': LocatieElementAbstract.Type.ADRES.uri,
    }