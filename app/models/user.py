from app.backend.db import Base
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firtstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)

    tasks = relationship('Task', back_populates='user')

from sqlalchemy.schema import CreateTable
create_table_statement = CreateTable(User.__table__)

print(str(create_table_statement))