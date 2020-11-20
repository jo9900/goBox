import settings
from sqlalchemy.orm import sessionmaker
from models import *
from common import *
from datetime import datetime, timedelta


engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s' % (settings.USER, settings.PASSWORD,
                                                              settings.DATA_HOST, settings.DATABASE), echo=True, client_encoding='utf8')
Base.metadata.create_all(engine)