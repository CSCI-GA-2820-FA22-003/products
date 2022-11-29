Feature: The product store service back-end
    As a  Product manager
    I need a RESTful product service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | price | description          | like_num | is_on_shelf |
        | book       | 15    | sci-fi               | 511      | True        |
        | iphone     | 799   | personal electronics | 7100     | True        |
        | soap       | 8     | home necessity       | 15       | True        |
        | bed sheet  | 25    | household products   | 51       | False       |

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Products RESTful Service Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "home page"
    And I set the "Name" to "watch"
    And I set the "Price" to "50"
    And I set the "Description" to "waterpoof and handmade"
    And I select "True" in the "On Shelf" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Price" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "watch" in the "Name" field
    And I should see "50" in the "Price" field
    And I should see "waterpoof and handmade" in the "Description" field
    And I should see "True" in the "On shelf" field

Scenario: List all products
    When I visit the "home page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "book" in the results
    And I should see "iphone" in the results
    And I should not see "dishwasher" in the results

Scenario: Search by names
    When I visit the "home page"
    And I set the "Name" to "book"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "book" in the results
    And I should not see "watch" in the results
    And I should not see "iphone" in the results

Scenario: Search by price
    When I visit the "home page"
    And I set the "Price" to "10"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "soap" in the results
    And I should not see "book" in the results
    And I should see "iphone" in the results
    And I should not see "bed sheet" in the results

Scenario: Update a Product
    When I visit the "home page"
    And I set the "Name" to "book"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "book" in the "Name" field
    And I should see "15" in the "Price" field
    When I change "Name" to "book_2"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "book_2" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "book_2" in the results
    And I should not see "book" in the results

Scenario: Delete a Product
    When I visit the "home page"
    And I set the "Name" to "mouse_delete"
    And I set the "Price" to "40"
    And I set the "Description" to "for computer"
    And I select "True" in the "On Shelf" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Price" field should be empty
    And the "Description" field should be empty
    When I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Product has been Deleted!"
    When I set the "Name" to "mouse_delete"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "mouse_delete" in the results


Scenario: Like a Product
    When I visit the "home page"
    And I set the "Name" to "iphone"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "iphone" in the "Name" field
    And I should see "7100" in the "Like Count" field
    When I press the "Like" button
    Then I should see the message "Product has been liked!"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "iphone" in the "Name" field
    And I should see "7101" in the "Like Count" field


Scenario: Dislike a Product
    When I visit the "home page"
    And I set the "Name" to "bed sheet"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "bed sheet" in the "Name" field
    And I should see "51" in the "Like Count" field
    When I press the "Dislike" button
    Then I should see the message "Product has been disliked!"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "bed sheet" in the "Name" field
    And I should see "50" in the "Like Count" field


Scenario: Onshelf a Product
    When I visit the "home page"
    And I set the "Name" to "bed sheet"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "bed sheet" in the "Name" field
    And I should see "False" in the "On Shelf" field
    When I I press the "On Shelf" button
    Then I should see the message "Product is now on shelf"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "bed sheet" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "bed sheet" in the "Name" field
    And I should see "True" in the "Onshelf" field

Scenario: Offshelf a Product
    When I visit the "home page"
    And I set the "Name" to "iphone"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "iphone" in the "Name" field
    And I should see "True" in the "On Shelf" field
    When I I press the "Off Shelf" button
    Then I should see the message "Product is now off shelf"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "iphone" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "iphone" in the "Name" field
    And I should see "False" in the "Onshelf" field