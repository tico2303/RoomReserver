from Handler import *
from time import sleep
from Gcalendar import eventinterface
from Gcalendar import cal


MON = ['12:00PM-3:00PM', '7:00PM-10:00PM']
MONF = ['4:00PM-7:00PM', '7:00PM-10:00PM']
TUE = ['4:00PM-7:00PM', '7:00PM-10:00PM']
WED = ['4:00PM-7:00PM', '7:00PM-10:00PM']
WEDF = ['11:00AM-2:00PM', '2:00PM-5:00PM']
THR = ['4:00PM-7:00PM', '7:00PM-10:00PM']
FRI = ['11:00AM-2:00PM', '3:00PM-6:00PM']
SAT = ['11:00AM-2:00PM', '2:00PM-5:00PM']
SUN = ['1:00PM-4:00PM', '4:00PM-7:00PM']

sched = [
         #{'2017/03/09': [THR[0], THR[1]]},
         #{'2017/03/10': [FRI[0], FRI[1]]},
         #{'2017/03/11': [SAT[0], SAT[1]]},
         #{'2017/03/12': [SUN[0], SUN[1]]},
         #{'2017/03/13': [MON[0], MON[1]]},
         #{'2017/03/14': [TUE[0], TUE[1]]},
         #{'2017/03/15': [WED[0], WED[1]]},
         #{'2017/03/16': [THR[0], THR[1]]},
         #{'2017/03/17': [FRI[0], FRI[1]]},
         #{'2017/03/18': [SAT[0], SAT[1]]},
         #{'2017/03/19': [SUN[0], SUN[1]]},
         {'2017/03/20': [MONF[0], MONF[1]]},
         #{'2017/03/21': [TUE[0], TUE[1]]},
         {'2017/03/22': [WEDF[0], WEDF[1]]},
         #{'2017/03/23': [THR[0], THR[1]]},
         {'2017/03/24': [FRI[0], FRI[1]]},
         {'2017/03/25': [SAT[0], SAT[1]]},
         {'2017/03/26': [SUN[0], SUN[1]]},
		 ]

def writeToGcal(RoomNum, date, time):
	summary = 'You have Room '+str(RoomNum) + ' reserved     '\
	           'from: '+ str(time)+ ' on '+ str(date)
	attending = ["tico82003@gmail.com", "cfalzone10@gmail.com"]

	eventcreator = eventinterface.EventWrapper()
	eventcreator.setSummary(summary)
	eventcreator.setAttendees(attending)
	event = eventcreator.setDateTime(date, time)
	print event
	gcal = cal.GCal()
	gcal.writeEvent(event)
	print("Showing Google Calendar Events: ")
	gcal.showEvents()
    
def getRoomsList(filename):
    pass

def getInfo(name):
	nameid = name.upper().strip()+"ID"
	print("name: ", nameid)
	id = os.environ.get(nameid)
	passwd = name.upper().strip()+"PASS"
	passwd = os.environ.get(passwd)

	phoneNum = name.upper().strip()+"PHONE"
	phoneNum = os.environ.get(phoneNum)
	return [id, passwd, phoneNum]

infoList = getInfo("Cody")
infoList2 = getInfo("Robert")
usedRooms = ['308', '216']
usedRooms2 = ['308']

for d in sched:
	i = 0
	date = d.keys()
	print date
	print d
	print d.keys()
	print d[date[0]]

	if(i == 0):
		print("date", date)
		print("time1", d[date[0]][0])
		print("time2", d[date[0]][1])

	curRoom = goGetIt(infoList[0], infoList[1], date[0], d[date[0]][0], infoList[2], usedRooms)
	#writeToGcal(curRoom, date[0], d[date[0]][0])
	usedRooms.append(curRoom)
	sleep(2)
	curRoom2 = goGetIt(infoList2[0], infoList2[1], date[0], d[date[0]][1], infoList2[2],usedRooms2)
	#writeToGcal(curRoom, date[0], d[date[0]][1])
	usedRooms2.append(curRoom2)
	sleep(2)
	i+=1





