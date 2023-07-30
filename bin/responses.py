import deets
from datetime import datetime
import database
from return_type import return_type
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

def test_conversion(p_message:list):
    try:
        if p_message[0] not in deets.DICT_COMMANDS:
            return False
        elif (not str.isdigit(p_message[1]) or not str.isdigit(p_message[2])):
            return False 
    
        return True
    except Exception as e:
        print(e)
        return False

def process_calc(p_message, dicsMsg, username, channel, server_name):
    #Data Processing & DB query
    dateInt = p_message[1]
    try:
        amount = int(p_message[2])
    except ValueError:
        return "Please enter a whole number greater than 0 as the input for the amount earned."
    try:
        date = datetime.strptime(dateInt, '%Y%m%d')
    except ValueError:
        return "Invalid date format - enter the date as YYYYMMDD\nExample: 20140506."
    if (len(p_message) == 4): #has comment
        comment = str(p_message[3])
    else:
        comment = ""

    if (amount < 0):
        return return_type("Please enter a whole number greater than 0 as the input for the amount earned.", return_type.TEXT)

    try:
        database.dbInsert(server_name, username, channel, amount, date, comment)
    except Exception as e:
        print(e)
    if (comment == ""):
        return return_type(f'The amount made on {date.date()} was {amount} gil. This figure was reported by {username} on the channel {channel} on the server {server_name}.', return_type.TEXT)
    else:
        return return_type(f'The amount made on {date.date()} was {amount} gil. This figure was reported by {username} on the channel {channel} on the server {server_name}. \
             \nA comment has been made on the record, {comment}', return_type.TEXT)
    
def process_help():
    return return_type("There are currently four commands available for use! Examples for formatting are as follows. \n\"!calc YYYYMMDD AMOUNT\" adds an entry\
          to YEAR MONTH DAY for the amount of AMOUNT gil earned.\n \"!help will give you this prompt again.\"\n\
            \"!calctotal will give you the total amount of reported earnings to date.\"\n\
            \"!calcmetrics will give some cursory information on earnings, more features to come.\"\n", return_type.TEXT)

def process_total(server_name, channel):
    try:
        result = database.dbTotal(server_name, channel)
    except Exception as e:
        print(e)
    return return_type(result, return_type.TEXT)

def process_total_month(server_name, channel):
    try:
        result = database.dbTotalByDay(server_name, channel)
    except Exception as e:
        print(e)
    return return_type(result, return_type.TEXT)

def process_metrics(server_name, channel):
    try:
        result = database.dbMetrics(server_name, channel)
    except Exception as e:
        print(e)
    return return_type(result, return_type.TEXT)

def process_best_day_of_week(server_name, channel):
    try:
        result = database.dbBestDaysOfWeek(server_name, channel)
        # Create the Seaborn bar chart
        plt.figure(figsize=(10, 6))
        sns.barplot(x="Weekday", y="Average Earnings", data=result.data)
        plt.title("Average Earnings on Each Weekday")
        plt.xlabel("Weekday")
        plt.ylabel("Average Earnings")
        plt.xticks(rotation=45)
        plt.tight_layout()
        # Save the chart as a figure and return it
        chart_figure = plt.gcf()  # Get the current figure
        buf = io.BytesIO()
        chart_figure.savefig(buf, format="png", dpi=300, bbox_inches="tight")
        buf.seek(0)
        # Convert the PNG file in memory to bytes
        png_bytes = buf.getvalue()
        plt.close()
        result.data = png_bytes
    except Exception as e:
        print(e)
    return return_type(result.ret, return_type.IMG, data=result.data)

def process_best_day(server_name, channel):
    try:
        result = database.dbHighestDay(server_name, channel)
    except Exception as e:
        print(e)
    return return_type(result, return_type.TEXT)

def process_worst_day(server_name, channel):
    try:
        result = database.dbLowestDay(server_name, channel)
    except Exception as e:
        print(e)
    return return_type(result, return_type.TEXT)

def process_export(server_name, channel):
    try:
        result = database.dbExport(server_name, channel)
    except Exception as e:
        print(e)
    return return_type(result, return_type.TEXT)   

def get_response(message:str, dicsMsg, username, channel, server_name):
    p_message = message.lower()
    p_message = p_message.split(' ')
    # Validations
    if (len(p_message) < 3 and p_message[0] == deets.DICT_COMMANDS[0]):
        return return_type(deets.INCORRECT_LENGTH, return_type.TEXT)
    
    if (p_message[0] == deets.DICT_COMMANDS[0]):
        return process_calc(p_message, dicsMsg, username, channel, server_name)
    elif(p_message[0] == deets.DICT_COMMANDS[1]):
        return process_help()
    elif(p_message[0] == deets.DICT_COMMANDS[2]):
        if (len(p_message) == 1):
            return process_total(server_name, channel)
        elif (p_message[1].lower() == deets.SUBCOMMAND_DAY):
            return process_total_month(server_name, channel)
    elif(p_message[0] == deets.DICT_COMMANDS[3]):
        if(len(p_message) == 2): 
            if (p_message[1] == deets.SUBCOMMAND_BESTDAYOFWEEK):
                return process_best_day_of_week(server_name, channel)
            elif(p_message[1] == deets.SUBCOMMAND_BEST_DAY):
                return process_best_day(server_name, channel)
            elif(p_message[1] == deets.SUBCOMMAND_WORST_DAY):
                return process_worst_day(server_name, channel)
            else:
                return return_type(deets.METRICS_HELP, return_type.TEXT)
        else:
            return return_type(deets.METRICS_HELP, return_type.TEXT)
    elif(p_message[0] == deets.DICT_COMMANDS[4]):
        return process_export(server_name, channel)

