@smoke @errors
Feature: Demo service error mapping

  Background:
    * url baseUrl
    * configure headers = { Accept: 'application/json', Content-Type: 'application/json' }
    * def orderId = '22222222-2222-2222-2222-222222222222'

  Scenario: Order domain rule violations are mapped to problem details
    * def request = read('classpath:payloads/orders/create-hazmat-expedited-order.json')
    Given path '/api/orders'
    And request request
    When method post
    Then status 422
    And match response.title == 'Domain rule violation'

  Scenario: Inventory conflicts are mapped to problem details
    Given path '/api/retail/inventory/reservations'
    And request { orderId: '#(orderId)', sku: 'LOW-AT-001', quantity: 2 }
    When method post
    Then status 409
    And match response.title == 'Resource conflict'

  Scenario: Payment currency violations are mapped to problem details
    Given path '/api/retail/payments/authorizations'
    And request { orderId: '#(orderId)', amount: 10.00, currency: 'EUR', paymentToken: 'tok1_at_bad_currency' }
    When method post
    Then status 422
    And match response.title == 'Domain rule violation'
