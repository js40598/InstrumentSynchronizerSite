from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

use_step_matcher("re")


@given('I am on "Home" page')
def step_impl(context):
    options = Options()
    options.add_argument("--kiosk")
    context.driver = webdriver.Chrome(chrome_options=options)
    context.server_url = 'http://127.0.0.1:8000'
    context.dict = dict()
    context.driver.get(context.server_url)


@when('I click on "REGISTER" button')
def step_impl(context):
    time.sleep(0.5)
    context.driver.find_element_by_xpath("//a[text()='REGISTER']").click()


@step('I click on "Synchronizer" button')
def step_impl(context):
    time.sleep(0.5)
    context.driver.find_element_by_xpath("//a[text()='SYNCHRONIZER']").click()


@step('I click on "My Projects" button')
def step_impl(context):
    time.sleep(0.5)
    context.driver.find_element_by_xpath("//a[text()='My Projects']").click()


@step('I click on "Add Project" button')
def step_impl(context):
    time.sleep(0.5)
    context.driver.find_element_by_xpath("//a[contains(@href,'/synchronizer/create')]").click()


@step('I submit a valid "Add Project" form')
def step_impl(context):
    time.sleep(0.5)
    br = context.driver

    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()

    project_title = 'test_title'
    br.find_element_by_name('title').send_keys(project_title)
    try:
        context.dict['project_title'] = project_title
    except AttributeError:
        pass
    br.find_element_by_name('bpm').send_keys('60')
    br.find_element_by_name('description').send_keys('test_description')
    br.find_element_by_name('creation_submit').click()


@step('I click on "Project" button')
def step_impl(context):
    time.sleep(0.5)
    context.driver.find_element_by_xpath("//td/a[text()='{}']".format(context.dict['project_title'])).click()


@step('I click on "Add Recording" button')
def step_impl(context):
    time.sleep(0.5)
    context.driver.find_element_by_xpath("//h5/a/button").click()


@step('I submit a valid "Add Recording" form')
def step_impl(context):
    time.sleep(0.5)
    br = context.driver

    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()

    br.find_element_by_name('file').send_keys(os.path.join(os.getcwd(), 'features', 'steps', 'record10sec.wav'))
    br.find_element_by_name('instrument').send_keys('test_instrument')
    br.find_element_by_name('identifier').send_keys('test_identifier')
    br.find_element_by_name('pitch').send_keys('test_pitch')
    br.find_element_by_name('author').send_keys('test_author')
    br.find_element_by_name('action').click()


@step('I submit a valid "Cut Recording" form')
def step_impl(context):
    time.sleep(0.5)
    context.driver.find_element_by_name('action').click()


@step('I click on "Synchronize" button')
def step_impl(context):
    time.sleep(0.5)
    context.driver.find_element_by_xpath('//form/div/button').click()


@then("File can be downloaded")
def step_impl(context):
    time.sleep(5)
