### 类似读书笔记的demo
目前实现的功能：
* 登录
* 注册
* 两种状态转化
* 课程发言
* 发言评论
* markdown/文本 写笔记
* 一级目录创建并显示
* 二级目录创建并成功渲染markdown
* 首页展示，笔记界面展示

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

#### 6、在`static`目录创建`upload_file`文件夹

#### 7、运行
```
flask run
```