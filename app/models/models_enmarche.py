"""SQLAlchemy de notre base de données Globale."""
from app.database import Base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

# import datetime
# 'tim': int ((self.tim - datetime.datetime (1970, 1, 1)).total_seconds ()),


class Adherents(Base):
    """Table adherents id/uuid"""

    __tablename__ = "adherents"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address_postal_code = Column(String, nullable=True)
    uuid = Column(String(36), unique=True, nullable=False, index=True)
    managed_area_id = Column(
        Integer, ForeignKey("referent_managed_areas_tags.referent_managed_area_id")
    )
    managed_area = relationship("ReferentManagedAreasTags")
    candidate_managed_area_id = Column(Integer, ForeignKey("candidate_managed_area.id"))
    candidate_managed_area = relationship("CandidateManagedArea")


class ReferentManagedAreasTags(Base):
    """Table referent_managed_areas_tags"""

    __tablename__ = "referent_managed_areas_tags"

    referent_managed_area_id = Column(Integer, index=True)
    referent_tag_id = Column(Integer, ForeignKey("referent_tags.id"), nullable=True)
    referent_tag = relationship("ReferentTags", lazy="joined")

    __mapper_args__ = {"primary_key": [referent_managed_area_id, referent_tag_id]}


class AdherentMessageFilters(Base):
    """Table adherent_message_filters"""

    __tablename__ = "adherent_message_filters"

    id = Column(Integer, primary_key=True, index=True)
    referent_tag_id = Column(Integer, ForeignKey("referent_tags.id"), nullable=True)
    referent_tag = relationship("ReferentTags", lazy="joined")
    zone_id = Column(Integer, ForeignKey("geo_zone.id"), nullable=True)
    zone = relationship("GeoZone", lazy="joined")


class ReferentTags(Base):
    """Table referent_tags"""

    __tablename__ = "referent_tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    type = Column(String, nullable=True)
    zone_id = Column(Integer, ForeignKey("geo_zone.id"), nullable=True)
    zone = relationship("GeoZone", lazy="joined")


class AdherentMessages(Base):
    """Table adherent_messages"""

    __tablename__ = "adherent_messages"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("adherents.id"), nullable=True)
    author = relationship("Adherents", lazy="joined")
    filter_id = Column(
        Integer, ForeignKey("adherent_message_filters.id"), nullable=True
    )
    filter = relationship("AdherentMessageFilters", lazy="joined")
    label = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    status = Column(String, nullable=False)
    type = Column(String, nullable=False)
    sent_at = Column(DateTime, nullable=True)


class CandidateManagedArea(Base):
    """Table candidate_managed_area pour retrouver la zone_id"""

    __tablename__ = "candidate_managed_area"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("geo_zone.id"))
    candidate_managed_zone = relationship("GeoZone")

    def get_zone_id(self):
        return self.zone_id


class GeoZone(Base):
    """Table geo_zone pour retrouver la zone_id"""

    __tablename__ = "geo_zone"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), nullable=False)
    type = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    postal_code = Column(String(255), nullable=True)

    UniqueConstraint("code", "type", name="geo_zone_code_type_unique")


class GeoZoneParent(Base):
    """Table geo_zone_parent pour retrouver la zone_id"""

    __tablename__ = "geo_zone_parent"

    child_id = Column(Integer, ForeignKey("geo_zone.id"), index=True)
    child = relationship("GeoZone", foreign_keys="GeoZoneParent.child_id")
    parent_id = Column(Integer, ForeignKey("geo_zone.id"), index=True)
    parent = relationship("GeoZone", foreign_keys="GeoZoneParent.parent_id")

    __mapper_args__ = {"primary_key": [child_id, parent_id]}


class GeoBorough(Base):
    """Table geo_borough"""

    __tablename__ = "geo_borough"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey("geo_city.id"))
    geo_city = relationship("GeoCity")


class GeoCity(Base):
    """Table geo_city"""

    __tablename__ = "geo_city"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    name = Column(String(255), nullable=False)
    postal_code = Column(String, nullable=False)
    active = Column(Boolean, nullable=True)
    department_id = Column(Integer, ForeignKey("geo_department.id"))
    geo_department = relationship("GeoDepartment")


class GeoDistrict(Base):
    """Table geo_district"""

    __tablename__ = "geo_district"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    department_id = Column(Integer, ForeignKey("geo_department.id"))
    geo_department = relationship("GeoDepartment")


class GeoDepartment(Base):
    """Table geo_department"""

    __tablename__ = "geo_department"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    region_id = Column(Integer, ForeignKey("geo_region.id"))
    geo_region = relationship("GeoRegion")


class GeoRegion(Base):
    """Table geo_region"""

    __tablename__ = "geo_region"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)


class GeoCountry(Base):
    """Table geo_country"""

    __tablename__ = "geo_country"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)


class JemarcheDataSurvey(Base):
    """Table jemarche_data_survey"""

    __tablename__ = "jemarche_data_survey"

    id = Column(Integer, primary_key=True, index=True)
    data_survey_id = Column(Integer, ForeignKey("jecoute_data_survey.id"), nullable=True)
    data_survey = relationship("JecouteDataSurvey", lazy="joined")
    postal_code = Column(String, nullable=True)
    age_range = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class JecouteDataSurvey(Base):
    """Table jecoute_data_survey"""

    __tablename__ = "jecoute_data_survey"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, nullable=False)
    author_id = Column(Integer, ForeignKey("adherents.id"), nullable=True)
    author = relationship("Adherents", lazy="joined")
    author_postal_code = Column(String, nullable=True)
    survey_id = Column(Integer, ForeignKey("jecoute_survey.id"))
    survey = relationship("JecouteSurvey", lazy="joined")
    posted_at = Column(DateTime, nullable=False)


class JecouteSurvey(Base):
    """Table jecoute_survey"""

    __tablename__ = "jecoute_survey"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, nullable=False)
    created_by_adherent_id = Column(Integer, ForeignKey("adherents.id"), nullable=True)
    author = relationship("Adherents", lazy="joined")
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    type = Column(String, nullable=False)
    zone_id = Column(Integer, ForeignKey("geo_zone.id"))
    geo_zone_relation = relationship("GeoZone")


class MailChimpCampaign(Base):
    """Table mailchimp_campaign"""

    __tablename__ = "mailchimp_campaign"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("adherent_messages.id"), nullable=True)
    message = relationship("AdherentMessages", lazy="joined")
    recipient_count = Column(Integer, nullable=True)
    status = Column(String, nullable=False)
    report_id = Column(
        Integer, ForeignKey("mailchimp_campaign_report.id"), nullable=True
    )
    report = relationship(
        "MailChimpCampaignReport", back_populates="mailchimp_campaign"
    )


class MailChimpCampaignReport(Base):
    """Table mailchimp_campaign_report"""

    __tablename__ = "mailchimp_campaign_report"

    id = Column(Integer, primary_key=True, index=True)
    open_total = Column(Integer, nullable=False)
    open_unique = Column(Integer, nullable=False)
    click_total = Column(Integer, nullable=False)
    click_unique = Column(Integer, nullable=False)
    email_sent = Column(Integer, nullable=False)
    unsubscribed = Column(Integer, nullable=False)
    mailchimp_campaign = relationship("MailChimpCampaign", back_populates="report")
