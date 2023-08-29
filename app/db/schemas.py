from pydantic import BaseModel

class DataSetBase(BaseModel):
    name: str
    organization: str
    description: str
    link: str

class DataSet(DataSetBase):
    id: int
    
    class Config:
        orm_mode = True
