from __future__ import print_function
import httplib2
import os
from apiclient import discovery
import datetime
import pprint
from Auth.auth import *

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

#Steps to creating google calendar event:
#   Oauth: get credentials
#   create service object
#   Construct Event Data Structure
#   call: service.events().insert(calID, event)

#

class GCal():
    def __init__(self):
        self.service = self._createServiceOBJ()
        self.calID = {'RoomResCal':'oc8nbhvnlr59bbk393oc8qfir8@group.calendar.google.com'}
        self.eventResults = None
        self.created_event = None
        self.now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        self.eventID = {}

    def _createServiceOBJ(self):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        return service
    
    def writeEvent(self, event, calID=None):
        if calID==None:
            self.created_event = self.service.events().insert(calendarId=self.calID['RoomResCal'], body=event).execute()
            return self.created_event
        else:
            self.created_event = self.service.events().insert(calendarId=calID, body=event).execute()
            return self.created_event


    def _getEventResults(self, resultNum=15):
        self.eventResults = self.service.events().list(
                    calendarId=self.calID['RoomResCal'], timeMin=self.now, 
                    maxResults=resultNum, singleEvents=True,
                    orderBy='startTime').execute()
        return self.eventResults
    
    def _createEventIdDict(self):
        if self.eventResults ==None:
            self._getEventResults()
        
        events = self.eventResults.get('items', [])
        eventIdDict = {}
        count = 0
        for event in events:
            key = str(count) + event['summary']
            eventIdDict[key] =event['id']
        return eventIdDict

    def showEvents(self):
        EventStr = ""
        if self.eventResults ==None:
            self._getEventResults()
        
        events = self.eventResults.get('items', [])
        #print(events)
        for event in events:
            print(event['summary'], " id: ", event['id'])
            location = event['location']
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            EventStr = event['summary'] +"\n" + "from: " + start + "\nto: " +  end + "\nAt: " + location  +"\n"
            attendList = event['attendees']
            EventStr += "Attending: "
            for name in attendList:
                attending = name['displayName'] +" "
                EventStr+= attending
            EventStr +="\n\n"
        print(EventStr)
        return EventStr

    def _getEventId(self, Event):
        if 'id' in Event:
            return Event['id']
        else:
            print("ERROR getting EventID")
            return None
        
    def deleteEvent(self,eventID, calID=None):
        
        if calID == None:
            self.service.events().delete(calendarId=self.calID, eventId=eventID).execute()

        else:
            self.service.events().delete(calendarId=calID, eventId=eventID).execute()


def main():
   

    """
    service = createServiceOBJ()
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    """
    
    # TODO: write a wrapper class around this 
    # Event Data Structure	

    #------------- Event DATA STRUCTURE-----
    event = {
      'summary' : 'Python Calendar TEST',
      'location': 'UCR, Riverside, CA 92507',
      'start': {
        'dateTime': '2017-02-17T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2017-02-18T17:00:00-07:00',
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
     
    gcal = GCal()
    gcal.writeEvent(event)
    print("showing events")
    gcal.showEvents()

    """
    idDict ={}
    idDict = gcal._createEventIdDict()
    print("idDict:  ", idDict)

    while True:
        print("Delete Menu: \n")
        res = raw_input("would you like to delete events?(y/n)")
        count = 0
        if res == 'y':
            for k, v in idDict.items():
                print(k, v)

            choice = raw_input("choose what you want to delete")
            print("deleting event with id: ", idDict[choice])
            gcal.deleteEvent(idDict[choice])

            gcal.showEvents()

        if res == 'n':
            exit(0)
    """
    

    """
    #-------------End Event DATA STRUCTURE

    #could create a dictionary with the names of the calendars
    # you would like to work with and there calID

    calID='oc8nbhvnlr59bbk393oc8qfir8@group.calendar.google.com'

    created_event = service.events().insert(calendarId=calID, body=event).execute()

    #print(created_event.get('htmlLink'))
   
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId=calID, timeMin=now, maxResults=15, singleEvents=True,
        orderBy='startTime').execute()

    print("***** eventsResult ******")
    pp = pprint.PrettyPrinter()
    #pp.pprint( eventsResult )
    events = eventsResult.get('items', [])
    pp.pprint(events)

    if not events:
        print('No upcoming events found.')

    #This is the part of the code that will change depending of the information you 
    # want to pull from the calendar
    for event in events:
        location = event['location']
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        print("from: ", start," to: ", end," at: ", location, event['summary'])
        attendList = event['attendees']
        for name in attendList:
            attending = name['displayName']
            print("attending: ", attending)

    """

if __name__ == '__main__':
    main()
