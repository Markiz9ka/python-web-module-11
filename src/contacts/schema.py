import sqlalchemy.orm as orm
import database
import datetime

class Contacts(database.Base):
    __tablename__ = "contacts"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(nullable=False)
    surename: orm.Mapped[str] = orm.mapped_column(nullable=False)
    email: orm.Mapped[str] = orm.mapped_column(nullable=False)
    phone_number: orm.Mapped[str] = orm.mapped_column(nullable=False)
    date_of_birth: orm.Mapped[datetime.date] = orm.mapped_column(nullable=False)
    description: orm.Mapped[str] = orm.mapped_column(nullable=True)
