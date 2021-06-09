from behave import *
from selenium import webdriver

use_step_matcher("re")


@given('I am on "Register" page')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.server_url = 'http://127.0.0.1:8000'
    br = context.driver
    br.get(context.server_url + '/accounts/register')


@when('I submit a valid "Register" form')
def step_impl(context):
    br = context.driver

    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()

    br.find_element_by_name('email').send_keys('test_email@gmail.com')
    username = 'test_username'
    br.find_element_by_name('username').send_keys(username)
    try:
        context.dict['username'] = username
    except AttributeError:
        pass
    br.find_element_by_name('first_name').send_keys('test_first_name')
    br.find_element_by_name('last_name').send_keys('test_last_name')
    br.find_element_by_name('password1').send_keys('test_password')
    br.find_element_by_name('password2').send_keys('test_password')
    br.find_element_by_name('action').click()


@then("I am logged in")
def step_impl(context):
    br = context.driver

    assert br.find_element_by_xpath("//a[text()='LOGOUT']")
