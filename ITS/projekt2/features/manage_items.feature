Feature: Manage items

    Manage items
    Background: 
        Given User is in administration on 'Catalog' page

    # Test 8
    Scenario: Find item
        When user searches for 'Canon EOS 5D'
        Then item is shown with available stock

    # Test 9
    Scenario: Delete item
        When user selects item
        And clicks 'Delete'
        Then item is deleted

    # # Test 10
    # Scenario: Add new item
    #     Given user is on 'Add New' in products
    #     When user fills all required fields
    #     Then item is created

    # Test 11
    Scenario: Filter items by price
        When user filters by price '200'
        Then item only 'Samsung SyncMaster 941BW' is shown

    # Test 12
    Scenario: Filter items by quantity
        When user filters quantity 'xxx'
        Then error should be shown 'Invalid number'

    # Test 13
    Scenario: Find item and change stock
        When user clicks on edit
        And changes quantity of available item
        And clicks 'Save'
        Then item is updated
