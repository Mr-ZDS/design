import os

from flask import Blueprint, render_template, request, flash, redirect, session, \
    url_for, send_from_directory
from flask_login import login_required
import markdown
from werkzeug.utils import secure_filename

from note.extensions import db
from note.forms.course import Course1Form, UploadForm, Recourse1Form, \
    EditnoteForm
from note.models.course import Course1, Course2, Upload
from note.models.user import Users
from note.util.archive import monthly_archive
from note.util.decorators import delete_file

note_router = Blueprint("note", __name__)


@note_router.route('/home/')
def home():
    user_id = session.get('user_id')
    users = Users.query.filter(Users.id == user_id).first()
    course1 = Course1.query.filter(Course1.user_id == user_id).all()
    return render_template(
        'courses/home.html',
        course1=course1,
        users=users,
        res=monthly_archive()
    )


# 一级目录输入
@note_router.route('/one_directory/', methods=['GET', 'POST'])
@login_required
def one_directory():
    form = Course1Form()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(form.errors)
            return render_template('courses/one_directory.html', form=form)
        status = request.form.get('status')
        user_id = session.get('user_id')
        course1 = Course1(title=form.title.data, status=status)
        # 一个用户不能创建相同的一级目录
        if Course1.query.filter(Course1.title == form.title.data,
                                Course1.user_id == user_id).first():
            flash('该课程目录已经存在，请重新输入标题！！！')
            return render_template('courses/one_directory.html', form=form)
        users = Users.query.filter(Users.id == user_id).first()
        course1.users = users
        db.session.add(course1)
        db.session.commit()
        return redirect(url_for('note.home'))
    return render_template('courses/one_directory.html', form=form)


# @note_router.route('/one_directory/', methods=['GET', 'POST'])
# @login_required
# def one_directory():
#     if request.method == 'GET':
#         return render_template('courses/one_directory.html')
#     else:
#         user_id = session.get('user_id')
#         title = request.form.get('one_title')
#         status = request.form.get('status')
#         if len(title.strip()) == 0:
#             flash('标题不能为空！！！')
#             return render_template('courses/one_directory.html')
#         # 一个用户不能创建相同的一级目录
#         if Course1.query.filter(Course1.title == title,
#                                 Course1.user_id == user_id).first():
#             flash('该课程目录已经存在，请重新输入标题！！！')
#             return render_template('courses/one_directory.html')
#         courese1 = Course1(title=title, status=status)
#         users = Users.query.filter(Users.id == user_id).first()
# #         courese1.users = users
# #         db.session.add(courese1)
# #         db.session.commit()
# #         return redirect(url_for('note.home'))


# 二级课程笔记创建
@note_router.route('/record_course/', methods=['GET', 'POST'])
@login_required
def record_course():
    # 将一级目录传给前端
    user_id = session.get('user_id')
    visit = Course1.query.filter(Course1.user_id == user_id).all()
    if request.method == 'GET':
        return render_template('courses/record.html', course=visit)
    else:
        title = request.form.get('real_title')
        belong = request.form.get('belong')
        status = request.form.get('course_status')

        # 标题为空时重新输入
        if len(title.strip()) == 0:
            flash('标题不能为空！！！')
            return render_template('courses/record.html', course=visit)
        # 个人没有一级目录时需要重新创建
        if belong == '0':
            flash('请先选择或创建课程归属！！！')
            return render_template('courses/record.html')
        # 个人同级标题不能重复
        course1 = Course1.query.filter(Course1.title == belong).first()
        if Course2.query.filter(Course2.title == title,
                                Course2.user_id == user_id,
                                Course2.course1_id == course1.id).first():
            flash('此标题已经存在，请输入新的课程标题！！！')
            return render_template('courses/record.html')

        markdowns = request.form.get('TextContent')
        text = request.form.get('text_content')
        if len(markdowns.strip()) == 0 and len(text.strip()) == 0:
            flash('请输入笔记内容！！！')
            return render_template('courses/record.html', course=visit)
        elif len(markdowns.strip()) != 0 and len(text.strip()) != 0:
            flash('请只选择一种文本编辑方式！！！')
            return render_template('courses/record.html', course=visit)
        else:
            if len(markdowns.strip()) == 0:
                content = text
                html_content = text
            else:
                html = markdown.markdown(markdowns)
                html_content = html
                content = markdowns
            course2 = Course2(title=title, content=content, status=status,
                              html_content=html_content)
            users = Users.query.filter(Users.id == user_id).first()
            course2.users = users
            course2.course1 = course1
            db.session.add(course2)
            db.session.commit()
            return redirect(url_for('note.home'))


# 二级笔记目录展示
@note_router.route('/second_show/<course1_id>')
def second_show(course1_id):
    user_id = session.get('user_id')
    users = Users.query.filter(Users.id == user_id).first()
    course2 = Course2.query.filter(Course2.course1_id == course1_id,
                                   Course2.user_id == user_id).all()
    course1 = Course1.query.filter(Course1.user_id == user_id).all()
    uploads = Upload.query.filter(Upload.user_id == user_id,
                                  Upload.course1_id == course1_id).all()
    return render_template(
        'courses/home.html',
        course2=course2,
        course1=course1,
        uploads=uploads,
        users=users,
        res=monthly_archive()
    )


# 二级笔记展示
@note_router.route('/note_detail/<course2_id>')
def note_detail(course2_id):
    detail = Course2.query.filter(Course2.id == course2_id).first()
    return render_template('courses/detail.html', detail=detail)


# 文件上传限制格式
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'png', 'jpg', 'jpeg', 'py'}


def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[
        1].lower() in ALLOWED_EXTENSIONS


# 文件上传
@note_router.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    user_id = session.get('user_id')
    visit = Course1.query.filter(Course1.user_id == user_id).all()
    if request.method == 'GET':
        return render_template(
            'courses/upload.html',
            course=visit,
            form=form
        )
    else:
        f = request.files['file']
        if allow_file(f.filename):
            # 当前文件所在路径
            basepath = os.path.dirname(__file__)
            # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            upload_path = os.path.join(basepath[:-6], 'static/upload_file',
                                       secure_filename(f.filename))
            f.save(upload_path)
        else:
            flash('书籍格式错误或者上传错误！！！！')
            return render_template(
                'courses/upload.html',
                course=visit,
                form=form
            )

        belong = request.form.get('belong')
        status = request.form.get('file_status')
        file_name = form.file_name.data
        intro = form.file_intro.data

        # 个人没有选择一级目录时需要重新创建，默认为无
        if belong == '0':
            flash('请先选择或创建课程归属！！！')
            return render_template(
                'courses/upload.html',
                course=visit,
                form=form)
        # 同级目录下不能有相同的笔记名或文件名
        course1 = Course1.query.filter(Course1.title == belong).first()
        if Upload.query.filter(Upload.user_id == user_id,
                               Upload.course1_id == course1.id,
                               Upload.file_name == file_name).first() or \
                Course2.query.filter(
                    Course2.title == file_name,
                    Course2.user_id == user_id,
                    Course2.course1_id == course1.id).first():
            flash('此文件名或笔记已经存在！！！')
            return render_template(
                'courses/upload.html',
                course=visit,
                form=form
            )

        upload_file = Upload(file_name=file_name, intro=intro, status=status)
        users = Users.query.filter(Users.id == user_id).first()
        upload_file.users = users
        upload_file.course1 = course1
        db.session.add(upload_file)
        db.session.commit()
        return redirect(url_for('note.home'))


# 上传的文件查看
@note_router.route('/file_detail/<file_id>/')
def file_detail(file_id):
    uploads = Upload.query.filter(Upload.id == file_id).first()
    return render_template(
        'courses/file_detail.html',
        uploads=uploads
    )


# 下载文件
@note_router.route("/download/<path:filename>")
def download(filename):
    # 这里是下载目录
    basepath = os.path.dirname(__file__)
    dirpath = os.path.join(basepath[:-6], 'static/upload_file')
    # as_attachment=True 一定要写，不然会变成打开，而不是下载
    return send_from_directory(dirpath, filename, as_attachment=True)


# 在线观看
@note_router.route('/online/<path:filename>')
def online(filename):
    basepath = os.path.dirname(__file__)
    dirpath = os.path.join(basepath[:-6], 'static/upload_file')
    return send_from_directory(dirpath, filename, as_attachment=False)


# 二级笔记删除
@note_router.route('/note_delete/<note_id>')
def note_delete(note_id):
    course2 = Course2.query.filter(Course2.id == note_id).first()
    db.session.delete(course2)
    db.session.commit()
    user_id = session.get('user_id')
    users = Users.query.filter(Users.id == user_id).first()
    course1 = Course1.query.filter(Course1.user_id == user_id).all()
    return render_template(
        'courses/home.html',
        course1=course1,
        users=users,
        res=monthly_archive()
    )


# 文件删除
@note_router.route('/file_delete/<file_id>')
@delete_file
def file_delete(file_id):
    uploads = Upload.query.filter(Upload.id == file_id).first()
    # 数据库删除
    db.session.delete(uploads)
    db.session.commit()
    # 项目保存的文件删除
    basepath = os.path.dirname(__file__)
    file = os.path.join(basepath[:-6], 'static/upload_file', uploads.file_name)
    if os.path.exists(file):
        os.remove(file)

    user_id = session.get('user_id')
    users = Users.query.filter(Users.id == user_id).first()
    course1 = Course1.query.filter(Course1.user_id == user_id).all()
    return render_template(
        'courses/home.html',
        course1=course1,
        users=users,
        res=monthly_archive()
    )


# 直接删除整个一级课程目录
@note_router.route('/directory_delete/<course1_id>/')
def directory_delete(course1_id):
    courses2 = Course2.query.filter(Course2.course1_id == course1_id).all()
    for course2 in courses2:
        db.session.delete(course2)
        db.session.commit()
    course1 = Course1.query.filter(Course1.id == course1_id).first()
    db.session.delete(course1)
    db.session.commit()
    user_id = session.get('user_id')
    users = Users.query.filter(Users.id == user_id).first()
    course1 = Course1.query.filter(Course1.user_id == user_id).all()
    return render_template(
        'courses/home.html',
        course1=course1,
        users=users,
        res=monthly_archive()
    )


# 一级目录编辑
@note_router.route('/update_one_directory/<course1_id>',
                   methods=['GET', 'POST'])
def update_one_directory(course1_id):
    course1 = Course1.query.filter(Course1.id == course1_id).first()
    form = Recourse1Form()
    form.title.data = course1.title
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(form.errors)
            return render_template(
                'courses/update_one_directory.html',
                form=form
            )
        status = request.form.get('status')
        user_id = session.get('user_id')
        form1 = Recourse1Form()
        if Course1.query.filter(
                Course1.title == form1.title.data,
                Course1.user_id == user_id).first() and form1.title.data != form.title.data:
            flash('该课程目录已经存在，请重新输入标题！！！')
            return render_template(
                'courses/update_one_directory.html',
                form=form
            )
        course1.title = form1.title.data
        course1.status = status
        db.session.commit()
        return redirect(url_for('note.home'))
    return render_template('courses/update_one_directory.html', form=form)


# 笔记编辑、修改
@note_router.route('/edit_note/<course2_id>', methods=['GET', 'POST'])
def edit_note(course2_id):
    course2 = Course2.query.filter(Course2.id == course2_id).first()
    form = EditnoteForm()
    form.title.data = course2.title
    form.content.data = course2.content
    if request.method == 'GET':
        return render_template('courses/edit_note.html', form=form)
    else:
        if not form.validate_on_submit():
            flash(form.errors)
            return render_template('courses/edit_note.html', form=form)
        form1 = EditnoteForm()
        status = request.form.get('course_status')
        # 用户目录下不能有相同的笔记名
        if Course2.query.filter(
                Course2.course1_id == course2.course1_id,
                Course2.title == form1.title.data).first() and form1.title.data != form.title.data:
            flash('该笔记标题已存在！！！')
            return render_template('courses/edit_note.html', form=form)

        course2.title = form1.title.data
        course2.status = status
        course2.content = form1.content.data
        course2.html_content = markdown.markdown(form.content.data)
        db.session.commit()
        return redirect(url_for('note.home'))
