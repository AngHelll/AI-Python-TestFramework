Feature: Token refresh
  As a QA engineer
  I want to refresh access tokens via the Auth API
  So sessions can continue without re-login

  # Golden story AUTH-TOKEN-REFRESH (implemented from approved Gate 2 plan)

  @smoke @AUTH-TOKEN-REFRESH
  Scenario: Refresh access token with a valid refresh token
    Given I have a valid refresh token
    When I refresh the access token
    Then I should receive a new access token

  @negative @AUTH-TOKEN-REFRESH
  Scenario: Refresh fails with an invalid refresh token
    Given I have an invalid refresh token
    When I refresh the access token
    Then the refresh should fail with error "INVALID_REFRESH"

  @negative @AUTH-TOKEN-REFRESH
  Scenario: Refresh fails with an empty refresh token
    Given I have an empty refresh token
    When I refresh the access token
    Then the refresh should fail with error "INVALID_REFRESH"
