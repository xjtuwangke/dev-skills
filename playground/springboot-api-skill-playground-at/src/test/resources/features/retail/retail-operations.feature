@smoke @retail
Feature: Demo service retail operations

  Background:
    * url baseUrl
    * configure headers = { Accept: 'application/json', Content-Type: 'application/json' }
    * def orderId = '11111111-1111-1111-1111-111111111111'

  Scenario: Read customer, catalog, promotion, and audit surfaces
    Given path '/api/retail/customers/ent-at-001/profile'
    When method get
    Then status 200
    And match response.customerId == 'ent-at-001'
    And match response.segment == 'ENTERPRISE'
    And match response.defaultCurrency == 'USD'

    Given path '/api/retail/catalog/items/SKU-AT-001'
    When method get
    Then status 200
    And match response.sku == 'SKU-AT-001'
    And match response.status == 'ACTIVE'
    And match response.currency == 'USD'
    And match response.hazardous == false

    Given path '/api/retail/promotions/SAVE20/eligibility'
    And param customerId = 'customer-at-001'
    And param sku = 'SKU-AT-001'
    When method get
    Then status 200
    And match response.couponCode == 'SAVE20'
    And match response.eligible == true
    And match response.discountAmount == 20.00

    Given path '/api/retail/audit/orders', orderId
    When method get
    Then status 200
    And match response.subjectId == orderId
    And match response.subjectType == 'ORDER'
    And match response.events contains 'ORDER_CREATED'

  Scenario: Exercise write operations that do not require persisted order state
    * def reservation = read('classpath:payloads/retail/inventory-reservation.json')
    * set reservation.orderId = orderId
    Given path '/api/retail/inventory/reservations'
    And request reservation
    When method post
    Then status 200
    And match response.sku == reservation.sku
    And match response.status == 'RESERVED'
    And match response.reservedQuantity == reservation.quantity

    * def quote = read('classpath:payloads/retail/price-quote.json')
    Given path '/api/retail/pricing/quotes'
    And request quote
    When method post
    Then status 200
    And match response.sku == quote.sku
    And match response.quantity == quote.quantity
    And match response.priceRule == 'DISCOUNTED'
    And match response.currency == 'USD'

    * def payment = read('classpath:payloads/retail/payment-authorization.json')
    * set payment.orderId = orderId
    Given path '/api/retail/payments/authorizations'
    And request payment
    When method post
    Then status 200
    And match response.authorized == true
    And match response.authorizationCode == '#string'

    * def shipment = read('classpath:payloads/retail/shipment-plan.json')
    * set shipment.orderId = orderId
    Given path '/api/retail/fulfillment/plans'
    And request shipment
    When method post
    Then status 200
    And match response.warehouseCode == 'DFW-01'
    And match response.carrier == 'ACME-PARCEL'
    And match response.serviceLevel == 'GROUND'

    * def returnRequest = read('classpath:payloads/retail/return-authorization.json')
    * set returnRequest.orderId = orderId
    Given path '/api/retail/returns/authorizations'
    And request returnRequest
    When method post
    Then status 200
    And match response.approved == true
    And match response.disposition == 'RESTOCK'

    * def ticket = read('classpath:payloads/retail/support-ticket.json')
    * set ticket.orderId = orderId
    Given path '/api/retail/support/tickets'
    And request ticket
    When method post
    Then status 200
    And match response.customerId == ticket.customerId
    And match response.status == 'OPEN'
