Title: Redis 常见使用场景 Demo
Date: 2016-03-20 14:16
Category: redis
Tags: redis, database, nosql
Summary: Redis 是一个基于内存的“数据结构”存储，可以用作: 数据库，缓存，消息管道。我们通过 demo 演示来理解这几个名词。

## 什么是 Redis？

官网的回答是：

    Redis is an open source (BSD licensed), in-memory data structure store,
    used as database, cache and message broker

基于内存的“数据结构”存储，可以用作：

- 数据库
- 缓存
- 消息管道

我们通过 demo 演示来理解这几个名词。

## 安装

Mac:
```bash
$ brew install redis
```

**澄清**

很多攻略给出的方法是: 编译安装。其实没必要。

这是以前官网推荐的方式，理由是 brew / apt-get 安装的版本太老。
实测，当前 brew 安装的就是最新 stable 版 3.07，所以无需编译安装。

编译安装：

```bash
wget http://download.redis.io/releases/redis-stable.tar.gz
tar xzf redis-stable.tar.gz
cd redis-stable/
make
sudo make install
```

## 基本用法

#### 开启服务器

```bash
$ redis-server
```

如果要运行在后台，在命令后加一个 `&` ，即：`redis-server &`


打开另外一个终端，
运行命令行界面（Command Line Interface，简称 cli)，连接到 Server
```bash
$ redis-cli
127.0.0.1:6379> ping
PONG
```

发送 ping，回复 pong，则表示链接成功。

否则
```bash
127.0.0.1:6379> ping
Could not connect to Redis at 127.0.0.1:6379: Connection refused
```

#### Key-Value 存储

使用 GET / SET 命令，key 和 value 都是 string

```bash
127.0.0.1:6379> set name jackon
OK
127.0.0.1:6379> get name
"jackon"
127.0.0.1:6379> set desc I'm Jackon
Invalid argument(s)
127.0.0.1:6379> set desc "I'm Jackon"
OK
```

#### 常用命令 keys ／ flushdb / del

`keys *` 查看所有 key，此处，`*` 是通配符.
查看所有以 `user_` 开头的 key，命令为 `keys user_*`

`del key` 删除 key 及其 value

`flushdb` 清空数据库。

`save` 命令与 `dump.rdb` 文件:
Redis 定期执行 save 命令，数据默认写入启动目录的 `dump.db` 文件。
下次启动 redis 时，会加载 dump.db 里的数据


个人的使用感触是，

在 redis 里操作一段时间以后，
基本记不清已经有多少 key 了，
一些笔记复杂的命令执行过后，需要看下对应的 key / value 是否符合预期。
此时，`keys *` 就很有用。

开发阶段，为了保证每次运行，代码执行结果一致，可以先 flushdb 一下。
注意，如果是跟其他人共用一个 db，就不要轻易 flushdb 了。

如果自己只用了三两个 key，每次代码执行时，del 精准的删掉这几个 key 就可以了。


```bash
127.0.0.1:6379> keys *
1) "age"
2) "desc"
3) "name"
127.0.0.1:6379> keys *e
1) "name"
2) "age"
127.0.0.1:6379> del name
(integer) 1
127.0.0.1:6379> keys *
1) "age"
2) "gender"
127.0.0.1:6379> flushdb
OK
127.0.0.1:6379> keys *
(empty list or set)
```

#### 编程语言接入－－Python 为例

搭建基础的 Python 开发环境，参考[搭建 PYTHON 开发环境](http://jackon.me/posts/python-dev-env/)

安装 Python 的 redis 包：
```bash
$ pip install redis
Collecting redis
  Downloading redis-2.10.5-py2.py3-none-any.whl (60kB)
    100% |████████████████████████████████| 61kB 68kB/s
Installing collected packages: redis
Successfully installed redis-2.10.5
```

Python 代码，文件名: papapa.py

```python
# -*- Encoding: utf-8 -*-
import redis  # python 语法要求，使用之前需要 import

# 使用默认的 IP/port 与 Redis 建立链接
r = redis.StrictRedis()
# 使用制定的 IP/port 与 Redis 建立链接
# 127.0.0.1 是本机 IP, Redis 默认端口 6379
r2 = redis.StrictRedis(host='127.0.0.1', port=6379)

r.set('name', 'jackon')
print 'name is %s' % r.get('name')

print 'get name by r2: name=%s' % r2.get('name')
```

运行 papapa.py 文件，执行的命令与结果

```bash
$ python papapa.py
name is jackon
get name by r2: name=jackon
```

#### 复杂数据结构

- List: 列表(链表)
- Set: 集合
    与列表的区别是，集合内的元素不重复
- Sorted set 有序集合
    与 set 相似，每个元素对应一个 score(浮点数)，用于排序
- Hash 哈希表

Redis 命令虽然多，但都遵循一个很好的模式。

- SET 命令以 S 开始
- 有序集合以 H 开始
- 哈希表以 Z 开始
- 列表，以 L(左)或 R(右) 开始，取决于操作方向。

Redis 里的数据结构, 有非常严格的数学概念. 值得深入研究.
比如, 统计 set 内元素的个数, 命令是 scard, 而不是常见的 size / length 一类.
card 是 cardinality 的缩写, 一个数学术语.  中文是`基数`

[Redis 官方文档](http://redis.io/topics/data-types-intro)

简单的演示几个命令, 不做深入介绍.
后续会出一个 Redis 数据结构的专题.

```bash
127.0.0.1:6379> FLUSHDB  # 清空演示数据库,避免已有干扰
OK
127.0.0.1:6379> sadd total 1  # 集合 total 内添加一个元素
(integer) 1  # 新增 1 个元素. 无需手动提前初始化一个空的 total 集合.
127.0.0.1:6379> sadd total 1 2 3 4 5  # 添加 5 个元素.
(integer) 4  # 新增 4 个元素
127.0.0.1:6379> smembers total  # set 内所有元素
1) "1"
2) "2"
3) "3"
4) "4"
5) "5"
127.0.0.1:6379> scard total  # set 内元素个数
(integer) 5
```

#### 缓存与 TTL

TTL -- 生存时间(Time To Live)

TTL 的概念, 在 HTTP 协议里, 用的很多.

Redis 里的术语, 叫: 到期功能.
即 set 命令设置 key / value 时，可以为 key 设置一个到期时间，比如 30秒。
30 秒后，Redis 自动删除这个键值对。其他的键值对不受影响。

到期功能，有助于避免总的键集无限增长。

基本命令:

- `SETEX key seconds value`
    设置 key / value, 生存时间为 seconds
- `ttl key`
    查询 key 的生存时间
    返回值及其含义
    - `-2` key 不存在
    - `-1` key 存在, 但没有过期时间
    - 正整数, 剩余的生存时间


用法演示：

```bash
27.0.0.1:6379> setex ice 10 "I'm melting..."  # ice 的 value 是 I'm melting...  保存 10 秒
OK
127.0.0.1:6379> ttl ice  # 剩余生存时间
(integer) 8  # 剩余 8 秒. 说明我的手速很快, 敲这些命令, 只用了 2 秒. :D
127.0.0.1:6379> get ice  # 获取 ice 的 value
"I'm melting..."
127.0.0.1:6379> exists ice  # 查询 ice 是否存在
(integer) 1  # 存在
127.0.0.1:6379> ttl ice
(integer) -2  # 无效值, 不存在了
127.0.0.1:6379> exists ice  # 查询 ice 是否存在
(integer) 0 # 不存在了
127.0.0.1:6379> get ice
(nil)
```

重新设置相同的值，会覆盖之前的数据，TTL 重新开始倒计时。
```bash
127.0.0.1:6379> setex ice 10 "I'm melting..."
OK
127.0.0.1:6379> ttl ice
(integer) 8
127.0.0.1:6379> setex ice 10 "I'm melting..."
OK
127.0.0.1:6379> ttl ice
(integer) 9
```

**黑科技：当 Redis 的 TTL 遇到了爬虫**

```python
# -*- Encoding: utf-8 -*-
import redis
import time

r = redis.StrictRedis()
r.flushdb()

# 发送 http 消息的函数
def req():
    time.sleep(1)
    print 'requesting jackon.me...'


lock_name = 'http-lock'  # 锁的名字, 可以为不同的 网站 / 页面类型设置不同的锁
INTERVAL = 3  # 相邻 http 请求的间隔秒数. 访问速度速度太快, 容易被网站屏蔽.

while True:  # 循环访问
    t = r.ttl(lock_name)  # lock_name 的生存时间, 即为仍需等待的时间
    if t > 0:  # 锁存在, 需要 sleep 消耗时间
        print 'sleep %s seconds' % t
        time.sleep(t)

    # 开始新的请求之前, 设置新的锁.
    r.setex(lock_name, INTERVAL, 'locking')
    req()  # 请求
```

一旦爬虫被封，进入 redis，setex 一下 'http-lock' 的 TTL。
爬虫自动进入休眠状态。

注意, 这个代码没有处理 ttl 返回 -1 的情况.

一般的爬虫代码, 是先 request, 再 sleep INTERVAL 秒.
所以, 实际的间隔时间超过预期, 抓取速度下降.

#### 发布 － 订阅

如此简单，以至于任何文字都是多余的。

不需要提前初始化一个空的频道.
第一个订阅者订阅时,  自动创建频道.

- 2 个客户端(人) 订阅了 python-cn 频道.
- 另外 1 个人, 发布了一条消息: Vim is the best editor.
- 2 个订阅者都收到了消息. 一般, 他们会进入 `沸腾的撕逼` 的状态.
- 1 个人在 phper 的频道里发布了一条消息: PHP 的是 拍黄片 的缩写.
- python-cn 的订阅者都没有收到消息.

看图
![redis-sub-pub](https://raw.githubusercontent.com/JackonYang/IOut.me/master/images/redis/redis-sub-pub.png)
