import datetime
import sqlite3 as sq
from db import fetch

current_date = datetime.date.today()

MONTH_EXP_QUERY = """SELECT sum(summa) as exp, category from expenses WHERE strftime('%m',date_exp)= strftime('%m')              
                    GROUP by category
                    ORDER BY exp DESC"""

LAST_EXP_QUERY = """SELECT summa as exp, category from expenses                 
                    ORDER BY date_exp DESC
                    LIMIT 1"""

TODAY_EXP_QUERY = f"""SELECT sum(summa) as exp, category from expenses WHERE date(date_exp)='{str(current_date)}'                 
                    GROUP by category
                    ORDER BY exp DESC"""


TODAY_SUMM_QUERY = f"SELECT sum(summa) as exp from expenses WHERE date(date_exp)='{str(current_date)}'"


MONTH_SUMM_QUERY = "SELECT sum(summa) as exp from expenses WHERE strftime('%m',date_exp)= strftime('%m')"


def fetch_month_exp():
    return fetch(MONTH_EXP_QUERY)


def fetch_last_exp():
    return fetch(LAST_EXP_QUERY)


def fetch_today_exp():
    return fetch(TODAY_EXP_QUERY)


def fetch_today_summ():
    try:
        con = sq.connect('bot.db')
        cur = con.cursor()
        cur.execute(f"SELECT sum(summa) as exp from expenses WHERE date(date_exp)='{str(current_date)}'")
        con.commit()
        row = cur.fetchall()
        return row
    except sq.Error:
        if con:
            con.rollback()

    finally:
        if con:
            con.close()


def fetch_month_summ():
    try:
        con = sq.connect('bot.db')
        cur = con.cursor()
        cur.execute("SELECT sum(summa) as exp from expenses WHERE strftime('%m',date_exp)= strftime('%m')")
        con.commit()
        row = cur.fetchall()
        return row
    except sq.Error:
        if con:
            con.rollback()

    finally:
        if con:
            con.close()

