from routes import regius
from controller import controller

regius.add_link('/', controller.Index)
regius.add_link('/halo/{name}', controller.Name)
regius.add_link('/redirect', controller.SampleRedirect)