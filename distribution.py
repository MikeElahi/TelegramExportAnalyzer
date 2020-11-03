""" Checks multiple distributions in chats 
List of Distributions:
    - Messages over Senders
    - Messages over Time (Rounded to Day)
    - Messages over Time of Day (Rounded to 10 minutes)
"""
import argparse
from core import Analyzer

# Generator functions - Generate scaffolding for output or processing
def generateTOD(step:int = 10):
    """ Generates an order dict with time of day as key and 0 as value 
    This is later used to calculate time distributions.

    Arguments:
        - step int (default: 10) determines the step for minute, increments by that amount everytime
    """
    step = 10 if step is None else step
    result = dict()
    for hour in range(0, 24):
        for minute in range(0, 60, step):
            current_time = '{:02d}:{:02d}'.format(hour, minute)
            result[current_time] = 0
    return result

# Setup ArgumentParser
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--tod', help='Set Time of the Day step (default: 10)', type=int, choices=[10, 30, 1])
parser.add_argument('-f', '--file', help='Source .json file from Telegram', required=True)

args = parser.parse_args()

# Validate options
if args.tod is not None and (args.tod > 30 or args.tod <= 0):
    raise ValueError('Time of Day step must be between 1 and 30, {} given.'.format(args.tod))

TOD = generateTOD(args.tod)

if __name__ == "__main__":
    with Analyzer(file_path=args.file) as obj:
        # Depending on whether the exported object is a singular chat or an account, this may be different.
        if 'about' in obj: # The object is an entire account
            chats = obj['chats']['list']
        else: # The object is a singular chat
            chats = [obj, ]
        
        for chat in chats:
            # Set measurement variables
            messages_over_senders = {}
            messages_over_time    = {}
            messages_over_tod_n  = generateTOD(args.tod)

            for message in chat['messages']:
                if message['type'] != 'message':
                    continue

                # Processing variables
                date, time = message['date'].split("T")

                if args.tod == 10:
                    time = '{}{}'.format(time[:-4], '0') # Rounds the single minute into zero
                elif args.tod == 30:
                    time = '{}{}'.format(time[:-5], '30' if int(time[-5]) > 3 else '00')
                else: # TOD == 1
                    time = time[:-3]
                
                # Sender distribution
                if message['from'] not in messages_over_senders:
                    messages_over_senders[message['from']] = 0
                messages_over_senders[message['from']] += 1

                # Date distribution
                if date not in messages_over_time:
                    messages_over_time[date] = 0
                messages_over_time[date] += 1

                # Messages over TOD (n)
                if time not in messages_over_tod_n:
                    messages_over_tod_n[time] = 0
                messages_over_tod_n[time] += 1
            
            # Sort by number of messages
            messages_over_senders = dict(sorted(messages_over_senders.items(), key=lambda x: x[1], reverse=True))
            
            files = {
                '{}-distribution-senders.csv'.format(chat['id']): messages_over_senders,
                '{}-distribution-time.csv'.format(chat['id']): messages_over_time,
                '{}-distribution-tod-{}.csv'.format(chat['id'], args.tod): messages_over_tod_n, 
            }
            
            for file, values in files.items():
                with open(file, 'w+') as file:
                    for label, value in values.items():
                        file.write('{},{}\n'.format(label, value))
        
