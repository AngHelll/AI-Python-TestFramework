using AutomationLab.Clients;
using AutomationLab.Models;
using AutomationLab.Tests.Support;
using AutomationLab.Validators;
using FluentAssertions;
using Reqnroll;

namespace AutomationLab.Tests.Steps;

[Binding]
public sealed class TokenRefreshSteps
{
    private readonly AuthApiClient _client;
    private string? _refreshToken;
    private LoginResponse? _response;

    public TokenRefreshSteps(ScenarioContext scenarioContext)
    {
        var api = scenarioContext.Get<IAuthApi>("AuthApi");
        _client = new AuthApiClient(api);
    }

    [Given("I have a valid refresh token")]
    public void GivenIHaveAValidRefreshToken()
    {
        // Login does not emit refresh tokens in this lab; fabricate FakeAuthApi-compatible value.
        _refreshToken = RefreshTokenData.Valid;
    }

    [Given("I have an invalid refresh token")]
    public void GivenIHaveAnInvalidRefreshToken()
    {
        _refreshToken = RefreshTokenData.Invalid;
    }

    [Given("I have an empty refresh token")]
    public void GivenIHaveAnEmptyRefreshToken()
    {
        _refreshToken = RefreshTokenData.Empty;
    }

    [When("I refresh the access token")]
    public void WhenIRefreshTheAccessToken()
    {
        _response = _client.RefreshToken(_refreshToken ?? string.Empty);
    }

    [Then("I should receive a new access token")]
    public void ThenIShouldReceiveANewAccessToken()
    {
        _response.Should().NotBeNull();
        LoginResponseValidator.ShouldBeSuccessful(_response!);
        _response!.AccessToken.Should().Be("lab-token-refreshed");
    }

    [Then(@"the refresh should fail with error ""(.*)""")]
    public void ThenTheRefreshShouldFailWithError(string errorCode)
    {
        _response.Should().NotBeNull();
        LoginResponseValidator.ShouldFailWith(_response!, errorCode);
    }
}
