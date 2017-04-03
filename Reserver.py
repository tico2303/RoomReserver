from BasePage import BasePage

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from time import sleep
import re


class AvaialbeTimesPage(BasePage):
	pass

class LoginPage(BasePage):
	url = 'http://ucr.evanced.info/dibs/Login'

	def setCreds(self, lib_card_num, paswd):
		self.fill_form_by_id("tbxPatronLibCard", lib_card_num)
		self.fill_form_by_id("tbxPatronPin", paswd)
	def submit(self):
		self.driver.find_element_by_id('btnLoginSubmit').click()
		return AvailableTimesPage(self.driver)


class LocationsPage(BasePage):
	pass

class AvailableTimesPage(BasePage):
	url = 'http://ucr.evanced.info/dibs/Search'
	__timeDict = {'AnyTime':'A', 
				  'Now':'N',
				  'Morning':'M',
				  'Afternoon':'Af',
				  'Evening':'E'
					}

	def setHours(self, hours):
		self.__wait(15)
		if hours not in [1,2,3]:
			return "Error in Selecting hours in ", url, " only can be 1, 2, or 3 hours" 
		self.fill_form_by_id('SelectedTime', hours)

	def setTime(self, time):
		timeSort = self.fill_form_by_id('SelectedTimeSort', self.__timeDict[time])	

	def setDate(self, date):
		SearchDate = self.driver.find_element_by_id('SelectedSearchDate')
		select = Select(SearchDate)
		select.select_by_value(date)

	def getDates(self):
		datesFullText = []
		dateNumerical = []

		html = self.driver.page_source
		soup = BeautifulSoup(html, "lxml")
		dropDown = soup.find('select', attrs={'id':'SelectedSearchDate'})
		options = dropDown.find_all('option')	
		
		#populating optionsList with Dates
		for opt in options:
			#print opt.get_text()	
			datesFullText.append(opt.get_text().encode('ascii','ignore'))

		for opt in options:
			#print opt.get('value')
			dateNumerical.append(opt.get('value').encode('ascii','ignore'))

		return dateNumerical	

	def next(self):
		SearchBtn =self.driver.find_element_by_class_name('btn-container')
		SearchBtn.click()
		return LocationsPage(self.driver)

	def __getDates(self):
		pass



	def __wait(self, delay=5):
		self.driver.implicitly_wait(delay)


class TimesPage(BasePage):
	pass

class LocationsPage(BasePage):
	url = 'http://ucr.evanced.info/dibs/Locations'
	__xpath = ""
	def choose(self, Library):
		if Library.lower() == 'orbach':
			self.__xpath = '//*[@id="frmBuildings"]/div/div[2]/div[1]/div'
		elif Library.lower() == 'rivera':
			self.__xpath = '//*[@id="frmBuildings"]/div/div[2]/div[2]/div/div[2]/em'

	def next(self):
		building = self.driver.find_element(By.XPATH, self.__xpath)
		building.click()
		self.wait(10)
		return TimesPage(self.driver)

class RoomsPage(BasePage):
	pass

class TimesPage(BasePage):
	url = 'http://ucr.evanced.info/dibs/Times#'
	timeList = []
	timeListindex=None

	def getTimes(self):
        #BeautifulSoup to get all available times
		suburl = 'Times'
		current_url = self.driver.current_url
		while(suburl not in current_url):
			current_url = self.driver.current_url

		timeout = 15
		element_present = EC.presence_of_element_located((By.CLASS_NAME, 'item-link'))
		WebDriverWait(self.driver, timeout).until(element_present)

		html = self.driver.page_source
		soup = BeautifulSoup(html, "lxml")
		timeTable = soup.find_all('div', attrs={'class':'item-link'})


		#creating a list of all available room times
		for t in timeTable:
			text = t.get_text().encode('ascii','ignore').strip('\n\t').split(' ')
			time1 = text[0] +text[1] +text[2]
			time1 = time1.rstrip('\n')
			spaces = ''.join(text[-2:])
			if time1 not in self.timeList:
				self.timeList.append(time1)
		return self.timeList

	def choose(self, desiredTime):
		if desiredTime in self.timeList:
			self.timeListindex = self.timeList.index(desiredTime)
			return self.timeList[self.timeListindex]
		else:
			return None

	def next(self):
		try:
			itemLinks = self.driver.find_elements(By.CLASS_NAME,'item-link')
			itemLinks[self.timeListindex].click()
			print("len(itemLinks): ", len(itemLinks))
			print("self.__timeListindex: ", self.timeListindex)
			return RoomsPage(self.driver)
		except:
			print("len(itemLinks): ", len(itemLinks))
			print("self.__timeListindex: ", self.timeListindex, " out of range")
			self.close()
			exit(0)

class RegisterPage(BasePage):
	pass

class RoomsPage(BasePage):
	url = 'http://ucr.evanced.info/dibs/'
	__roomIndex = None
	__roomNumbersList = []


	def getRooms(self):
		timeout = 15
		element_present = EC.presence_of_element_located((By.ID, 'frmRooms'))
		WebDriverWait(self.driver, timeout).until(element_present)

		roomNumbersList = []
		html = self.driver.page_source
		soup = BeautifulSoup(html, "lxml")
		roomTable = soup.find_all('div', attrs={'class':'item-link'})

		pattern ='(\d\d\d[A]*)' 
		for r in roomTable:
			rtext = r.get_text().encode('ascii','ignore').strip('\n\t').split(' ')
			rtext = ''.join(rtext)
			result = re.search(pattern, rtext)
			rtext = result.group(0)
			#//Make sure that a room was found, i.e. rtext is not null or empty.
			roomNumbersList.append(rtext)
		self.__roomNumbersList = roomNumbersList
		return roomNumbersList

	def choose(self, room):
		if room in self.__roomNumbersList:
			self.__roomIndex = self.__roomNumbersList.index(room)

	def next(self):
		studyRooms = self.driver.find_elements(By.CLASS_NAME, 'item-link')
		studyRooms[self.__roomIndex].click()
		return RegisterPage(self.driver)


class RegisterPage(BasePage):

	def wait(self, timeout=15):
		element_present = EC.presence_of_element_located((By.ID, 'Phone'))
		WebDriverWait(self.driver, timeout).until(element_present)

	def setPhoneNum(self, phoneNum):
		self.wait()
		self.fill_form_by_id('Phone', phoneNum)

	def submit(self):
		self.wait()
		try:
			DibsBtn = self.driver.find_element(By.ID, 'btnCallDibs')
			DibsBtn.click()
		except:
			print("Couldn't find submit button")

		try:
			button = self.driver.find_element(By.LINK_TEXT,"OK")
			if button.is_displayed():
				#f.write("Error after trying to reserve room: " + self.curr_room + "\n")
				button.click()
				time.sleep(2)
		except:
			print "Room Reserved Successfully."
			time.sleep(2)
			self.driver.close()	



