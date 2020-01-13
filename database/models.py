from regiuss import *
from database.core import Db


#==========================#
#          MODELS          #
#==========================#

class DataNama(Db.Base):
    __tablename__ = "data_nama"

    id = Column(Integer, primary_key=True)
    nama = Column(String(45))
    alamat = Column(String(45))
    status = Column(Integer)