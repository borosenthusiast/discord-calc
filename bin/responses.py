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
    except:
        return False

def get_response(message:str, dicsMsg, username, channel, server_name):
    p_message = message.lower()

    p_message = p_message.split(' ')

    # Validations
    if (len(p_message) != 4 and p_message[0] == deets.DICT_COMMANDS[0]):
        return deets.INCORRECT_LENGTH
    elif (not test_conversion(p_message)):
        return deets.INCORRECT_PARAM
    
    #Data Processing & DB query
    dateInt = p_message[1]
    amount = int(p_message[2])
    date = datetime.strptime(dateInt, '%Y%m%d').strftime('%m/%d/%Y')
    #TODO: DB INSERT
    try:
        database.dbInsert(server_name, username, channel, amount, date)
    except Exception as e:
        print(e)
    #TODO: REMOVE TEMP TEST OUTPUT (or make concise as a confirmation output)
    return f'The amount made on {date} was {amount} gil. This figure was reported by {username} on the channel {channel} on the server {server_name}.'
    
  