Title: 搭建 Python 开发环境
Date: 2013-09-02 14:16
Category: python
Tags: python, install
Summary: win7 / ubuntu 下 Python 开发环境搭建


开发环境主要包括：

- 运行环境: python2.7
- 类库管理工具: pip
- 常用类库.

windows 环境搭建
----------------

#### python

python 主要包括 2.x 和 3.x 两个大版本，代码之间不兼容。
推荐使用 Python2.7，类库较为丰富，安装相对简单。

1. [下载 python][download-python] 并安装。
2. [设置环境变量][set-env] PATH 中添加 python 安装路径，默认为 `C:\python27`

#### setuptools

1. [下载 setuptools][download-setuptools] 并解压
2. DOS 下进入解压目录执行 `python setup.py install`

#### pip

1. [下载 pip][download-pip] 并解压
2. DOS 下进入解压目录执行 `python setup.py install`
3. [设置环境变量][set-env]，PATH 中添加 pip 的路径，默认为 `c:\python27\Scripts`

#### Notes for 小白

1. 环境变量  
    `环境变量` 是操作系统搜索可执行程序的路径.  
    如果不配置, 命令行里输入 python / pip 时, 就会提示找不到 python 程序.
2. 如何执行 python 程序  
    通过命令行进入待执行的代码所在路径, `python filename.py` 执行 python 程序.
3. 命令行里如何切换路径  
    分两种情况  
    不更换盘符, 比如 C 盘切换到 C 盘的另一个路径, 使用 `cd target/path`  
    更换盘符, 比如 C 盘切换到 D 盘. 先用 `D:\` 切换盘符. 然后在 D 盘内切换路径.
4. 如何安装第三方类库  
    命令行执行: `pip install lib-name`


[download-python]: http://www.python.org/getit/
[download-setuptools]: https://pypi.python.org/pypi/setuptools/1.1
[download-pip]: https://pypi.python.org/pypi/pip
[set-env]: http://zhidao.baidu.com/question/187573577.html


Ubuntu 环境搭建
---------------

```shell
$ sudo apt-get install -y python python-setuptools python-dev
$ sudo easy_install -U distribute
$ sudo apt-get install python-pip
```

如果 python-dev 未安装,
使用 easy_install or setup.py 时报错:   
`command 'gcc' failed with exit status 1`

Ubuntu 下开发环境完善
---------------------

一些类库, 依赖的 package 无法通过 pip 自动安装.

ubuntu 下的类库整理如下:

#### lib for apache2/mysql

```shell
$ apt-get install libapache2-mod-python, libmysqlclient-dev
```

如果 libmysqlclient-dev 未安装，安装 mysql-python 时报错：  
`EnvironmentError: mysql_config not found`

#### flake8

```shell
$ sudo pip install flake8
```
