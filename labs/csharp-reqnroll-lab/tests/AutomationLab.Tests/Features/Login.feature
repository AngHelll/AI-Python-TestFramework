Feature: User Login API
  As a QA engineer
  I want deterministic Auth login scenarios
  So we can evaluate AI reuse of Builders and Validators

  # XRay-like tags for eval (synthetic)
  # @TEST_KEY: AUTH-LOGIN-*

  @smoke @login @AUTH-LOGIN-OK
  Scenario: Successful login with valid credentials
    When I login as a valid user
    Then the login should succeed
    And I should receive an access token

  @login @negative @AUTH-LOGIN-NEG
  Scenario: Failed login with invalid credentials
    When I login as an invalid user
    Then the login should fail with error "INVALID_CREDENTIALS"
    And an error message should be shown

  @login @security @AUTH-LOCKOUT
  Scenario: Account lockout after multiple failed attempts
    When I attempt login with wrong credentials 3 times for user "lock_me"
    Then the account should be locked
