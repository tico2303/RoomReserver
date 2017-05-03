from __future__ import print_function
from datetime import datetime
from datetime import timedelta
import pickle

class User:
        def __init__(self):
                self.roomsNtimes = {}
        
        def save(self):
                pickle.dump(self.roomsNtimes, open('roomsNtimes.pkl','wb'))

        def loadData(self):
                try:
                        return pickle.load(open('roomsNtimes.pkl','rb'))
                except:
                        return {}

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
        #check if there is an existing pickeled file
        u.roomsNtimes = u.loadData() 
        """
        How a date and room are added to user class
        u.addRoom("2017/05/01",213)
        u.addRoom("2017/05/02",214)
        u.addRoom("2017/05/03",215)
        u.addRoom("2017/04/11",216)
        u.addRoom("2017/04/12",217)
        u.addRoom("2017/04/13",218)
        """
        # How to save the roomsNtimes dict to pickle file
        # u.save()

        print("roomsNtimes: ", u.roomsNtimes)
        
        # method that updates roomsNtimes dict and removes
        # rooms that are ealier than todays date
        u.updateUsedRooms()
        print("roomsNtimes: ", u.roomsNtimes)
        
        #Extracting usedRoomsList
        print("usedRooms: ",u.getUsedRooms() )




