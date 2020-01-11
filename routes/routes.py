from routes import regius
from controller import controller

regius.add_link('/', controller.Index)
