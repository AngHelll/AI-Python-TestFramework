Feature: User profile
  As a QA engineer
  I want to fetch the authenticated user profile
  So we can verify AuthApiClient.GetProfile reuse

  @smoke @USER-PROFILE-GET
  Scenario: Get profile with a valid access token
    Given I have a valid access token
    When I request the user profile
    Then I should receive the lab user profile

  @USER-PROFILE-GET
  Scenario: Get profile with a token issued from refresh
    Given I have an access token from refresh
    When I request the user profile
    Then I should receive the lab user profile

  @negative @USER-PROFILE-GET
  Scenario: Profile is absent with an invalid access token
    Given I have an invalid access token
    When I request the user profile
    Then the user profile should be absent

  @negative @USER-PROFILE-GET
  Scenario: Profile is absent with an empty access token
    Given I have an empty access token
    When I request the user profile
    Then the user profile should be absent
