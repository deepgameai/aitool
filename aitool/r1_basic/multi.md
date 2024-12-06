# pool_map，pool_starmap，multi_map
- 修改**1行**代码将顺序执行改造为并行执行。
- 三种方法都**按序输出**，多次运行获得的结果**顺序是一致**的。
- 三种方法都基于multiprocess库，而非multiprocessing库。因为multiprocessing有[设计缺陷](https://bugs.python.org/issue25053)。）


**NOTE** 
1、被调用函数最好只有1个参数，即，将原本的输入参数用一个list或dict包装一下   
2、是进程级并行，会复制整个进程，最好优化一下进程里内存消耗。
3、python的线程级并行并没有实际用到多核，所以一下均使用的进程级并行

**顺序执行的写法**：
```python
def toy(x, y=1):
    # 需要被多次调用的函数
    return x, y

for result in map(toy, range(3)):
    print(result)
```

**并行执行的3种写法**：
```python
# 提供3种实现方式：pool_map，pool_starmap，multi_map
# 3种方式是几乎等效的，在参数不复杂的情况下推荐使用pool_map
from aitool import pool_map, pool_starmap, multi_map

def toy(x, y=1):
    # 需要被多次调用的函数
    return x, y

# 方法1：
for result in pool_map(toy, range(3)):
    print(result)

# 方法2：
for result in pool_starmap(toy, [[0, 1], [1, 1], [2, 1]]):
    print(result)

# 方法3：
for result in multi_map(toy, range(3)):
    print(result)
```

### pool_map、pool_starmap、multi_map的对比

| 方法 | 实现方案 | 优点 | 缺点 | 耗时（秒） |
| --- | --- | --- | --- |
| - | 按序循环执行 | - | - | 987.171 |
| pool_map | 封装pool.map | 稳定 | 参数不灵活 | 87.051 |
| pool_starmap | 封装pool.starmap | 稳定 | 参数不灵活 | 87.047 |
| multi_map | 封装pool.apply_async | 参数灵活 | 不稳定 | 83.348 |

评测详情请参考：[pool_map和pool_starmap和multi_map的对比](#pool_map和pool_starmap和multi_map的对比)。

### 环境配置
```shell script
pip install aitool --upgrade
```

### multi_map参数灵活
```python
from aitool import multi_map

def toy(x, y=1):
    return x, y

for result in multi_map(toy, [1, [2, 3], {'x': 4}, {'x': 6, 'y': 7}]):
    print(result)
```

### multi_map和multi和get_functions
> multi_map基于multi和get_functions实现

- [multi基本用法](#multi基本用法)
- [get_functions基本用法](#get_functions基本用法)
- [get_functions通常用法](#get_functions通常用法)
- [multi通常用法](#multi通常用法)

### multi基本用法

```python
from time import sleep
from random import random
from aitool import multi


def toy_1(x=1, y=2):
    sleep(random())
    return x, y


def toy_2(x=3, y=4):
    sleep(random())
    return x, y


for result in multi([toy_1, toy_2], ordered=True):
    print(result)
```
> 输出
```text
(1, 2)
(3, 4)
```

### get_functions基本用法
- 需要并发执行的往往是同一个函数，只不过参数不一样。  
- get_functions可以基于参数列表生成函数列表。

```python
from time import sleep
from random import random
from aitool import get_functions


def toy(x):
    sleep(random())
    return x


for function in get_functions(toy, range(3)):
    print(function())
```
> 输出
```text
0
1
2
```

### get_functions通常用法
- 支持多种灵活的传参方式

```python
from time import sleep
from random import random
from aitool import get_functions


def toy(x=-1, y=1):
    sleep(random())
    return x, y


condition = [None, 1, [2, 3], {'x': 4}, {'x': 6, 'y': 7}]
for function in get_functions(toy, condition):
    print(function())
```
> 输出
```text
(-1, 1)
(1, 1)
(2, 3)
(4, 1)
(6, 7)
```

### multi通常用法
- 先用get_functions获取函数列表  
- 再用multi多进程执行

```python
from aitool import get_functions, multi


def toy(x, y=1):
    return x, y


def bauble(x=1, y=2):
    return x+y


toy_functions = list(get_functions(toy, [1, [2, 3], {'x': 4}, {'x': 6, 'y': 7}]))
bauble_functions = list(get_functions(bauble, [None, -2, [-3], [6, -1], {'y': 4}]))
for result in multi(toy_functions+bauble_functions):
    print(result)
```
> 输出
```text
(1, 1)
(2, 3)
(4, 1)
(6, 7)
3
0
-1
5
5
```


### pool_map和pool_starmap和multi_map的对比
> 测试环境: 12核mac笔记本电脑, 可能会有一些误差
> 需要先安装环境`pip install aitool --upgrade`

| 函数名 | 实现方案 | 优点 | 缺点 | 耗时（秒） |
| --- | --- | --- | --- |
| test_sequence() | 按序循环执行 | - | - | 987.171 |
| test_pool_map() | 封装pool.map | 稳定 | 参数不灵活 | 87.051 |
| test_pool_starmap() | 封装pool.starmap | 稳定 | 参数不灵活 | 87.047 |
| test_multi_map() | 封装pool.apply_async | 参数灵活 | 不稳定 | 83.348 |

```python
from random import random
from time import sleep
from aitool import pool_map, pool_starmap, multi_map, exe_time


SLEEP_TIME = [random() for _ in range(2000)]


def toy(x):
    sleep(x)
    return x


def do_something_in_parent_process(data):
    print(data)


@exe_time(print_time=True)
def test_sequence():
    data = [toy(time) for time in SLEEP_TIME]
    do_something_in_parent_process(data)


@exe_time(print_time=True)
def test_pool_map():
    data = [result for result in pool_map(toy, SLEEP_TIME)]
    do_something_in_parent_process(data)


@exe_time(print_time=True)
def test_pool_starmap():
    data = [result for result in pool_starmap(toy, [[_] for _ in SLEEP_TIME])]
    do_something_in_parent_process(data)


@exe_time(print_time=True)
def test_multi_map():
    data = [result for result in multi_map(toy, SLEEP_TIME)]
    do_something_in_parent_process(data)


print(sum(SLEEP_TIME))
test_pool_map()
test_pool_starmap()
test_multi_map()
test_sequence()

```