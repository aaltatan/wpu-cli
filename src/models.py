from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Tax(Base):
    __tablename__ = "taxes"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    brackets: Mapped[list["TaxBracket"]] = relationship(
        back_populates="tax", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Tax(name={self.name}, description={self.description})>"


class TaxBracket(Base):
    __tablename__ = "tax_brackets"

    from_: Mapped[int] = mapped_column(nullable=False)
    to_: Mapped[int] = mapped_column(nullable=False)
    rate: Mapped[float] = mapped_column(nullable=False)
    tax: Mapped[Tax] = mapped_column(ForeignKey("taxes.id"))

    def __repr__(self):
        return f"<TaxBracket(from_={self.from_}, to_={self.to_}, rate={self.rate})>"


class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True, default=1)
    key: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[str] = mapped_column(nullable=False)


# if Setting.select().count() == 0:
#     Setting.create(key="social_security_deduction_rate", value=0.07)
#     Setting.create(key="social_security_minimum_salary", value=837_000)
#     Setting.create(key="locality_percentage", value=0.5)
#     Setting.create(key="compensation_tax_rate", value=0.05)

# if Tax.select().count() == 0:
#     Tax.create(name="Syrian Layers Tax", description="Default taxes")
#     TaxLayer.create(from_=0, to_=837_000, rate=0, tax_id=1)
#     TaxLayer.create(from_=837_001, to_=850_000, rate=0.11, tax_id=1)
#     TaxLayer.create(from_=850_001, to_=1_100_000, rate=0.13, tax_id=1)
#     TaxLayer.create(from_=1_100_001, to_=50_000_000, rate=0.15, tax_id=1)
