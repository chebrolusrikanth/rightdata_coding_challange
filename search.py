from models import Dataset, DatasetColumn

def search_datasets(db, query: str):
    results = []

    for d in db.query(Dataset).filter(Dataset.table.ilike(f"%{query}%")).all():
        results.append((1, d))

    for d in db.query(Dataset)\
        .join(DatasetColumn)\
        .filter(DatasetColumn.name.ilike(f"%{query}%")).all():
        results.append((2, d))

    for d in db.query(Dataset).filter(Dataset.schema.ilike(f"%{query}%")).all():
        results.append((3, d))

    for d in db.query(Dataset).filter(Dataset.database.ilike(f"%{query}%")).all():
        results.append((4, d))

    unique = {}
    for p, d in results:
        if d.fqn not in unique or p < unique[d.fqn][0]:
            unique[d.fqn] = (p, d)

    return sorted(unique.values(), key=lambda x: x[0])