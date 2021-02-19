# Defines Database Models for all 3 file type

import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime, PickleType
from src.database import Base


class Song(Base):
    __tablename__ = "Songs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), index=True)
    duration = Column(Integer)
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)


class Podcast(Base):
    __tablename__ = "Podcasts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), index=True)
    duration = Column(Integer)
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)
    host = Column(String(100), index=True)
    participants = Column(PickleType)

    def __repr__(self):
        return str(self.id)

# To use many to many relationships for Podcast-Participant Not needed when it's just list of string
# class Participant(Base):
#     __tablename__ = "Participants"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     name = Column(String(100), index=True)
#     podcast= relationship('Podcast', secondary='PodcastParticipants')
# class PodcastParticipants(Base):
#     __tablename__ = 'PodcastParticipants'
#     id =Column(Integer, primary_key=True)
#     participant_id = Column(Integer, ForeignKey('Participants.id'))
#     podcast_id = Column(Integer, ForeignKey('Podcasts.id'))
#     participant = relationship(Participant, backref=backref("PodcastParticipants", cascade="all, delete-orphan"))
#     product = relationship(Podcast, backref=backref("PodcastParticipants"))


class AudioBook(Base):
    __tablename__ = "AudioBooks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), index=True)
    author = Column(String(100), index=True)
    narrator = Column(String(100), index=True)
    duration = Column(Integer)
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return str(self.id)
