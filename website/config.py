class BaseConfig:
    SECRET_KEY = ""  # should be set by runner (doesn't matter unless hosted)
    SQLALCHEMY_DATABASE_URI = "sqlite:///local.db"
