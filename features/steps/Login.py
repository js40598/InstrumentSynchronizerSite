from behave import *
from selenium import webdriver
from synchronizer.models import Project
import django
import InstrumentSynchronizerSite.settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InstrumentSynchronizerSite.settings")
from django.conf import settings

use_step_matcher("re")


@given('I am on "Login" page')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.server_url = 'http://127.0.0.1:8000'
    br = context.driver
    br.get(context.server_url + '/accounts/login')


@given("I have an account")
def step_impl(context):
    pass


@when('I submit a valid "Login" form')
def step_impl(context):
    br = context.driver

    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()

    br.find_element_by_name('username').send_keys('test_username')
    br.find_element_by_name('password').send_keys('test_password')
    br.find_element_by_name('action').click()
