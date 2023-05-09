Feature: Search and add to cart

    Search and add to cart
    # Test 1
    Scenario: Search item
        Given user is on index page
        When user searches for 'macbook'
        Then page with following products is shown:
            | product     |
            | MacBook     |
            | MacBook Air |
            | MacBook Pro |

    # Test 2
    Scenario: Add to cart
        Given user is on index page
        And user has empty cart
        When user clicks 'Add to cart'
        Then user sees item in cart

    # Test 3
    Scenario: Search and add to cart
        Given user is on index page
        When user searches for 'iphone'
        Then page with following products is shown:
            | product |
            | iPhone  |
        And user clicks 'Add to cart'
        Then user sees item in cart

    # Test 4
    Scenario: Remove item
        Given user is on 'Shopping cart' page
        And user has item in cart
        When user clicks 'Remove' on item
        Then item is removed from cart

    # Test 5
    Scenario: Checkout items
        Given user is on 'Checkout' page
        And user is not logged in
        And user has item in cart
        When user fills required fields
        And clicks on 'Confirm order'
        Then user is logged in and 'Order has been placed' is shown 
