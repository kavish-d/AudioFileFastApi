# Utilities to perform CRUD over DB
from sqlalchemy.orm import Session
from src import models, schemas
from datetime import datetime
from fastapi import HTTPException

# To Obtain models from filetype strings
model_of = {
    'song': models.Song,
    'podcast': models.Podcast,
    'audiobook': models.AudioBook,
}

# Read Operation


def read(db: Session, file_type: str, file_id):
    cur_model = model_of[file_type]  # Resolve model from file type
    if file_id:  # If id specific request
        result = db.query(cur_model).filter_by(id=file_id).first()
        if not result:  # Id doesn't exist return 404 not found
            raise HTTPException(status_code=404, detail="File doesn't exist")
        return result
    # Id not specified get all
    return db.query(cur_model).all()

# Create Operation


def create(db: Session, file_type: str, file: schemas.audio_files_read):
    # Validate datetime to be more than current time
    if file.upload_time and file.upload_time < datetime.now(file.upload_time.tzinfo):
        # file.upload_time.tzinfo resolves timezone based on recieved valude
        # Raise unprocessable entity 422 same as default in fastapi
        raise HTTPException(
            status_code=422, detail="Upload Time should be more than current:"+str(datetime.now()))

    file = model_of[file_type](**file.dict())  # Create new row
    db.add(file)  # Add to db
    db.commit()  # Commit changes
    db.refresh(file)  # Refresh values in model instance
    return file


def update(db: Session, file_type: str, file: schemas.audio_files_update, file_id: int):
    # Fetch already existing row from db read already handles file not present
    old = read(db=db, file_type=file_type, file_id=file_id)
    # Validate datetime to be more than current time
    if file.upload_time and file.upload_time < datetime.now(file.upload_time.tzinfo):
        # file.upload_time.tzinfo resolves timezone based on recieved valude
        # Raise unprocessable entity 422 same as default in fastapi
        raise HTTPException(
            status_code=422, detail="Upload Time should be more than current:"+str(datetime.now()))
    # Iterate over recieved data
    for k, v in file.dict().items():
        if v:
            # update model instance fields with new fetched values as in update values in row
            setattr(old, k, v)
    db.commit()  # Commit changes
    db.refresh(old)  # Refresh values in model instance
    return old  # return refreshed row


def delete(db: Session, file_type: str, file_id: int):
    # Fetch already existing row from db read already handles file not present
    file = read(db=db, file_type=file_type, file_id=file_id)
    db.delete(file)  # delete file
    db.commit()  # commit changes
    return HTTPException(status_code=200, detail="Success!")  # return success
