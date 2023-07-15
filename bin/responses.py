import deets
from datetime import datetime
import database

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
        return "Please enter a whole number greater than 0 as the input for the amount earned."

    try:
        database.dbInsert(server_name, username, channel, amount, date, comment)
    except Exception as e:
        print(e)
    if (comment == ""):
        return f'The amount made on {date.date()} was {amount} gil. This figure was reported by {username} on the channel {channel} on the server {server_name}.'
    else:
        return f'The amount made on {date.date()} was {amount} gil. This figure was reported by {username} on the channel {channel} on the server {server_name}. \
             \nA comment has been made on the record, {comment}'
    
def process_help():
    return "There are currently four commands available for use! Examples for formatting are as follows. \n\"!calc YYYYMMDD AMOUNT\" adds an entry\
          to 2010 DECEMBER 25 for the amount of 6969 gil earned.\n \"!help will give you this prompt again.\"\n\
            \"!calctotal will give you the total amount of reported earnings to date.\"\n\
            \"!calcmetrics will give some cursory information on earnings, more features to come.\"\n"

def process_total(server_name, channel):
    try:
        result = database.dbTotal(server_name, channel)
    except Exception as e:
        print(e)
    return result

def process_total_month(server_name, channel):
    try:
        result = database.dbTotalByDay(server_name, channel)
    except Exception as e:
        print(e)
    return result

def process_metrics(server_name, channel):
    try:
        result = database.dbMetrics(server_name, channel)
    except Exception as e:
        print(e)
    return result

def process_best_day_of_week(server_name, channel):
    try:
        result = database.dbBestDaysOfWeek(server_name, channel)
    except Exception as e:
        print(e)
    return result

def process_best_day(server_name, channel):
    try:
        result = database.dbHighestDay(server_name, channel)
    except Exception as e:
        print(e)
    return result

def process_worst_day(server_name, channel):
    try:
        result = database.dbLowestDay(server_name, channel)
    except Exception as e:
        print(e)
    return result

def process_export(server_name, channel):
    try:
        result = database.dbExport(server_name, channel)
    except Exception as e:
        print(e)
    return result    

def get_response(message:str, dicsMsg, username, channel, server_name):
    p_message = message.lower()
    p_message = p_message.split(' ')
    # Validations
    if (len(p_message) < 3 and p_message[0] == deets.DICT_COMMANDS[0]):
        return deets.INCORRECT_LENGTH
    
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
                return deets.METRICS_HELP
        else:
            return deets.METRICS_HELP
    elif(p_message[0] == deets.DICT_COMMANDS[4]):
        return process_export(server_name, channel)

