from datetime import datetime
import dateutil.parser


"""
AutoRoomRes class uses the following formats for time and date:

Date: yyyy/mm/dd
time: HH:MMAM-HH:MMPM

Google calendar uses UTC time for events:
Utc_time: yyyy-mm-ddTHH:MM:SS.mmm

The TimeConverter Class acts as an interface between the two
formats
"""
DEBUG = False

class TimeConverter():
    def __init__(self, date='', time=''):
        self.time=time
        self.date = date
        self.startDict = {}
        self.endDict = {}

    def parseTime(self, time):
        """ parses the time returns the START and END time in a list
            timeformat: ex: 8:00AM-9:00PM"""
        splt = time.split('-')
        t =[0,0]
        for i in range(len(splt)):
            res = datetime.strptime(splt[i],'%I:%M%p')
            res = res.strftime('%H:%M:%S')
            t[i]=res
        return t

    def parseDate(self, date):
        """ date inputformat: 1999/06/8
            date ouput format 1999-06-08\n"""

        return datetime.strptime(date, "%Y/%m/%d").strftime("%Y-%m-%d")

    def convertTime(self, time, format='utc'): 
        """Usage: convertTime(time, format='utc')\n"""
        if format == 'utc':
            t = time.split('T')
            if DEBUG:
                print self.parseDate(t[0])
            dateutil.parser.parse(t[1])
            dt = dateutil.parser.parse(t[1])
            return dt.strftime('%I:%M%p')
        else:
            if DEBUG:
                print "ERROR: format not supported yet"
            return

    def changeToUTC(self, date, time, startTime=True):
        date = self.parseDate(date)
        #GMT = '-07:00'
        PST = '-08:00'
        time = self.parseTime(time)    

        if startTime:
            time = time[0]
        else:
            time = time[1]
        return date + "T" + time + PST
        
    def createStartEndEvent(self, date=None, time=None):
        if date ==None:
            if self.date != None:
                date = self.date
            else:
                if DEBUG:
                    print "Need to either pass a date\
                            as constructors or as function parameters"
                else:
                    return
        else:
            date = date
        
        if time == None:
            if self.time != None:
                time = self.time
            else:
                if DEBUG:
                    print "Need to either pass a time\
                            as constructors or as function parameters"
                else:
                    return
        else:
            time = time
                    
        startData = self.changeToUTC(date, time, startTime=True)
        endData = self.changeToUTC(date, time, startTime=False)
        #ToDo: Note Add timezone functionality
        timezone = 'America/Los_Angeles'

        self.startDict['dateTime'] = startData
        self.startDict['timeZone'] = timezone

        self.endDict['dateTime'] = endData
        self.endDict['timeZone'] = timezone



def main():


    utc_time = '2016-10-01T04:00:00.000-05:00'
#print "match UTC FORMAT: ", utc_time
#print "Testing parseDate: "
    time='8:30PM-11:00PM'
    date = '2016/10/6'

    convert = TimeConverter(date, time)
    #convert.parseDate(date)

    #print convert.changeToUTC(date, time)
    #convert.createStartEndEvent(date, time)
    convert.createStartEndEvent()
    #Access the StartDict  and EndDict
    print("Start:")
    print convert.startDict
    print("End:")
    print convert.endDict

if __name__ == "__main__":
    main()




