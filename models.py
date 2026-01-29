from sqlalchemy import Column, Integer, String, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True)
    fqn = Column(String(255), unique=True, index=True, nullable=False)
    connection = Column(String(100))
    database = Column(String(100))
    schema = Column(String(100))
    table = Column(String(100))
    source_type = Column(Enum("MYSQL", "MSSQL", "POSTGRESQL", name="source_type"))

    columns = relationship("DatasetColumn", back_populates="dataset")


class DatasetColumn(Base):
    __tablename__ = "dataset_columns"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(ForeignKey("datasets.id"))
    name = Column(String(100), index=True)
    type = Column(String(50))

    dataset = relationship("Dataset", back_populates="columns")


class DatasetLineage(Base):
    __tablename__ = "dataset_lineage"

    id = Column(Integer, primary_key=True)
    upstream_id = Column(ForeignKey("datasets.id"), nullable=False)
    downstream_id = Column(ForeignKey("datasets.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("upstream_id", "downstream_id"),
    )