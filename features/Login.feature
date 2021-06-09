Feature: Login
  As a User I should be able to
  login to page

  Background:
    Given I am on "Login" page

  Scenario: Log in correctly
    Given I have an account
    When I submit a valid "Login" form
    Then I am logged in
