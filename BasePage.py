
class BasePage(object):
	url = None

	def __init__(self, driver):
		self.driver = driver

	def fill_form_by_id(self, form_element_id, value):
		elem = self.driver.find_element_by_id(form_element_id)
		elem.send_keys(value)
		return elem

	def go(self):
		self.driver.get(self.url)	

	def wait(self, delay=3):
		self.driver.implicitly_wait(delay)

	def close(self):
		self.driver.close()
