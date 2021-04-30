"""
SQLAlchemy de notre base de données CRM
"""
from sqlalchemy import Column, Integer, String, Date, DateTime

from app.database import CRM

# import datetime
# 'tim': int ((self.tim - datetime.datetime (1970, 1, 1)).total_seconds ()),


class Contact(CRM):
    """ Table contacts """
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    genre = Column(String, nullable=True)
    prenom = Column(String, nullable=True)
    nom = Column(String, nullable=True)
    sub_email = Column(String, nullable=True)
    sub_tel = Column(String, nullable=True)
    centres_interet = Column(String, nullable=True)
    code_postal = Column(String, nullable=True)
    code_commune = Column(String, nullable=True)
    commune = Column(String, nullable=True)
    code_departement = Column(String, nullable=True)
    departement = Column(String, nullable=True)
    code_region = Column(String, nullable=True)
    region = Column(String, nullable=True)


    def serialize(self):
        """ Print pour le call /contacts/ """
        return {
            'id': self.id,
            'Genre': self.genre,
            'Prénom': self.prenom,
            'Nom': self.nom,
            'Abonné_email': True if self.sub_email is not None else False,
            'Abonné_tel': True if self.sub_tel else False,
            'Code_postal': self.code_postal,
            'Code_commune': self.code_commune,
            'Commune': self.commune,
            'Code_département': self.code_departement,
            'Département': self.departement,
            'Code_région': self.code_region,
            'Région': self.region,
            'Centres_d\'intérêt': [] if self.centres_interet is None else self.centres_interet.split(',')
        }


class ContactFull(Contact):
    adherent_id = Column(Integer, nullable=True)
    email = Column(String, nullable=False, unique=True)
    telephones = Column(String, nullable=True)
    typeforms = Column(String, nullable=True)


class Downloads(CRM):
    """ Table crm_downloads """
    __tablename__ = 'crm_downloads'

    index = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    zone_type = Column(String, nullable=False)
    zone_name = Column(String, nullable=False)
    unique_user = Column(Integer, nullable=False)


class Users(CRM):
    """ Table crm_usage """
    __tablename__ = 'crm_usage'

    index = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    zone_type = Column(String, nullable=False)
    zone_name = Column(String, nullable=False)
    unique_user = Column(Integer, nullable=False)
