import sqlite3

from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from flask import redirect, render_template, session
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



def connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn, conn.cursor()

def to_dict(result):
    new_dict = [dict(item) for item in result]
    return new_dict



def usd(number):
    new_number = "{:.2f}".format(float(number))
    return new_number


def get_last(start, period):
    today = datetime.now().strftime("%Y-%m-%d")
    today = datetime.strptime(today, "%Y-%m-%d")
    start = datetime.strptime(start, "%Y-%m-%d")
    if period == 'year':
        time = relativedelta(years=1)
    elif period == 'month':
        time = relativedelta(months=1)
    elif period == 'two weeks':
        time = relativedelta(weeks=2)
    elif period == 'week':
        time = relativedelta(weeks=1)
    elif period == 'day':
        time = relativedelta(days=1)
    while start + time <= today:
        start += time
    return start.strftime("%Y-%m-%d")

