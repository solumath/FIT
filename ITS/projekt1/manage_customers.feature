Feature: Manage customers

    Manage customers
    Background: 
        Given User is logged in as administrator
        And user is in administration on 'Customers' page

    # Test 18
    Scenario: Create Customer
        Given user is in 'Add New' customer
        When user fills all required fields
        And clicks 'Save'
        Then customer is created

    # Test 19
    Scenario: Delete Customer
        When user selects customer
        And clicks 'Delete'
        Then customer is deleted

    # Test 20
    Scenario: Change password
        Given user is editing existing user
        When user changes password
        And clicks 'Save'
        Then 'You have modified customers!' is shown

    # Test 21
    Scenario: Edit address 
        Given user is editing existing user
        When user changes customer address
        And clicks 'Save'
        Then customer address is updated
