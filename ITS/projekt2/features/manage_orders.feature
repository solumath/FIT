# Feature: Manage orders

#     Manage orders
#     Background: 
#         Given User is logged in as administrator

#     # Test 14
#     Scenario: Show order details
#         Given user is in administration on 'Orders' page
#         And sees order
#         When user clicks on view
#         Then order details are shown

#     # Test 15
#     Scenario: Update order history
#         Given user is viewing order
#         When user changes order status
#         And clicks 'Add History'
#         Then order history is updated

#     # Test 16
#     Scenario: Delete order
#         Given user is in administration on 'Orders' page
#         When user selects order
#         And clicks 'delete'
#         Then order is deleted

#     # Test 17
#     Scenario: Create order
#         Given user is creating a new order
#         When he fills all required fields
#         And clicks 'Confirm'
#         Then new order is created
#         And is visible on 'Orders' page
