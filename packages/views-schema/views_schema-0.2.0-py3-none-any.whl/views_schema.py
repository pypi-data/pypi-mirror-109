
from typing import List,Optional
import pydantic

class Operation(pydantic.BaseModel):
    """
    A path-element in a path defining a data column.
    May be a DatabaseOperation or a TransformOperation.
    """
    class Config:
        orm_mode = True

    namespace: str
    name: str
    arguments: List[str]

class DatabaseOperation(Operation):
    """
    The terminal operation of a path defining a data column.
    The name attribute points to a table.column in the database.
    The arguments attribute is either "values", or in the case of
    aggregation, the name of an aggregation function.
    """
    class Config:
        orm_mode = True

    namespace = "base"
    arguments: List[str] = ["values"]

class TransformOperation(Operation):
    """
    A non-terminal operation in a path defining a data column.  The name
    attribute points to a module.function in the transform service, which is
    applied to the subsequent data in the path.
    """
    class Config:
        orm_mode = True

    namespace = "trf"

class RenameOperation(TransformOperation):
    name = "util.rename"

class Queryset(pydantic.BaseModel):
    """
    A set of operations with associated metadata.
    """
    class Config:
        orm_mode = True

    loa: str
    name: str
    themes: List[str] = []

    description: Optional[str]

    operations: List[List[Operation]]
