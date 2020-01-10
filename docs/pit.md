* #### 2019-12-24
多级菜单自动创建，目前只能手动创建二级菜单

* #### 2019-12-25
flask使用flask_script映射模型，在模型反转字段，两个模型字段相同冲突，造成数据库映射失败

* #### 2019-12-26
在没有选择一级目录的情况下不能成功完成笔记，默认为无需要自己选择已经有的课程归属

`render_template`传参时，一直显示最后的一个参数未定义，可能是一次性传的参数过多

* #### 2020-01-02
`<texterea>`标签和`<pre>`标签在用于输入和显示时，不要换行或者空格，不然会有奇怪的空格

后台数据库的html在渲染时需要添加`safe`过滤器


* #### 2020-01-06
`send_from_directory`注意传递的是否为绝对路径，返回404


- #### 2020-01-10
    - 文件上传时有中文
    - 文件删除时文件夹文件不会自动删除
    
- 上传时文件名有中文解决，修改`secure_filename`源码
    - `\venv\Lib\site-packages\werkzeug\utils.py`修改`secure_filename`函数
    
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

    if (
        os.name == "nt"
        and filename
        and filename.split(".")[0].upper() in _windows_device_files
    ):
        filename = "_" + filename

    return filename
```