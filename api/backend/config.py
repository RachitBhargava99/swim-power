import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = '0917b13a9091915d54b6336f45909539cce452b3661b21f386418a257883b30a'
    ENDPOINT_ROUTE = ''
    CURRENT_URL = 'https://spindler.thinger.appspot.com/'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    PROJECT_ID = os.environ.get('PROJECT_ID')
    DATA_BACKEND = os.environ.get('DATA_BACKEND')
#    CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
#    CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
#    CLOUDSQL_DATABASE = os.environ.get('CLOUDSQL_DATABASE')
#    CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
#    SQLALCHEMY_DATABASE_URI = (
#        'mysql+pymysql://{user}:{password}@localhost/{database}?unix_socket=/cloudsql/{connection_name}').format(
#        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD, database=CLOUDSQL_DATABASE,
#        connection_name=CLOUDSQL_CONNECTION_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_URL = 'https://images-api.nasa.gov/'
    SEARCH_URL = 'search'
    META_DATA_URL = 'metadata/'
    MEDIA_DATA_URL = 'asset/'
    IMG_URL = 'asset/img/'
