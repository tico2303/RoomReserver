#!/usr/bin/python
from __future__ import print_function
from Reserver import LoginPage
from selenium import webdriver


def TestLoginPage():
	driver = webdriver.Firefox()
	loginPage = LoginPage(driver)
	loginPage.go()
	loginPage.setCreds('21210022829659', 'martinez')
	return loginPage.submit()

def TestAvailableTimesPage():
	availTimePage = TestLoginPage()
	availTimePage.setHours(3)
	availTimePage.setTime('AnyTime')

	#/// Need to implement
	dateList = availTimePage.getDates()
	print(dateList)
	date = '2017/02/06'
	availTimePage.setDate(date)
	print("Setting Date: %s"%(date))
	return availTimePage.next()


def TestLocationsPage():
	LocationsPage = TestAvailableTimesPage()
	LocationsPage.choose('Rivera')
	return LocationsPage.next()

def TestTimesPage():	
	TimesPage = TestLocationsPage()		
	timesList = TimesPage.getTimes()
	#Assuming the room and time is there
	# TODO: test case for unavaiable room
	TimesPage.choose('3:00PM-6:00PM')
	print(timesList)
	print("Choosing Time:", timesList[0])
	return TimesPage.next()

def TestRoomsPage():	
	RoomsPage = TestTimesPage()
	roomList = RoomsPage.getRooms()
	print(roomList)
	print("Choosing Room:", roomList[0])
	RoomsPage.choose('213A')	
	return RoomsPage.next()

def TestRegisterPage():
	RegisterPage = TestRoomsPage()
	RegisterPage.setPhoneNum('9092738585')
	go = raw_input()
	RegisterPage.submit()

def TestNavigation():
	driver = webdriver.Firefox()
	Page = LoginPage(driver)
	Page.go('Search')
	Page.go('Times')
	Page.go('Locations')
	Page.go('Rooms')
	Page.back()

if '__main__' == __name__:
    #TestSetUp()
    #print("TestSetUp Done!")
    #TestLocationsPage()
    #TestTimesPage()
    TestRegisterPage()
    print("Test Done")
