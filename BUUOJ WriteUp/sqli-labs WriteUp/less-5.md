题目：sqli-labs less5

在url后加入`?id=1`，访问后，输出如下
```
Welcome    Dhakkan
You are in...........
```
可以看出不同于`less1-4`，现在的输出只有一句`You are in...........`，在url后加入`?id=1' and 1=2 --+`，访问后，输出如下
```
Welcome    Dhakkan
```
在url后加入`?id=1' and 1=1 --+`，访问后，输出如下
```
Welcome    Dhakkan
You are in...........
```
因此，这里存在布尔盲注的空间，接下来编写python脚本如下进行布尔盲注
代码见文件[less-5.py](./code/less-5.py)
通过执行代码可以获取到
总共有6个数据库，分别是`ctftraining`, `information_schema`, `mysql`, `performance_schema`, `security`, `test`(这里面_在代码中求出来的值为`{`而不是`_`，这猜测可能与我使用的字典集以及mysql的字符比较有关，等待未来解决。)
当前使用的数据库名称为`security`
其下有四个表,分别为`emails` ，`referers` ，`uagents` ，`users`
其中`users`表有三个字段分别为`id`，`username`，`password`
获取`users`表中的数据可获得如下所示内容
- ` dumb ` ， ` dumb `
- ` angelina ` ， ` i-kill-you `
- ` dummy ` ， ` p@ssword `
- ` secure ` ， ` crappy `
- ` stupid ` ， ` stupidity `
- ` superman ` ， ` genious `
- ` batman ` ， ` mob'le `
- ` admin ` ， ` admin `

其中左侧为用户名，右侧为密码。
在数据库`ctftraining`中，有3个表分别为`flag`，`news`，`users`
在`flag`表中有`flag`字段，其中的数据查询后即可获得`flag`
`flag`:`flag{8bd44270-8f98-476a-a51e-31a6b28de300}`

经过实际体验，感觉布尔盲注手写还是太麻烦了，要重复很多遍的数量，长度，名称的判断循环来找到答案。还是用现成的工具进行攻击比较好。