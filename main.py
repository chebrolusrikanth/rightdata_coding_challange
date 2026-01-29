from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from schemas import DatasetCreate, LineageCreate
from models import Dataset
import crud, search

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Metadata Service")


@app.post("/datasets")
def add_dataset(data: DatasetCreate, db: Session = Depends(get_db)):
    return crud.create_dataset(db, data)


@app.post("/lineage")
def add_lineage(data: LineageCreate, db: Session = Depends(get_db)):
    upstream = db.query(Dataset).filter_by(fqn=data.upstream_fqn).first()
    downstream = db.query(Dataset).filter_by(fqn=data.downstream_fqn).first()

    if not upstream or not downstream:
        raise HTTPException(404, "Dataset not found")

    try:
        crud.create_lineage(db, upstream, downstream)
    except ValueError as e:
        raise HTTPException(400, str(e))

    return {"message": "Lineage created"}


@app.get("/search")
def search_api(q: str, db: Session = Depends(get_db)):
    results = search.search_datasets(db, q)
    return [
        {
            "priority": p,
            "fqn": d.fqn,
            "source_type": d.source_type
        }
        for p, d in results
    ]