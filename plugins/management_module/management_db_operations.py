import sqlite3
from .create_database import db_file
from nonebot.log import logger
def delete_permission(group:int,name:str):
    """
    删除某个群聊中的某项功能

    name: int
    """
    result=is_function_exist(name)
    if result:
        name=result[0]
        with sqlite3.connect(db_file) as conn:
            cur=conn.cursor()
            sql = "DELETE FROM GroupFunctionPermission WHERE groupnum = ? AND function = ?"
            cur.execute(sql, (group, name))
            conn.commit()

def add_permission(group,name):
    """
    添加功能，先检测能否添加

    """
    result=is_function_exist(name)
    if result:
        name=result[0]
        with sqlite3.connect(db_file) as conn:
            cur=conn.cursor()
            sql=f"insert into GroupFunctionPermission(groupnum,function) values(?,?) "
            cur.execute(sql,(group,name))
            conn.commit()


def is_function_enabled(group_num:int, functions:str)->int:
    """
    群中是否包含某项功能
    """
    result=is_function_exist(functions)
    if result:
        functions=result[0]
        with sqlite3.connect(db_file) as conn:
            cur=conn.cursor()
            sql=f"select * from GroupFunctionPermission where groupnum=? and function=?"
            cur.execute(sql,(group_num,functions))
            result=cur.fetchone()
            return result

def add_function(name:str):
    """
    往功能表中添加功能
    """
    with sqlite3.connect(db_file) as conn:
        cur=conn.cursor()
        sql=f"insert into FunctionTable(function) values(?) "
        tmp=cur.execute(sql,(name,))
        conn.commit()
def get_all_functions():
    with sqlite3.connect(db_file) as conn:
        cur=conn.cursor()
        sql=f"select * from FunctionTable"
        cur.execute(sql)
        return cur.fetchall()

def is_function_exist(name:str):
    """
    是否存在某个功能，如果存在，返回id
    """
    with sqlite3.connect(db_file) as conn:
        cur=conn.cursor()
        sql=f"select * from FunctionTable where function=?"
        tmp=cur.execute(sql,(name,))
        result=cur.fetchone()
        logger.debug(f"is_function_exist:: {result}")

        return result

def get_functions_by_group_id(group:int):
    with sqlite3.connect(db_file) as conn:
        cur=conn.cursor()
        sql=f"select * from GroupFunctionPermission where groupnum=?"
        tmp=cur.execute(sql,(group,))
        return cur.fetchall()

