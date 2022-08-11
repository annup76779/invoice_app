from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///invoice.db"
    MIGRATION_DIR = "./migrations"

    # jwt stuff is done here
    JWT_SECRET_KEY = 'u6weMMZ8E2_qoVY3aW9uU9Mco6osJjLfjDj3gR_RA_dG8CAxsNQEBi4ZbpPIqOGcM0ErguxjpSE' # set this later into environment variable
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30 * 5)
    JWT_QUERY_STRING_NAME = "token"
    JWT_QUERY_STRING_VALUE_PREFIX = "Bearer "

class Development(Config):
    pass

class Production(Config):
    pass

class Test(Config):
    pass