from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
import pprint

import sys

sys.path.append('../Auth/')

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# taking off the .readonly from SCOPES allows read and write priviledges
#SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
SCOPES = 'https://www.googleapis.com/auth/calendar'

#client_secret.json must be in working directory
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():

    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())



    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    # TODO: write a wrapper class around this 
    # Event Data Structure	

    #------------- Event DATA STRUCTURE-----
    event = {
      'summary' : 'this is a test',
      'location': 'UCR, Riverside, CA 92507',
      'start': {
        'dateTime': '2016-10-04T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2016-10-05T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
      ],
      'attendees': [
        {'email': 'cfalzone10@gmail.com'},
        {'email': 'tico82003@gmail.com'},
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    #-------------End Event DATA STRUCTURE


    calID='oc8nbhvnlr59bbk393oc8qfir8@group.calendar.google.com'
    created_event = service.events().insert(calendarId=calID, body=event).execute()
    print(created_event.get('htmlLink'))
    """
    #-------testing quick add---------
	#calID = 'primary'
    calID='oc8nbhvnlr59bbk393oc8qfir8@group.calendar.google.com'
    #calID = 's6bf1oosasdrukpib4pq0b9mek@group.calendar.google.com'
    created_event = service.events().quickAdd(
        calendarId=calID,
        text='Created this event programatically using PYTHON!!').execute()
    """
   
    print(created_event['id'])
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=15, singleEvents=True,
        orderBy='startTime').execute()

    print("***** eventsResult ******")
    pp = pprint.PrettyPrinter()
    #pp.pprint( eventsResult )
    events = eventsResult.get('items', [])
    print ("\n")
    print ("\n")
    print ("\n")
    #pp.pprint(events)

    if not events:
        print('No upcoming events found.')

    #This is the part of the code that will change depending of the information you 
    # want to pull from the calendar
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()
