import os


class DevConfig(object):
    "dev config class"
    SECRET_KEY = os.urandom(24)
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = \
        "postgresql+psycopg2://postgres:111111@localhost:5432/note"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 文件上传大小限制,若大于16M，抛出RequestEntityTooLarge异常
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
