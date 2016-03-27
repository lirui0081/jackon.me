Title: Redis 常见使用场景 Demo
Date: 2016-03-20 14:16
Category: redis
Tags: redis, database, nosql
Summary: Redis 是一个基于内存的“数据结构”存储，可以用作: 数据库，缓存，消息管道。我们通过几个 demo 来理解基本概念。

## 什么是 Redis？

官网的回答是：

    Redis is an open source (BSD licensed), in-memory data structure store,
    used as database, cache and message broker

基于内存的“数据结构”存储，可以用作：

- 数据库
- 缓存
- 消息管道

我们通过几个 demo 来理解基本概念。

## 安装

Mac:
```bash
$ brew install redis
```

**澄清**

很多攻略给出的方法是: 编译安装, 命令如下

```bash
wget http://download.redis.io/releases/redis-stable.tar.gz
tar xzf redis-stable.tar.gz
cd redis-stable/
make
sudo make install
```

曾经，这是官网推荐的方式，因为 brew / apt-get 安装的版本太老。
实测，当前 brew 安装的就是最新 stable 版 3.0.7，所以无需编译安装。

## 基本用法

#### 开启服务器

```bash
$ redis-server
```

如果要运行在后台，在命令后加一个 `&` ，即：`redis-server &`

打开另外一个终端，
运行命令行界面（Command Line Interface，简称 cli)，连接到 Server

`127.0.0.1:6379>` 是 redis-cli 的命令行提示符,
就像 Mac / Linux 下的 `jackon@local-ubuntu:~$` 一样.

**redis-cli 里的命令不区分大小写**

发送 ping，回复 pong，则表示链接成功。
```bash
$ redis-cli
127.0.0.1:6379> ping
PONG
```

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
127.0.0.1:6379> set desc Web Developer  # value 里面有空格, redis 就搞不定了.
Invalid argument(s)
127.0.0.1:6379> set desc "Web Developer"  # 一个 " 解决问题
OK
```

#### 实用但被忽略的基础命令

- `keys *` 查看所有 key，此处，`*` 是通配符.
    查看所有以 `user_` 开头的 key，命令为 `keys user_*`
- `del key` 删除 key 及其 value
- `flushdb` 清空数据库。

个人的使用感触是，

在 redis 里操作一段时间以后，
基本记不清已经有多少 key 了，
一些比较复杂的命令执行过后，需要看下执行结果是否符合预期。
比如, 批量添加了 100 个 key  / value 对.
此时，`keys *` 就很有用。

开发阶段，为了保证每次运行，代码执行结果一致，可以先 flushdb 清空历史数据。
注意，如果是跟其他人共用一个 db，就不要轻易 flushdb 了。

如果自己只用了三两个 key，每次代码执行时，del 精准的删掉这几个 key 就可以了。

演示:

```bash
127.0.0.1:6379> keys *  # 已经提前添加了 3 个 key / value
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

#### `dump.rdb` 文件是什么鬼

Redis 会定期把内存里的数据写入硬盘备份.
默认, 写入启动目录下的 `dump.db` 文件.
下次启动 redis 时，会加载 dump.db 里的数据.

`save` 命令会触发一次 备份.

```bash
127.0.0.1:6379> save
OK
```

 dump.db 文件更新, 同时, Server 端的 log 日志出现:
```bash
5247:M 24 Mar 10:37:53.534 * DB saved on disk
```

## 编程语言接入 -- Python 为例

搭建基础的 Python 开发环境，参考 [搭建 PYTHON 开发环境](http://jackon.me/posts/python-dev-env/)

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
# 使用指定的 IP/port 与 Redis 建立链接
# 127.0.0.1 是本机 IP, Redis 默认端口 6379
r2 = redis.StrictRedis(host='127.0.0.1', port=6379)

r.set('name', 'jackon')  # 用第一个连接写入数据
print 'name is %s' % r.get('name')  # 第一个连接可以读取数据

print 'get name by r2: name=%s' % r2.get('name')  # 第二个连接也可以读取数据
```

运行 papapa.py 文件，执行的命令与结果

```bash
$ python papapa.py
name is jackon
get name by r2: name=jackon
```

## 复杂数据结构

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
比如, 统计 set 内元素的个数, 命令是 `scard`, 而不是常见的 size / length 一类.
card 是 cardinality 的缩写, 一个数学术语.  中文是`基数`

[Redis 官方文档](http://redis.io/topics/data-types-intro)

简单的演示几个命令, 不做深入介绍.
后续会出一个 Redis 数据结构的专题.

```bash
127.0.0.1:6379> FLUSHDB  # 清空演示数据库,避免已有数据干扰
OK
127.0.0.1:6379> sadd total 11  # 集合 total 内添加一个元素
(integer) 1  # 新增 1 个元素. 无需手动提前初始化一个空的 total 集合.
127.0.0.1:6379> sadd total 11 12 13 14 15  # 添加 5 个元素.
(integer) 4  # 新增 4 个元素. 其中, 11 是重复的.
127.0.0.1:6379> smembers total  # set 内所有元素
1) "11"
2) "12"
3) "13"
4) "14"
5) "15"
127.0.0.1:6379> scard total  # set 内元素个数
(integer) 5
```

## 缓存与 TTL

TTL -- 生存时间(Time To Live).
熟悉 HTTP 协议的, 应该对 ttl 不陌生.

Redis 里的术语, 叫: 到期功能.
即设置 key / value 时，可以为 key 设置一个到期时间，比如 30秒。
30 秒后，Redis 自动删除这个键值对。其他的键值对不受影响。

到期功能，有助于避免总的键集无限增长。

#### 常用命令

- `SETEX key seconds value`
    设置 key / value, 生存时间为 seconds
- `TTL key` 查询 key 的生存时间
    返回值
    - `-2` key 不存在 (到期已删除)
    - `-1` key 存在, 但没有过期时间
    - 正整数, 剩余的生存时间, 单位为 秒

用法演示：

```bash
27.0.0.1:6379> setex ice 10 "I'm melting..."  # ice 的 value 是 I'm melting...  保存 10 秒
OK
127.0.0.1:6379> ttl ice  # 剩余生存时间
(integer) 8  # 剩余 8 秒. 手速有多快! 敲这些命令, 只用了 2 秒 :D
127.0.0.1:6379> get ice  # 获取 ice 的 value
"I'm melting..."
127.0.0.1:6379> exists ice  # 查询 ice 是否存在
(integer) 1  # 存在
127.0.0.1:6379> ttl ice
(integer) -2  # ice 不存在, 已被删除
127.0.0.1:6379> exists ice  # 再次查询 ice 是否存在
(integer) 0 # 不存在
127.0.0.1:6379> get ice  # 不存在的 key, 返回空(nil)
(nil)
```

重新设置相同的值，会覆盖之前的数据，TTL 重新开始倒计时。
```bash
127.0.0.1:6379> setex ice 10 "I'm melting..."
OK
127.0.0.1:6379> ttl ice
(integer) 8
127.0.0.1:6379> setex ice 20 "I'm melting..."
OK
127.0.0.1:6379> ttl ice
(integer) 19
```

#### 黑科技：当 Redis TTL 遇到了爬虫

```python
# -*- Encoding: utf-8 -*-
import redis
import time

r = redis.StrictRedis()
r.flushdb()

# 发送 http 消息的函数
def req():
    print 'requesting jackon.me...'
    time.sleep(1)  # 假设, 我们的网络环境, 发送收发一次 http, 需要 1 秒钟.


lock_name = 'http-lock'  # 锁的名字, 可以为不同的 网站 / 页面类型 设置不同的锁
INTERVAL = 3  # 相邻 http 请求的间隔秒数. 访问速度速度太快, 容易被网站屏蔽.

while True:  # 循环访问
    t = r.ttl(lock_name)  # lock_name 的生存时间, 即, 仍需等待的时间
    if t > 0:  # 锁存在, 剩余存活时间 t 秒
        print 'sleep %s seconds' % t
        time.sleep(t)  # 等待 t 秒

    # 开始新的请求之前, 设置新的锁.
    r.setex(lock_name, INTERVAL, 'locking')
    req()  # 请求
```

一旦爬虫被封，进入 redis, 执行以下命令, 爬虫休眠 1 小时

```bash
127.0.0.1:6379> setex http-lock 3600 locking
OK
```

一般的爬虫, 是先 request, 再 sleep INTERVAL 秒.
所以, 实际的间隔时间超过预期, 抓取速度下降.

注意, 这段代码仅用于演示核心思路, 存在几个坑

- 没有处理 ttl 返回 -1 的情况
- 代码执行 `r.setex(...)`时, 可能会覆盖 redis-cli 手动添加的休眠指令.

## 发布 / 订阅

如此简单，以至于任何解释都是多余的。

#### 案例背景

    A, B, C 三个程序员, python-cn 和 phper 是 2 个聊天室.
    我们让前者沸腾, 后者哭泣.

#### 演示步骤

1. A 通过 `subscribe` 命令订阅 python-cn 频道.
2. B 通过 `subscribe` 命令, 在另外一个 terminal 中订阅 python-cn 频道.
3. C 通过 `publish` 命令在 python-cn 频道里发布了一条消息: Vim is the best editor.
    频道订阅者(A 和 B)都收到了消息. 一般, 他们会进入 `沸腾的撕逼` 的状态.
4. C 又在 phper 的频道里发布了一条消息: PHP is short for pai huang pian(PHP 的是 拍黄片 的缩写)
    python-cn 的订阅者都没有收到消息.
    如果有 php 码农订阅了 phper 频道, 他的女朋友恰好路过看到了这条消息, 他会哭. 

注意: 
不需要提前初始化一个空的频道.
第一个订阅者订阅时,  自动创建频道.

看图
![redis-sub-pub](https://raw.githubusercontent.com/JackonYang/IOut.me/master/images/redis/redis-sub-pub.png)
