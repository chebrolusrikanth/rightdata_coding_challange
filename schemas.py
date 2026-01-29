from typing import List
from pydantic import BaseModel

class ColumnSchema(BaseModel):
    name: str
    type: str


class DatasetCreate(BaseModel):
    fqn: str
    source_type: str
    columns: List[ColumnSchema]


class LineageCreate(BaseModel):
    upstream_fqn: str
    downstream_fqn: str