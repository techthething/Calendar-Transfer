from __future__ import print_function

from datetime import datetime, timedelta
import os.path
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']



def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # Run local server with dynamically allocated port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', 0))
                _, port_number = s.getsockname()
                flow.run_local_server(port=port_number)
            creds = flow.credentials
        # Save the credentials for the next run

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

        print("Dynamically assigned port number:", port_number)

    try:
        service = build('calendar', 'v3', credentials=creds)

        year = 2023 #note: run program in parts by year
        utc_to_cst = '05:00' #-05:00 w/ daylight savings time and -6:00 w/o
        day = 0 
        earliest_time = 5 #if event does not have time, set default starting time to 5 and iterate by 1 hour every time
        name = "John" #owner of calendar
        
        with open("doc_cal.txt") as f: #creates list containing every line
            lines = f.readlines() 


        def convert_time(time_str): #accepts time of format 6:32 PM and 6 AM and returns formatted time (18:32 and 06:00 respectively)
            if ":" in time_str:
                time_format = '%I:%M %p'
            else:
                time_format = '%I %p'
            print(time_str)
            time_obj = datetime.strptime(time_str, time_format)
            formatted_time = datetime.strftime(time_obj, '%H:%M')
            return formatted_time
            
        def preserve_arrow(string): #takes weird arrows and preserves form in actual calendar
            arrow_symbol = "â†’"
            if arrow_symbol in string:
                string = string.replace(arrow_symbol, "\u2192")
            return string
        
        def is_am(string): #accepts a.m. w/ or w/o periods and upper or lower. also accepts additional character at end (ex: a.m.;)
            pattern = r'^a\.?m\.?[^a-zA-Z0-9]*$|^am[^a-zA-Z0-9]*$'
            return bool(re.match(pattern, string.lower()))

        def is_pm(string): #same as is_am, but works for pm
            pattern = r'^p\.?m\.?[^a-zA-Z0-9]*$|^am[^a-zA-Z0-9]*$'
            return bool(re.match(pattern, string.lower()))
        
        for event_line in lines[0:50]:
            if event_line == '\n': #blank line
                day = 0 #blank line means that next line is a date of form - Day of Week, Month Day 
                continue
            else:
                event_info = event_line.split()
                if day == 0: #line with date
                    month = str(datetime.strptime(event_info[1], "%B").month) #converts month name to month number (ex: "March" -> "3")
                    day = re.search(r'\d+', event_info[2]).group() #gets number from day
                else: #line with event info
                    am_or_pm = None #is this in the am or pm?
                    has_no_time = True #if no time given at all
                    no_end = False #if only one time given
                    n = len(event_info)
                    once_am_or_pm = True #avoids repeats of am and pm (only takes last)
                    for x in range(n-1, -1, -1):
                        if once_am_or_pm and (is_am(event_info[x]) or is_pm(event_info[x])): #if end time 
                            event_info[x] = re.sub(r'[^\w\s]', '', event_info[x].upper()) #standardize input
                            am_or_pm, hour_end = event_info[x], event_info[x-1]
                            pos_time = x-1 #to make sure that next number input is not equal to the first
                            time_str = hour_end + " " + am_or_pm
                            formatted_time_end = convert_time(time_str)
                            no_end = True
                            has_no_time = False
                            once_am_or_pm = False
                        elif am_or_pm != None and bool(re.search(r'\d', event_info[x])) and x < pos_time and x > pos_time - 3:
                            hour_start = event_info[x]
                            if hour_start > hour_end or "12" in hour_end: #if start time is greater than end time (or if end time is 12:xx PM), first time must be in the AM
                                am_or_pm = "AM"
                            time_str = hour_start + " " + am_or_pm                           
                            formatted_time_start = convert_time(time_str)
                            no_end = False
                            break #once you have start and end time, exit for-loop
                    
                    if has_no_time: #no time given
                        time_str = str(earliest_time) + " AM"
                        formatted_time_start = convert_time(time_str)                           
                        time_str = str(earliest_time+1) + " AM"
                        formatted_time_end = convert_time(time_str)
                        earliest_time += 1
                    elif no_end: #no end time given
                        formatted_time_start = formatted_time_end #since no end time, must be the start time
                        if ":" in time_str:
                            time_format = '%I:%M %p'
                        else:
                            time_format = '%I %p'
                        start_time = datetime.strptime(time_str, time_format)
                        end_time = start_time + timedelta(hours=1) #adds one hour to starting time
                        formatted_time_end = datetime.strftime(end_time, '%H:%M')
                    event_line = preserve_arrow(event_line)
                    
                    event = { #set event
                        'summary': event_line, 
                        'start': {
                            'dateTime': f"{year}-{month.zfill(2)}-{day.zfill(2)}T{formatted_time_start}:00-{utc_to_cst}",
                            'timeZone': "America/Chicago",
                        },
                        'end': {
                            'dateTime': f"{year}-{month.zfill(2)}-{day.zfill(2)}T{formatted_time_end}:00-{utc_to_cst}",
                            'timeZone': "America/Chicago",
                        },
                    }
                    print(f"The following event ({event_line}) has been added to {name}'s Calendar") #prints out what event was just added
                    print(event['start']['dateTime']) #prints full start time
                    print(event['end']['dateTime']) #prints full end time

                    event = service.events().insert(calendarId='primary', body=event).execute()



    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()