import os
from functools import wraps

from note.models.course import Upload


# 在删除一个文件之前删除文件夹中存在的但是数据库没有标识的文件
def delete_file(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        # 数据库文件列表
        # file_dir = Upload.query.with_entities(Upload.file_name)
        upload = Upload.query.all()
        file_dir = []
        for visit in upload:
            file_dir.append(visit.file_name)
        # 当前文件路径
        basepath = os.path.dirname(__file__)
        # 文件所在路径
        dirpath = os.path.join(basepath[:-5], 'static/upload_file')
        for filename in os.listdir(dirpath):
            if filename not in file_dir:
                file_delete = os.path.join(basepath[:-5], 'static/upload_file',
                                           filename)
                if os.path.exists(file_delete):
                    os.remove(file_delete)
        return func(*args, **kwargs)

    return decorated
