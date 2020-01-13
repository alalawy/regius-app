from regiuss import *
from database.config import *

class Db:
    if db == "mysql":
        enginedb = create_engine('mysql+pymysql://' + user + ':' + password + '@' + server + '/' + db_name)
    if db == "postgresql":
        enginedb = create_engine('postgresql://' + user + ':' + password + '@' + server + '/' + db_name)

    Session = sessionmaker(bind=enginedb)
    session = Session()
    Base = declarative_base()

    def save(models):
        Db.session.add(models)
        Db.session.commit()
    
    def show_all(models):
        data = Db.session.query(models).all()
        return data

    
    show = session