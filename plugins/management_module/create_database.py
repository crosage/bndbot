import sqlite3
import os
file_directory=os.path.dirname(os.path.abspath(__file__))
parent_directory=os.path.dirname(file_directory)
print(f"{file_directory} {parent_directory}")
db_file=os.path.join(parent_directory,"qqbot.db")
if os.path.exists(db_file)==False:
    conn=sqlite3.connect(db_file)
    cursor=conn.cursor()
    night_table='''
        CREATE TABLE `MorningCheckIn` (
            `id` INTEGER  PRIMARY KEY AUTOINCREMENT,
            `groupnum` INTEGER  DEFAULT NULL,
            `qqnum` INTEGER  DEFAULT NULL,
            `time_stamp` INTEGER DEFAULT NULL
        );
    '''
    morning_table='''
        CREATE TABLE `EveningCheckIn`(
            `id` INTEGER  PRIMARY KEY AUTOINCREMENT,
            `groupnum` INTEGER  DEFAULT NULL,
            `qqnum` INTEGER  DEFAULT NULL,
            `time_stamp` INTEGER DEFAULT NULL
        )
    '''
    NSFW_permission='''
        CREATE TABLE `NSFWPermission`(
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `groupnum` INTEGER DEFAULT NULL
            
        )
    '''
    function_table='''
        CREATE TABLE `FunctionTable`(
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `function` VARCHAR(30) DEFAULT NULL
        )
    '''
    group_function_permission='''
        CREATE TABLE `GroupFunctionPermission`(
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `groupnum` INTEGER DEFAULT NULL,
            `function` INTEGER,
            FOREIGN KEY (`function`) REFERENCES `FunctionTable`(`id`)
        )
    '''

    cursor.execute(night_table)
    cursor.execute(morning_table)
    cursor.execute(NSFW_permission)
    cursor.execute(function_table)
    cursor.execute(group_function_permission)
    conn.commit()
    conn.close()
