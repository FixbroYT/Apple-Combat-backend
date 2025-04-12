from sqlalchemy import BigInteger, ForeignKey, String, Integer, Float
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from config import DATABASE_URL


engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    coins: Mapped[int] = mapped_column(BigInteger, default=0)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), nullable=True)

    # связи
    location = relationship("Location", back_populates="users")
    upgrades = relationship("UserUpgrade", back_populates="user", cascade="all, delete")
    owned_locations = relationship("UserLocation", back_populates="user", cascade="all, delete")

class Upgrade(Base):
    __tablename__ = "upgrades"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column()
    cost: Mapped[int] = mapped_column(Integer)
    bonus: Mapped[float] = mapped_column(Float)

    users = relationship("UserUpgrade", back_populates="upgrade", cascade="all, delete")

class UserUpgrade(Base):
    __tablename__ = "user_upgrades"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    upgrade_id: Mapped[int] = mapped_column(ForeignKey("upgrades.id"))
    count: Mapped[int] = mapped_column(default=1)

    user: Mapped["User"] = relationship(back_populates="upgrades")
    upgrade: Mapped["Upgrade"] = relationship(back_populates="users")

class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    cost: Mapped[int] = mapped_column(Integer)
    bonus_multiplier: Mapped[float] = mapped_column(Float)

    users = relationship("User", back_populates="location")

class UserLocation(Base):
    __tablename__ = "user_locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))

    user = relationship("User", back_populates="owned_locations")
    location = relationship("Location")

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables have been created!")