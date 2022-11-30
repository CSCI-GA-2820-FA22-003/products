Feature: The product store service back-end
    As a  Product manager
    I need a RESTful product service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | price | description          |
        | book       | 15    | sci-fi               |
        | iphone     | 799   | personal electronics |
        | soap       | 8     | home necessity       |
        | bed sheet  | 25    | household products   |

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Products RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "home page"
    And I set the "name" to "watch"
    And I set the "price" to "50"
    And I set the "description" to "waterpoof and handmade"
    And I press the "create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "clear" button
    Then the "id" field should be empty
    And the "name" field should be empty
    And the "price" field should be empty
    When I paste the "id" field
    And I press the "retrieve" button
    Then I should see the message "Success"
    And I should see "watch" in the "name" field
    And I should see "50" in the "price" field
    And I should see "waterpoof and handmade" in the "description" field
    And I should see "true" in the "onshelf" field

Scenario: List all products
    When I visit the "home page"
    And I press the "search" button
    Then I should see the message "Success"
    And I should see "book" in the results
    And I should see "iphone" in the results
    And I should not see "dishwasher" in the results

Scenario: Search by names
    When I visit the "home page"
    And I set the "name" to "book"
    And I press the "search" button
    Then I should see the message "Success"
    And I should see "book" in the results
    And I should not see "watch" in the results
    And I should not see "iphone" in the results

Scenario: Search by price
    When I visit the "home page"
    And I set the "price" to "700"
    And I press the "search" button
    Then I should see the message "Success"
    And I should see "soap" in the results
    And I should see "book" in the results
    And I should see "bed sheet" in the results
    And I should not see "iphone" in the results

Scenario: Search by description
    When I visit the "home page"
    And I set the "description" to "electronics"
    And I press the "search" button
    Then I should see the message "Success"
    And I should see "iphone" in the results
    And I should not see "book" in the results
    And I should not see "bed sheet" in the results
    And I should not see "soap" in the results


Scenario: Update a Product
    When I visit the "home page"
    And I set the "name" to "book"
    And I press the "search" button
    Then I should see the message "Success"
    And I should see "book" in the "name" field
    And I should see "15" in the "price" field
    When I change "name" to "magazine"
    And I press the "update" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "clear" button
    And I paste the "id" field
    And I press the "retrieve" button
    Then I should see the message "Success"
    And I should see "magazine" in the "name" field
    When I press the "clear" button
    And I press the "search" button
    Then I should see the message "Success"
    And I should see "magazine" in the results
    And I should not see "book" in the results

Scenario: Delete a Product
    When I visit the "home page"
    And I set the "name" to "mouse_delete"
    And I set the "price" to "40"
    And I set the "description" to "for computer"
    And I press the "create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "clear" button
    Then the "id" field should be empty
    And the "name" field should be empty
    And the "price" field should be empty
    And the "description" field should be empty
    When I paste the "id" field
    And I press the "delete" button
    Then I should see the message "Product has been Deleted!"
    When I set the "name" to "mouse_delete"
    And I press the "search" button
    Then I should see the message "Success"
    And I should not see "mouse_delete" in the results


Scenario: Like a Product
    When I visit the "home page"
    And I set the "name" to "iphone"
    And I press the "search" button
    Then I should see the message "Success"
    And I should see "iphone" in the "name" field
    And I should see "0" in the "likes" field
    When I copy the "id" field
    And I press the "like" button
    Then I should see the message "Product has been liked!"
    When I press the "clear" button
    And I paste the "id" field
    And I press the "retrieve" button
    Then I should see the message "Success"
    And I should see "iphone" in the "name" field
    And I should see "1" in the "likes" field


Scenario: Dislike a Product
    When I visit the "home page"
    And I set the "name" to "bed sheet"
    And I press the "search" button
    Then I should see the message "Success"
    And I should see "bed sheet" in the "name" field
    And I should see "0" in the "likes" field
    When I copy the "id" field
    And I press the "dislike" button
    Then I should see the message "Product has been disliked!"
    When I press the "clear" button
    And I paste the "id" field
    And I press the "retrieve" button
    Then I should see the message "Success"
    And I should see "bed sheet" in the "name" field
    And I should see "-1" in the "likes" field

Scenario: Onshelf and Offshelf a Product
    When I visit the "home page"
    And I set the "name" to "iphone"
    And I press the "search" button
    Then I should see the message "Success"
    And I should see "iphone" in the "name" field
    And I should see "true" in the "onshelf" field
    When I copy the "id" field 
    And I press the "off-shelf" button
    Then I should see the message "Product is now off shelf"
    When I press the "clear" button
    And I paste the "id" field
    And I press the "retrieve" button
    Then I should see the message "Success"
    And I should see "iphone" in the "name" field
    And I should see "false" in the "onshelf" field
    When I set the "name" to "iphone"
    And I press the "search" button
    Then I should see the message "Success"
    And I should see "iphone" in the "name" field
    And I should see "false" in the "onshelf" field
    When I copy the "id" field
    And I press the "on-shelf" button
    Then I should see the message "Product is now on shelf"
    When I press the "clear" button
    And I paste the "id" field
    And I press the "retrieve" button
    Then I should see the message "Success"
    And I should see "iphone" in the "name" field
    And I should see "true" in the "onshelf" field