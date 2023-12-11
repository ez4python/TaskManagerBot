from sqlalchemy import create_engine, BIGINT, TEXT, ForeignKey, VARCHAR
from sqlalchemy.orm import declarative_base, Mapped, Session, mapped_column

engine = create_engine("postgresql+psycopg2://postgres:1@localhost:5432/task_manager_db")

Base = declarative_base()
session = Session(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(__type_pos=BIGINT, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(__type_pos=BIGINT, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=True)
    phone_number: Mapped[str] = mapped_column(__type_pos=VARCHAR(13), nullable=True)


class Tasks(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(__type_pos=BIGINT, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=True, default=None)
    description: Mapped[str] = mapped_column(__type_pos=TEXT)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))


Base.metadata.create_all(engine)

session.close()
