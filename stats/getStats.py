import base
from stats import Stat
from games import Game
from jornadas import Jornada
from groups import Group
from seasons import Season
from leagues import League

import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(open('database_info_free.txt', 'r').read())
base.Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

start_time = time.time()

URL = 'http://competiciones.feb.es/estadisticas/Resultados.aspx?g=1&t=2019'
le = League('LEB ORO', 'Senior', 'male', True, 'processing')
League.scrapSeasons_statsLEB(URL, le, session)
session.commit()

URL = 'http://competiciones.feb.es/estadisticas/Resultados.aspx?g=4&t=2019'
le = League('Liga Femenina', 'Senior', 'female', True, 'processing')
League.scrapSeasons_statsLEB(URL, le, session)
session.commit()

URL = 'http://competiciones.feb.es/estadisticas/Resultados.aspx?g=2&t=2017'
le = League('LEB PLATA', 'Senior', 'male', True, 'processing')
League.scrapSeasons_statsLEB(URL, le, session)
session.commit()

URL = 'http://competiciones.feb.es/estadisticas/Resultados.aspx?g=9&t=2019'
le = League('Liga Femenina 2', 'Senior', 'female', True, 'processing')
session.add(le)
League.scrapSeasons_statsLEB(URL, le, session)
session.commit()

URL = 'http://competiciones.feb.es/estadisticas/Resultados.aspx?g=3&t=2019'
le = League('Liga EBA', 'Senior', 'male', True, 'processing')
League.scrapSeasons_statsLEB(URL, le, session)
session.commit()

print(time.time()-start_time)