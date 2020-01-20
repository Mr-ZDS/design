from flask import session
from sqlalchemy import extract

from note.models.course import Course2, Upload


# 笔记按月归档,返回归档字典
def monthly_archive():
    user_id = session.get('user_id')
    # 返回字典格式: res = {month:[course2,upload], 1:[], 2:[]}
    res = {}
    for month in range(1, 13):
        query = Course2.query.filter(
            extract('month', Course2.create_time) == month)
        query = query.filter(Course2.user_id == user_id).all()
        visit = []
        for course2 in query:
            visit.append(course2)
        res[month] = visit
    return res


# 文件归档,返回字典
def upload_archive():
    user_id = session.get('user_id')
    res = {}
    for month in range(1, 13):
        query = Upload.query.filter(
            extract('month', Upload.create_time) == month)
        query = query.filter(Upload.user_id == user_id).all()
        visit = []
        for upload in query:
            visit.append(upload)
        res[month] = visit
    return res


# 图片上传限制格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[
        1].lower() in ALLOWED_EXTENSIONS