import uvicorn
from typing import List, Optional
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from src.database import SessionLocal, engine

from src import schemas, crud, models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allows cors for everyone
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# database Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Redirects base to docs


@app.get("/")
def main():
    return RedirectResponse(url="/docs")


# GET File Read
@app.get("/api/{audioFileType}/", response_model=List[schemas.audio_files])
@app.get("/api/{audioFileType}/{audioFileID}/", response_model=schemas.audio_files)
def get_file(audioFileType: schemas.FileType, audioFileID: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.read(db=db, file_type=audioFileType, file_id=audioFileID)


# POST File Write
@app.post("/api/", response_model=schemas.audio_files)
def post_file(fileIn: schemas.AudioFileIn, db: Session = Depends(get_db)):
    return crud.create(db=db, file_type=fileIn.audioFileType, file=fileIn.audioFileMetadata)

# PUT File Update


@app.put("/api/{audioFileID}/", response_model=schemas.audio_files)
def update_file(fileUpdate: schemas.AudioFileUpdate, audioFileID: int, db: Session = Depends(get_db)):
    return crud.update(db=db, file_type=fileUpdate.audioFileType, file=fileUpdate.audioFileMetadata, file_id=audioFileID)

# DELETE File Delete


@app.delete("/api/{audioFileType}/{audioFileID}/", status_code=200)
def delete_file(audioFileType: schemas.FileType, audioFileID: int, db: Session = Depends(get_db)):
    return crud.delete(db=db, file_type=audioFileType, file_id=audioFileID)


# For Development / Debugger
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
