Feature: Register and see history of purchases

    Register and see history of purchases

    # Test 6
    Scenario: Register user
        Given user is on registration
        And user is not logged in
        When user fills all required fields
        And checks 'I have read and agree...'
        Then page with 'Your Account Has Been Created!' is shown

    # Test 7
    Scenario: See history
        Given user is logged in
        And user is on 'My account'
        When user clicks 'Order History'
        Then user sees his order with status 'Pending'
