from nonebot import require

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler
import pymysql

# @scheduler.scheduled_job("cron", second="*/2", id="xxx", args=[1], kwargs={"arg2": 2})
async def run_every_2_hour(arg1, arg2):
    with pymysql.connect(host="localhost",user="root",password="allforqqbot",database="qqbot",port=3306,charset="UTF8") as conn:
        cur=conn.cursor()