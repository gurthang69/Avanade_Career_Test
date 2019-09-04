import unittest

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome


class AvanadeTests(unittest.TestCase):
    def setUp(self):
        self.driver = driver()
        self.addCleanup(self.driver.quit)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.navigate_to_main_page()
        self.click_cookies()
        self.navigate_to_roles_and_locations()

    def test_find_10_jobs_or_more_in_Canada(self):
        self.search_for_jobs('Canada')
        self.assert_minimum_jobs_condition(10)

    def test_find_1_job_or_more_in_Denmark(self):
        self.search_for_jobs('Denmark')
        self.assert_minimum_jobs_condition(0)

    def test_find_agile_in_qualifications(self):
        self.search_for_jobs(search_term='Agile')
        self.driver.find_elements_by_css_selector('h3[role="jobname"]')[1].click()
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mainDetails')))
        description = (self.driver.find_element_by_class_name('mainDetails')).get_attribute('innerText')
        self.assertTrue('agile' in description.lower())

    def navigate_to_main_page(self):
        self.driver.get("http://avanade.com")

    def navigate_to_roles_and_locations(self):
        action = ActionChains(self.driver)
        action.move_to_element(
            self.driver.find_elements_by_xpath("//ul[contains(@class, 'nav')]//a[text()='Careers']")[1])
        action.click(self.driver.find_elements_by_xpath("//a[contains(text(),'Roles and Locations')]")[1])
        action.perform()

    def click_cookies(self):
        self.driver.find_element_by_class_name('accept-cookies-button').click()

    def search_for_jobs(self, country=None, search_term=None):
        roles_elem = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#main-navbar ul [href="/en/careers/roles-and-locations"]')))
        roles_elem.click()
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "saveButton")))
        if country:
            option_elems = self.driver.find_elements_by_css_selector("select option")
            country_elem = [e for e in option_elems if e.get_attribute("innerText") == country]
            country_elem[0].click()
        if search_term:
            self.driver.find_element_by_css_selector("#tpt_search").send_keys(search_term)
        self.driver.find_element_by_class_name('saveButton').click()
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".listJobs li")))

    def assert_minimum_jobs_condition(self, minimum):
        jobs = list(self.driver.find_elements_by_css_selector(".listJobs li"))
        jobs_length = len(jobs)
        while jobs_length < minimum:
            if not self.driver.find_element_by_css_selector(".nextLink"):
                break
            maincontent = self.driver.find_element_by_css_selector("#mainContent").location_once_scrolled_into_view
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nextLink")))
            self.driver.find_element_by_css_selector(".nextLink").click()
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".listJobs li")))
            jobs_length += len(list(self.driver.find_elements_by_css_selector(".listJobs li")))
        self.assertGreater(jobs_length, minimum)


if __name__ == '__main__':
    unittest.main()
