using AutomationLab.Clients;
using AutomationLab.Models;
using AutomationLab.Tests.Support;
using AutomationLab.Validators;
using FluentAssertions;
using Reqnroll;

namespace AutomationLab.Tests.Steps;

[Binding]
public sealed class UserProfileSteps
{
    private readonly AuthApiClient _client;
    private string? _accessToken;
    private UserProfile? _profile;

    public UserProfileSteps(ScenarioContext scenarioContext)
    {
        var api = scenarioContext.Get<IAuthApi>("AuthApi");
        _client = new AuthApiClient(api);
    }

    [Given("I have a valid access token")]
    public void GivenIHaveAValidAccessToken()
    {
        _accessToken = AccessTokenData.Valid;
    }

    [Given("I have an access token from refresh")]
    public void GivenIHaveAnAccessTokenFromRefresh()
    {
        _accessToken = AccessTokenData.FromRefresh;
    }

    [Given("I have an invalid access token")]
    public void GivenIHaveAnInvalidAccessToken()
    {
        _accessToken = AccessTokenData.Invalid;
    }

    [Given("I have an empty access token")]
    public void GivenIHaveAnEmptyAccessToken()
    {
        _accessToken = AccessTokenData.Empty;
    }

    [When("I request the user profile")]
    public void WhenIRequestTheUserProfile()
    {
        _profile = _client.GetProfile(_accessToken ?? string.Empty);
    }

    [Then("I should receive the lab user profile")]
    public void ThenIShouldReceiveTheLabUserProfile()
    {
        UserProfileValidator.ShouldMatchLabUser(_profile);
    }

    [Then("the user profile should be absent")]
    public void ThenTheUserProfileShouldBeAbsent()
    {
        UserProfileValidator.ShouldBeAbsent(_profile);
        _profile.Should().BeNull();
    }
}
