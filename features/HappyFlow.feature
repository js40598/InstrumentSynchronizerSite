Feature: Register
  As a User I should be able to
  use every function which
  is available for me

  Scenario: Happy Flow
    Given I am on "Home" page
    When I click on "REGISTER" button
    And I submit a valid "Register" form
    And I click on "Synchronizer" button
    And I click on "My Projects" button
    And I click on "Add Project" button
    And I submit a valid "Add Project" form
    And I click on "Project" button
    And I click on "Add Recording" button
    And I submit a valid "Add Recording" form
    And I submit a valid "Cut Recording" form
    And I click on "Synchronize" button
    Then File can be downloaded
