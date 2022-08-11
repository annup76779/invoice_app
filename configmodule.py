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
    SQLALCHEMY_DATABASE_URI = "postgres://hnzofmxxtaylfk:caa68de4b2ca14b21d1b362f190d6913d8ca0f83ac83755bf7cf400e0f626873@ec2-3-224-8-189.compute-1.amazonaws.com:5432/d9avpngqkt0eai"

class Test(Config):
    pass