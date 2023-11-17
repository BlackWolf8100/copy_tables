from my_base import My_base
from my_loger import My_loger


LOG_FILE = 'c:\\API\Mykola\copy_tables\copy_tables.log'


def format_time(time_duration):
    hours, remainder = divmod(time_duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours}:{minutes}:{seconds}'


def main(loger):
    
    db_out = My_base(logger = loger)
    db_inp = My_base(logger = loger, dbfile = 'mytest_out.db')
    

    if not db_inp.open():
        print('Помилка роботи з базою даних!')
        loger.log('Помилка роботи з базою даних!')
        return
    
    if not db_out.open():
        print('Помилка роботи з базою даних!')
        loger.log('Помилка роботи з базою даних!')
        return 
    
    
    tables = ('parse', 'parse_a', 'parse_h', 'parse_img')
    for table in tables:
        sql = f'DELETE FROM {table}'
        db_out.cursor.execute(sql)
    db_out.mydb.commit()
    
    for table in tables:
        print(table)
        loger.log(f'Обробляємо таблицю: {table}')
        sql = f'SELECT * FROM {table}'
        db_inp.cursor.execute(sql)
        count = len(db_inp.cursor.description)
        result = (e for e in db_inp.cursor.fetchall())
        s_string = '%s, '*count
        sql = f'INSERT INTO {table} VALUES({s_string[:-2]})'
        db_out.executemany(sql, result)
        db_out.mydb.commit()
        
        
    db_inp.close()
    db_out.close()


        
if __name__ == '__main__':
    loger = My_loger(LOG_FILE)
    loger.log(f'copy_tables starting')
    main(loger)
    loger.log(f'copy_tables end')