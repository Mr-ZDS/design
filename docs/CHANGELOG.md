### 2019-12-23
#### Added 建立项目结构，完成登录、注册、状态转换功能

#### 根目录
* `app.py`项目入口
* `manage.py`模型映射文件

#### `note`app文件
* `config`包   项目配置
* `models/user`  用户模型
* `view`包 路由视图
* `template` 模板渲染文件
* `static/css` css文件



### 2019-12-24
#### Added 增加用户`交流`和`评论`模型，及相关的视图及模板

### 2019-12-25
#### Added 新增`一级用户`模型，及相应的视图和模板
* `/note/static/editormd`  markdown集成

### 2019-12-26
#### Added 二级目录`title`显示
* `/note/templates/courses/one_directory.html`
* `/note/templates/courses/record.html`

#### Changed  二级模型更改，视图显示
* `/note/models/course.py`
* `/note/views/index.py`


### 2020-01-02
#### Added 后台html成功渲染，个别标签(表格等)还没完成
* `/note/templates/courses/detail.html`
* `/note/views/user.py`
* `/note/views/index.py`
* `/note/views/communicate.py`
* `/note/views/note.py`

#### Changed 更改为多蓝图文件
* `/note/views/note.py`


### 2020-01-06
#### Added 增加文件上传、下载相应的视图和界面
* `/note/template/upload.html`
* `/note/template/file_detail.html`
* `/note/static/css/upload.css`
* `/note/static/upload_file`文件夹

#### Changed
* `/note/models/course.py`  增加文件上传模型
* `/note/views/note.py`  增加相应功能视图


### 2020-01-07
#### Added  增加首页展示视图及相应界面，管理员为(username=admin)的用户
* `/note/template/index`包

#### Changed
* `/note/views/index.py`


### 2020-01-09
#### Added  增加表单，将原生表单转化为wtf表单
* `/note/forms/user.py`
* `/note/forms/communicate.py`
* `/note/forms/course.py`

#### Changed 将对应的原生表单改为`wtf`表单及其相应的视图、界面
* `/note/views/user.py`
* `/note/views/communicate.py`
* `/note/views/note.py`


### 2020-01-10
#### Changed  修改`secure_filename`函数源码，让上传时支持中文名
* `\venv\Lib\site-packages\werkzeug\utils.py`


### 2020-01-14
#### Add  新增头像更换功能、文章编辑功能及相应视图及界面;
* `/note/templates/users/reicon.html`
* `/note/templates/communicate/update_comm.html`

#### Changed
* `/note/models/user.py`  新增`icon`字段
* `/note/views/user.py`   头像更换路由
* `/note/views/communicate.py` 文章、笔记编辑