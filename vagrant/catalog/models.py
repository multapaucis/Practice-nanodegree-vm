from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    picture = Column(String(256))


class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    description = Column(String(256))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'user_id': self.user_id,
        }


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String(32))
    author = Column(String(32))
    genre = relationship(Genre)
    genre_id = Column(Integer, ForeignKey('genre.id'))
    description = Column(String(256))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return {
            'title': self.title,
            'id': self.id,
            'author': self.author,
            'genre': self.genre.name,
            'description': self.description,
            'user_id': self.user_id,
        }


engine = create_engine('sqlite:///libraryUser.db')

Base.metadata.create_all(engine)
