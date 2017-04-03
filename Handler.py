#!/usr/bin/python
from __future__ import print_function
from Reserver import LoginPage
from selenium import webdriver
from optparse import OptionParser
import os
from Constants import TVROOMS, ROOMS 


def parsecmds():
	parser = OptionParser("Usage: -u <name> -d <date> -t <time> -r <roomNumber>")
	#parser.add_option("-i", dest="libid", help="Library ID number")
	parser.add_option("-u", dest="name", help="first name")
	parser.add_option("-d", dest="date", help="date of reservation eg. 1/22/17")
	parser.add_option("-t", dest="time", help="time you want the reservation eg. 1:00PM-3:00PM")
	parser.add_option("-r", dest="room", help="room number you want")


	(options, args) = parser.parse_args()

	if((options.name == None) | (options.date==None) |(options.time == None) | (options.room == None)):
		print(parser.usage)
		exit(0)
	else:
		name = options.name
		date = options.date
		time = options.time
		room = options.room
	return (name, date, time, room)	


def findRoom(roomList, usedRooms):
	allRooms = [str(i) for i in TVROOMS] + [str(i) for i in ROOMS]
	validRooms = set(roomList).intersection(allRooms)
	callableRooms = validRooms - set(usedRooms)
	print("callableRooms: ", callableRooms)
	callableRooms = list(callableRooms)
	return callableRooms[0]



def goGetIt(uname, passwd, date, time, phoneNum, usedRooms):
	driver = webdriver.Firefox()
	loginPage = LoginPage(driver)
	loginPage.go()
	loginPage.setCreds(uname, passwd)

	availTimePage = loginPage.submit()
	
	availTimePage.setHours(3)
	availTimePage.setTime('AnyTime')
	#dateList
	dateList = availTimePage.getDates()
	if date in dateList:
		availTimePage.setDate(date)
	else:
		print('Date', date, " is NOT available... exiting")
		availTimePage.close()
		exit(0)

	LocationsPage=availTimePage.next()
	LocationsPage.choose('Rivera')
	TimesPage=LocationsPage.next()
	timesList = TimesPage.getTimes()
	#Assuming the room and time is there
	# TODO: test case for unavaiable room
	if time in timesList:
		TimesPage.choose(time)
	else:
		print("time: ", time, " is NOT available... exiting")
		TimesPage.close()
		exit(0)

	RoomsPage = TimesPage.next()
	roomList = RoomsPage.getRooms()

	roomNum = findRoom(roomList, usedRooms)
	RoomsPage.choose(roomNum)
	RegisterPage = RoomsPage.next()
	RegisterPage.setPhoneNum(phoneNum)	
	RegisterPage.submit()
	return roomNum



if __name__ == '__main__':
	name, date, time, room = parsecmds()
	nameid = name.upper().strip()+"ID"
	print("name: ", nameid)
	id = os.environ.get(nameid)
	print("id: ",id)
	passwd = name.upper().strip()+"PASS"
	passwd = os.environ.get(passwd)

	phoneNum = name.upper().strip()+"PHONE"
	print("phoneNum var: ", phoneNum)
	phoneNum = os.environ.get(phoneNum)

	print('pass: ', passwd)
	print("date: ", date)
	print("time: ", time)
	print("phone: ", phoneNum)

	goGetIt(id, passwd, date, time, phoneNum, usedRooms)




