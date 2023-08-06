from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Boolean,
    String,
)

from ...database import Base


class DesignationOutboxModel(Base):
    __tablename__ = "designations_outbox"

    id = Column(Integer, primary_key=True)
    intervention_condition_id = Column(
        Integer,
        ForeignKey('intervention_condition.id'),
        nullable=False,
    )
    designation = Column(String(128), nullable=False, index=True)
    news_id = Column(
        Integer,
        ForeignKey('newswires.id'),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
