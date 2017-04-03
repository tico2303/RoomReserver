
#-------------- Event Dtat Structure ---------
EVENT = {
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

from utils.timeconverter import TimeConverter

class EventWrapper():
    def __init__(self, event=None):
        if event==None:
            self.event = {} 
            self._createEvent()
        else:
            self.event = event
        self.timeConverter = TimeConverter()
        self.setLocation()

    def _createEvent(self):
        self.event={'summary':'',
                    'location':'',
                    'recurrence':['RRULE:FREQ=DAILY;COUNT=2'],
                    'attendees':[],
                    'reminders':{'useDefaults':False,
                                },
                    }
    
    def setSummary(self, summary):
        self.event['summary'] = str(summary)
        return self.event
    
    def setLocation(self,addr='UCR', city='Riverside', state='CA', zipcode='92507' ):
        """Usage: setLocation(addr='UCR', city='Riverside', state='CA', zipcode='92507' )\n
        The defaults are set to UCR library specs.\n"""
        location = str(addr)+ " " + str(city)+ "," + str(state)+" "+ str(zipcode)
        self.event['location'] = location
        return self.event
    
    def setAttendees(self, peopleList):
        """ takes in a list of the emails of the people who will attend the event"""
        for email in peopleList:
           attendeeDict = {}
           attendeeDict["email"] = email
           self.event['attendees'].append(attendeeDict)

    # UTC long format setter
    def __setStartTime(self, time):
        timeDict={}
        timeDict['dateTime'] = time
        timeDict['timeZone'] = 'America/Los_Angeles'
        self.event['start'] = timeDict
        return self.event

    # UTC long format setter
    def __setEndTime(self, time):
        timeDict={}
        timeDict['dateTime'] = time
        timeDict['timeZone'] = 'America/Los_Angeles'
        self.event['end'] = timeDict
        return self.event 

    # takes in date format (2017/12/31) and time format (8:00AM-11:00PM)
    def setDateTime(self, date, time):
        timeDict={}
        self.timeConverter.createStartEndEvent(date,time)
        self.event['start'] = self.timeConverter.startDict
        self.event['end'] = self.timeConverter.endDict
        return self.event

def main():
    import pprint
    pp = pprint.PrettyPrinter()
    ew = EventWrapper()
    pp.pprint(EVENT)
    print "*"*40
    ew.setSummary("This is a test Calendar entry")
    print "\n"
    print "\n"
    ew.setLocation()
    print "\n"
    print "\n"
    """
    print("Setting time to: ", "2017-02-18T004:00:00-7:00")
    ew.__setStartTime("2017-02-18T004:00:00-7:00")
    """
    date = '2017/02/22'
    time = '8:00AM-11:00AM'
    attendingList = ["tico82003@gmail.com", "cfalzone10@gmail.com"]
    ew.setAttendees(attendingList)
    pp.pprint(ew.setDateTime(date, time) )
    print "\n"
    print "\n"
    #pp.pprint(ew.__setEndTime("2017-02-19T004:00:00-7:00"))
    
    

if __name__ == "__main__":
    main()

