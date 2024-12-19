from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    slug = Column(String, unique=True, index=True)

    @property
    def user(self):
        from app.models.user import User  # Импортируем здесь
        return relationship('User', back_populates='tasks')

    #user = relationship('User', back_populates='tasks')

from sqlalchemy.schema import CreateTable
create_table_statement = CreateTable(Task.__table__)

print(str(create_table_statement))