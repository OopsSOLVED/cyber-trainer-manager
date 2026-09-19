"""
Curriculum ORM models.

Defines the hierarchical structure for the cybersecurity training roadmap:

    Phase → SkillLayer → Domain → Topic → LearningObjective

This maps to the 196-day learning plan structure:
- Phase: Groups of related skill areas (e.g., "Foundation", "Offensive")
- SkillLayer: Major skill categories (e.g., "Networking", "Linux")
- Domain: Sub-areas within a skill (e.g., "TCP/IP Fundamentals")
- Topic: Individual learning topics (e.g., "Subnetting")
- LearningObjective: Specific measurable goals (e.g., "Calculate CIDR notation")
"""

from sqlalchemy import String, Integer, Text, Boolean, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Phase(Base):
    """
    Top-level grouping of the curriculum.

    Examples: "Foundation Phase", "Offensive Security Phase",
    "Defensive Security Phase", "Teaching Phase"
    """

    __tablename__ = "phases"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    skill_layers: Mapped[list["SkillLayer"]] = relationship(
        back_populates="phase",
        cascade="all, delete-orphan",
        order_by="SkillLayer.order",
    )

    def __repr__(self) -> str:
        return f"<Phase(id={self.id}, name={self.name})>"


class SkillLayer(Base):
    """
    Major skill category within a phase.

    Maps to the 13 roadmap items:
    1. Computer foundations     8. SOC/SIEM/defensive
    2. Networking               9. Malware analysis
    3. Linux                   10. CTFs and labs
    4. Windows                 11. Teaching ability
    5. Offensive security      12. Curriculum creation
    6. Web/app security        13. Student management
    7. Enterprise/AD/Kerberos
    """

    __tablename__ = "skill_layers"

    phase_id: Mapped[int] = mapped_column(
        ForeignKey("phases.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    estimated_days: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    phase: Mapped["Phase"] = relationship(back_populates="skill_layers")
    domains: Mapped[list["Domain"]] = relationship(
        back_populates="skill_layer",
        cascade="all, delete-orphan",
        order_by="Domain.order",
    )

    def __repr__(self) -> str:
        return f"<SkillLayer(id={self.id}, name={self.name})>"


class Domain(Base):
    """
    Sub-area within a skill layer.

    Example: Under "Networking" → "TCP/IP Fundamentals",
    "Routing & Switching", "Wireless Security"
    """

    __tablename__ = "domains"

    skill_layer_id: Mapped[int] = mapped_column(
        ForeignKey("skill_layers.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    estimated_days: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    skill_layer: Mapped["SkillLayer"] = relationship(back_populates="domains")
    topics: Mapped[list["Topic"]] = relationship(
        back_populates="domain",
        cascade="all, delete-orphan",
        order_by="Topic.order",
    )

    def __repr__(self) -> str:
        return f"<Domain(id={self.id}, name={self.name})>"


class Topic(Base):
    """
    Individual learning topic within a domain.

    Example: Under "TCP/IP Fundamentals" → "Subnetting",
    "DNS Resolution", "ARP Protocol"
    """

    __tablename__ = "topics"

    domain_id: Mapped[int] = mapped_column(
        ForeignKey("domains.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    day_number: Mapped[int | None] = mapped_column(
        Integer, nullable=True,
        comment="Which day in the 196-day plan this topic falls on",
    )
    estimated_hours: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    difficulty: Mapped[str] = mapped_column(
        String(20), nullable=False, default="intermediate",
        comment="beginner, intermediate, advanced, expert",
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    domain: Mapped["Domain"] = relationship(back_populates="topics")
    objectives: Mapped[list["LearningObjective"]] = relationship(
        back_populates="topic",
        cascade="all, delete-orphan",
        order_by="LearningObjective.order",
    )

    def __repr__(self) -> str:
        return f"<Topic(id={self.id}, name={self.name}, day={self.day_number})>"


class LearningObjective(Base):
    """
    Specific measurable learning goal within a topic.

    Example: Under "Subnetting" → "Calculate CIDR notation from subnet mask",
    "Determine network/broadcast addresses"
    """

    __tablename__ = "learning_objectives"

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_measurable: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    topic: Mapped["Topic"] = relationship(back_populates="objectives")

    def __repr__(self) -> str:
        return f"<LearningObjective(id={self.id}, topic_id={self.topic_id})>"
