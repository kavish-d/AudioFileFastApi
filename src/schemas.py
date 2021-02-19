# Defines Various Schemas for accepting request and returning response

from typing import Optional, Union
from pydantic import BaseModel, conint, constr, conlist
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

from pydantic.schema import schema

# Base for All Audio File


class AudioFileBase(BaseModel):
    duration: conint(strict=True, gt=0)
    upload_time: Optional[datetime]

    class Config:
        orm_mode = True

# Base for update makes fields optional


class AudioFileUpdateBase(BaseModel):
    duration: Optional[conint(strict=True, gt=0)]
    upload_time: Optional[datetime]

    class Config:
        orm_mode = True


# Song Schemas

class SongBase(AudioFileBase):
    name: constr(strip_whitespace=True, strict=True, max_length=100)


class SongUpdate(AudioFileUpdateBase):
    name: Optional[constr(strip_whitespace=True, strict=True, max_length=100)]


class Song(SongBase):
    id: int  # UUID can be used also

# Podcast Schemas


class PodcastBase(AudioFileBase):
    name: constr(strip_whitespace=True, strict=True, max_length=100)
    host: constr(strip_whitespace=True, strict=True, max_length=100)
    participants: Optional[conlist(item_type=constr(
        strip_whitespace=True, strict=True, max_length=100), max_items=10)] = []


class PodcastUpdate(AudioFileUpdateBase):
    name: Optional[constr(strip_whitespace=True, strict=True, max_length=100)]
    host: Optional[constr(strip_whitespace=True, strict=True, max_length=100)]
    participants: Optional[conlist(item_type=constr(
        strip_whitespace=True, strict=True, max_length=100), max_items=10)] = []


class Podcast(PodcastBase):
    id: int

# AudioBook Schemas


class AudioBookBase(AudioFileBase):
    title: constr(strip_whitespace=True, strict=True, max_length=100)
    author: constr(strip_whitespace=True, strict=True, max_length=100)
    narrator: constr(strip_whitespace=True, strict=True, max_length=100)


class AudioBookUpdate(AudioFileUpdateBase):
    title: Optional[constr(strip_whitespace=True, strict=True, max_length=100)]
    author: Optional[constr(strip_whitespace=True,
                            strict=True, max_length=100)]
    narrator: Optional[constr(strip_whitespace=True,
                              strict=True, max_length=100)]


class AudioBook(AudioBookBase):
    id: int

# Enum for file type


class FileType(str, Enum):
    audio_book = 'audiobook'
    podcast = 'podcast'
    song = 'song'

# Schema for accepting JSON for Audio File Creation (POST)


class AudioFileIn(BaseModel):
    audioFileType: FileType
    audioFileMetadata: Union[AudioBookBase, PodcastBase, SongBase]

    def __init__(__pydantic_self__, **data) -> None:
        super().__init__(**data)
        # Some fields being optional pydantic can't auto recognize File Type Schema form json So need to do manually
        __pydantic_self__.audioFileMetadata = schema_of_create[data['audioFileType']](
            **data['audioFileMetadata'])

# Schema for accepting JSON for modifying Audio File (PUT)


class AudioFileUpdate(BaseModel):
    audioFileType: FileType
    audioFileMetadata: Union[AudioBookUpdate, PodcastUpdate, SongUpdate]

    def __init__(__pydantic_self__, **data) -> None:
        super().__init__(**data)
        # All fields being optional can't make pydantic auto recognize File Type Schema form json So need to do manually
        __pydantic_self__.audioFileMetadata = schema_of_update[data['audioFileType']](
            **data['audioFileMetadata'])


# Represents Schema to accept json for all type of files for read
audio_files_read = Union[
    PodcastBase,
    AudioBookBase,
    SongBase,
]


# Represents Schema to accept json for all type of files for sending as response
audio_files = Union[
    Podcast,
    AudioBook,
    Song,
]


# Represents Schema to accept json for all type of files for updating
audio_files_update = Union[
    PodcastUpdate,
    AudioBookUpdate,
    SongUpdate,
]

# Resolve schema from filetype
schema_of = {
    'song': Song,
    'podcast': Podcast,
    'audiobook': AudioBook,
}



# Resolve schema from filetype
schema_of_create = {
    'song': SongBase,
    'podcast': PodcastBase,
    'audiobook': AudioBookBase,
}

# Resolve File Update schema from filetype
schema_of_update = {
    'song': SongUpdate,
    'podcast': PodcastUpdate,
    'audiobook': AudioBookUpdate,
}
