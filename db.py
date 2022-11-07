import sqlite3 as sq
from categories import Categories_new


def insert(message, date):
    try:
        con = sq.connect('bot.db')
        cur = con.cursor()
        if len(message.split()) == 2:
            if isinstance(message.split()[1], str):
                mes = [int(message.split()[0]), message.split()[1], date]
                for category in Categories_new:
                    if mes[1].lower() in category[2]:
                        mes[1] = category[1]
                        break

                if (mes[1] == message.split()[1]) and (mes[1] not in [c[1] for c in Categories_new]):
                    mes[1] = 'Прочее'

                cur.execute("INSERT INTO expenses VALUES(NULL, ?, ?, ?)", mes)
                con.commit()
                mess = "Данные успешно внесены"
                return mess
        else:
            raise ValueError
    except sq.Error as e:
        if con:
            con.rollback()
        raise ValueError
    finally:
        if con:
            con.close()


def delete():
    try:
        con = sq.connect('bot.db')
        con.row_factory = sq.Row
        cur = con.cursor()
        cur.execute("""DELETE FROM expenses 
                    WHERE date_exp=(SELECT date_exp FROM expenses ORDER BY date_exp DESC LIMIT 1)""")

        con.commit()
        mes = 'Последние внесенные данные удалены'
        return mes
    except sq.Error:
        if con:
            con.rollback()

    finally:
        if con:
            con.close()


def fetch(query:str):
    try:
        con = sq.connect('bot.db')
        con.row_factory = sq.Row
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        return [{x['category']: x['exp']} for x in cur]
    except sq.Error:
        if con:
            con.rollback()

    finally:
        if con:
            con.close()