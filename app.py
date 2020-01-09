import os

from note import create_app

config_name = os.getenv('note_cfg'.upper()) or "dev"
app = create_app(config_name)
