Feature: Register
  As a User I should be able to
  register to page

  Background:
    Given I am on "Register" page

  Scenario: Create new account
    When I submit a valid "Register" form
    Then I am logged in
