#Date
from datetime import datetime,time,date,timedelta
from dateutil.relativedelta import relativedelta

def getDateNow():
    return datetime.now()

def getSubstactedDate(currentDate,subYears,subMonths):
    return currentDate - relativedelta(years=subYears,months=subMonths)

def parseDateIntoRegularStr(date):
    return date.strftime('%Y-%m-%d')