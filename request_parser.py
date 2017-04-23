import re

# определяем формат времени
from datetime import datetime


# TimeFormatDashRegex = re.compile("[\d]+-[\d]+")
# TimeFormatColonRegex = re.compile("[\d]+:[\d]+")


def setRequest(request):
    data = {}
    request_text = ""
    request = str(request).split(" ")
    for i in range(len(request)):
        if request[i].__contains__("/Напомнить"):
            request[i] = ""
        if re.match("[\d]+-[\d]+", request[i]):
            date_object = datetime.strptime(request[i], "%H-%M")
            request[i] = ""
        if re.match("[\d]+:[\d]+", request[i]):
            date_object = datetime.strptime(request[i], "%H:%M")
            request[i] = ""
        request_text += request[i] + " "
    data['Text'] = request_text
    data['Date'] = date_object
    return data

