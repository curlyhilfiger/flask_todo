class Config(object):
    """ Config  """

    SECRET_KEY = "Blah-blah-blah"

    DEBUG = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:12345@localhost/todo"

    SESSION_COOKIE_SECURE = True


class DevelopmentConfig(Config):
    """ Dev config settings """

    DEBUG = True

    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    pass


key = Config.SECRET_KEY
