### 类似读书笔记的demo

实现的功能
- [ ] 用户管理 
  - [x] 用户注册
  - [x] 用户登录与注销
  - [ ] 用户个人中心
    - [x] 头像上传和显示
    - [x] 个人资料设置
    - [ ] 修改密码 

- [x] 交流区
  - [x] 交流发言(含标题、集成CKEditor富文本编辑)
  - [x] 交流区展示(创建时间排序)
  - [x] 文本详情
  - [x] 交流评论
  - [x] 交流区个人中心统计
  - [x] 按评论数倒序展示
  

- [x] 笔记区
  - [x] 一级笔记
  - [x] 二级笔记
  - [x] 文件上传(限制格式)、在线、下载
  - [x] 笔记、文件删除
  - [x] 展示、详情
  - [x] 笔记编辑(权限，内容等更改)
  - [x] 非公开笔记具有绝对管理权
  - [x] 按月归档
  
- [x] 最高管理员权限

- 暂定：
    - username为`admin`的用户设置为管理员，即下载后立即注册这个用户名,可设置id或者号码等作为管理员标识符


### 部署安装
#### 1、下载
```
git clone https://github.com/Mr-ZDS/Grad.git
```

#### 2、安装virtualenv
```
pip install virtualenv
```

#### 3、进入文件夹，创建虚拟环境
```
python -m venv venv
```

#### 4、激活虚拟环境
```
venv\Scripts\activate
```

#### 5、更新依赖
```
pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

#### 6、若没有`upload_file`文件夹，在`static`目录创建`upload_file`文件夹

#### 7、为了使上传的文件名能包含中文，需要修改`secure_filename`函数的源码，该函数位于`\venv\Lib\site-packages\werkzeug\utils.py`
修改后的函数如下：
```
def secure_filename(filename):
    if isinstance(filename, text_type):
        from unicodedata import normalize

        filename = normalize("NFKD", filename).encode("utf-8", "ignore")
        if not PY2:
            filename = filename.decode("utf-8")
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")

    _filename_ascii_add_strip_re = re.compile(r'[^A-Za-z0-9_\u4E00-\u9FBF.-]')
    filename = str(_filename_ascii_add_strip_re.sub('', '_'.join(
        filename.split()))).strip('._')

    # on nt a couple of special files are present in each folder.  We
    # have to ensure that the target file is not such a filename.  In
    # this case we prepend an underline
    if (
        os.name == "nt"
        and filename
        and filename.split(".")[0].upper() in _windows_device_files
    ):
        filename = "_" + filename

    return filename
```

#### 8、运行
```
flask run
```