@smoke @orders
Feature: Demo service order lifecycle

  Background:
    * url baseUrl
    * configure headers = { Accept: 'application/json', Content-Type: 'application/json' }

  Scenario: Create, read, list, and cancel an order
    * def createOrder = read('classpath:payloads/orders/create-standard-order.json')
    Given path '/api/orders'
    And request createOrder
    When method post
    Then status 201
    And match response.id == '#string'
    And match response.customerId == createOrder.customerId
    And match response.sku == createOrder.sku
    And match response.quantity == createOrder.quantity
    And match response.shippingPriority == 'EXPEDITED'
    And match response.requestedShipDate == '2026-02-05'
    And match response.status == 'CREATED'
    And match response.manualReviewRequired == false
    * def orderId = response.id
    And match responseHeaders['Location'][0] == '/api/orders/' + orderId

    Given path '/api/orders', orderId
    When method get
    Then status 200
    And match response.id == orderId
    And match response.status == 'CREATED'

    Given path '/api/orders/customers', createOrder.customerId
    When method get
    Then status 200
    And match response[*].id contains orderId

    * def updateStatus = read('classpath:payloads/orders/update-cancelled-order.json')
    Given path '/api/orders', orderId, 'status'
    And request updateStatus
    When method patch
    Then status 200
    And match response.id == orderId
    And match response.status == 'CANCELLED'
