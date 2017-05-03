from __future__ import print_function
# needs to save date and usedrooms per-user
# needs to update usedRooms based on the current day

from datetime import datetime
from datetime import timedelta
import pickle

"""
print("datatime().now().strftime()", datetime.now().strftime("%Y/%m/%d"))

curr_date = datetime.now().strftime("%Y/%m/%d")

######convert input string into datetime object
mydate = "2017/05/02"
my_date = datetime.strptime(mydate,"%Y/%m/%d");
print("my_date: ", my_date)
####################################

########## check for old times: 
if my_date < datetime.now():
        print("This date", my_date," is before: ", datetime.today())
else:
        print("no less than")
######################
"""
class User:
        def __init__(self):
                self.roomsNtimes = {}
        
        def save(self):
                pickle.dump(self.roomsNtimes, open('roomsNtimes.pkl','wb'))

        def loadData(self):
                return pickle.load(open('roomsNtimes.pkl','rb'))

        def __convertTime(self, time):
                return datetime.strptime(time, "%Y/%m/%d")
        
        def getUsedRooms(self):
                self.roomsNtimes = self.updateUsedRooms()
                return [x for x in self.roomsNtimes.values()]
                
        def addRoom(self,date,room):
                self.roomsNtimes[date] = room
        
        def updateUsedRooms(self):
                dates = self.roomsNtimes.keys()
                for date in dates:
                        d = self.__convertTime(date)
                        if d < datetime.now():
                                del self.roomsNtimes[date]
                return  self.roomsNtimes
                
if __name__ == '__main__':
        
        u = User()
        u.roomsNtimes = u.loadData() 
        """
        u.addRoom("2017/05/01",213)
        u.addRoom("2017/05/02",214)
        u.addRoom("2017/05/03",215)
        u.addRoom("2017/04/11",216)
        u.addRoom("2017/04/12",217)
        u.addRoom("2017/04/13",218)
        """
        #u.save()

        print("roomsNtimes: ", u.roomsNtimes)
        u.updateUsedRooms()
        print("roomsNtimes: ", u.roomsNtimes)
        print("usedRooms: ",u.getUsedRooms() )




