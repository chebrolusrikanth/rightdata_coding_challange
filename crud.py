from sqlalchemy.orm import Session
from models import Dataset, DatasetColumn, DatasetLineage
from lineage import creates_cycle

def create_dataset(db: Session, data):
    parts = data.fqn.split(".")

    dataset = Dataset(
        fqn=data.fqn,
        connection=parts[0],
        database=parts[1],
        schema=parts[2],
        table=parts[3],
        source_type=data.source_type
    )
    db.add(dataset)
    db.flush()

    for col in data.columns:
        db.add(DatasetColumn(
            dataset_id=dataset.id,
            name=col.name,
            type=col.type
        ))

    db.commit()
    return dataset


def create_lineage(db: Session, upstream: Dataset, downstream: Dataset):
    if creates_cycle(db, upstream.id, downstream.id):
        raise ValueError("Invalid lineage: cycle detected")

    db.add(DatasetLineage(
        upstream_id=upstream.id,
        downstream_id=downstream.id
    ))
    db.commit()