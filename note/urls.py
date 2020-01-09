# -*- coding: utf-8 -*-

from note.views.communicate import communicate_router
from note.views.index import index_router
from note.views.note import note_router
from note.views.user import user_router


routers = (
    (index_router, "/"),
    (user_router, "/user"),
    (communicate_router, "/communicate"),
    (note_router, "/note")
)
