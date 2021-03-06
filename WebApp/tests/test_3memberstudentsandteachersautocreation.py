# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys


class Test2Memberstudentsandteachersautocreation():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_2Memberstudentsandteachersautocreation(self):
        self.driver.get("http://127.0.0.1:8000/login/?next=/memberinfo/create/")
        self.driver.find_element(By.ID, "id_username").send_keys("nsdevil")
        self.driver.find_element(By.ID, "id_password").send_keys("nsdevil")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

        self.driver.find_element(By.ID, "id_Member_ID").send_keys("Culpa dolor adipisci")
        self.driver.find_element(By.ID, "id_username").send_keys("savezidotu")
        self.driver.find_element(By.ID, "id_first_name").send_keys("Julian")
        self.driver.find_element(By.ID, "id_last_name").send_keys("Chang")
        self.driver.find_element(By.ID, "id_email").send_keys("huto@mailinator.com")
        dropdown = self.driver.find_element(By.ID, "id_Member_Gender")
        dropdown.find_element(By.XPATH, "//option[. = 'Male']").click()
        self.driver.find_element(By.ID, "id_Is_Student").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()


        self.driver.get("http://127.0.0.1:8000/login/?next=/memberinfo/create/")
        self.driver.find_element(By.ID, "id_Member_ID").send_keys("Nulla in eu velit ad")
        self.driver.find_element(By.ID, "id_username").send_keys("hehoquluw")
        self.driver.find_element(By.ID, "id_first_name").send_keys("Isaac")
        self.driver.find_element(By.ID, "id_last_name").send_keys("Robles")
        self.driver.find_element(By.ID, "id_email").send_keys("qoha@mailinator.net")
        dropdown = self.driver.find_element(By.ID, "id_Member_Gender")
        dropdown.find_element(By.XPATH, "//option[. = 'Female']").click()
        self.driver.find_element(By.ID, "id_Is_Student").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()


        self.driver.get("http://127.0.0.1:8000/login/?next=/memberinfo/create/")
        self.driver.find_element(By.ID, "id_Member_ID").send_keys("Eos quidem pariatur")
        self.driver.find_element(By.ID, "id_username").send_keys("wegonufy")
        self.driver.find_element(By.ID, "id_first_name").send_keys("Felix")
        self.driver.find_element(By.ID, "id_last_name").send_keys("Harrison")
        self.driver.find_element(By.ID, "id_email").send_keys("zalymetin@mailinator.net")
        dropdown = self.driver.find_element(By.ID, "id_Member_Gender")
        self.driver.find_element(By.ID, "id_Is_Student").click()
        dropdown.find_element(By.XPATH, "//option[. = 'Female']").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()

        self.driver.get("http://127.0.0.1:8000/login/?next=/memberinfo/create/")
        self.driver.find_element(By.ID, "id_Member_ID").send_keys("Mollit placeat est")
        self.driver.find_element(By.ID, "id_username").send_keys("dilenuz")
        self.driver.find_element(By.ID, "id_first_name").send_keys("Pearl")
        self.driver.find_element(By.ID, "id_last_name").send_keys("Henson")
        self.driver.find_element(By.ID, "id_email").send_keys("xesybimaz@mailinator.com")
        dropdown = self.driver.find_element(By.ID, "id_Member_Gender")
        dropdown.find_element(By.XPATH, "//option[. = 'Male']").click()
        self.driver.find_element(By.ID, "id_Is_Student").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()


        self.driver.get("http://127.0.0.1:8000/login/?next=/memberinfo/create/")
        self.driver.find_element(By.ID, "id_Member_ID").send_keys("Quas qui in dolor do")
        self.driver.find_element(By.ID, "id_username").send_keys("selapi")
        self.driver.find_element(By.ID, "id_first_name").send_keys("Helen")
        self.driver.find_element(By.ID, "id_last_name").send_keys("Haley")
        self.driver.find_element(By.ID, "id_email").send_keys("cyxori@mailinator.net")
        dropdown = self.driver.find_element(By.ID, "id_Member_Gender")
        self.driver.find_element(By.ID, "id_Is_Student").click()
        dropdown.find_element(By.XPATH, "//option[. = 'Female']").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()


        self.driver.get("http://127.0.0.1:8000/login/?next=/memberinfo/create/")
        self.driver.find_element(By.ID, "id_Member_ID").send_keys("Aute odit id et est ")
        self.driver.find_element(By.ID, "id_username").send_keys("noboledod")
        self.driver.find_element(By.ID, "id_first_name").send_keys("Stephanie")
        self.driver.find_element(By.ID, "id_last_name").send_keys("Patton")
        self.driver.find_element(By.ID, "id_email").send_keys("gomyxo@mailinator.net")
        dropdown = self.driver.find_element(By.ID, "id_Member_Gender")
        dropdown.find_element(By.XPATH, "//option[. = 'Female']").click()
        self.driver.find_element(By.ID, "id_Is_Teacher").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()


        self.driver.get("http://127.0.0.1:8000/login/?next=/memberinfo/create/")
        self.driver.find_element(By.ID, "id_Member_ID").send_keys("Modi doloremque maio")
        self.driver.find_element(By.ID, "id_username").send_keys("haduhi")
        self.driver.find_element(By.ID, "id_first_name").send_keys("Sloane")
        self.driver.find_element(By.ID, "id_last_name").send_keys("Leach")
        self.driver.find_element(By.ID, "id_email").send_keys("nozigyx@mailinator.com")
        dropdown = self.driver.find_element(By.ID, "id_Member_Gender")
        dropdown.find_element(By.XPATH, "//option[. = 'Female']").click()
        self.driver.find_element(By.CSS_SELECTOR, ".col-md-3:nth-child(3)").click()
        self.driver.find_element(By.ID, "id_Is_Teacher").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()


        self.driver.get("http://127.0.0.1:8000/login/?next=/memberinfo/create/")
        self.driver.find_element(By.ID, "id_Member_ID").send_keys("Eius reprehenderit ")
        self.driver.find_element(By.ID, "id_username").send_keys("fafofapyti")
        self.driver.find_element(By.ID, "id_first_name").send_keys("MacKenzie")
        self.driver.find_element(By.ID, "id_last_name").send_keys("Murphy")
        self.driver.find_element(By.ID, "id_email").send_keys("ketutoqab@mailinator.net")
        dropdown = self.driver.find_element(By.ID, "id_Member_Gender")
        dropdown.find_element(By.XPATH, "//option[. = 'Male']").click()
        self.driver.find_element(By.ID, "id_Is_Teacher").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()

        self.driver.get("http://127.0.0.1:8000/memberinfo/")
        assert self.driver.find_element(By.ID, "DataTables_Table_0_info").text == "Showing 1 to 8 of 8 entries"