using AutomationLab.Builders;
using AutomationLab.Clients;
using AutomationLab.Models;
using AutomationLab.Pages;
using AutomationLab.Validators;
using FluentAssertions;
using Reqnroll;

namespace AutomationLab.Tests.Steps;

[Binding]
public sealed class LoginSteps
{
    private readonly ScenarioContext _scenarioContext;
    private readonly AuthApiClient _client;
    private readonly LoginPage _loginPage;
    private LoginResponse? _response;

    public LoginSteps(ScenarioContext scenarioContext)
    {
        _scenarioContext = scenarioContext;
        var api = _scenarioContext.Get<IAuthApi>("AuthApi");
        _client = new AuthApiClient(api);
        _loginPage = new LoginPage(_client);
    }

    [When("I login as a valid user")]
    public void WhenILoginAsAValidUser()
    {
        var request = new LoginRequestBuilder().AsValidUser().Build();
        _response = _loginPage.Submit(request);
    }

    [When("I login as an invalid user")]
    public void WhenILoginAsAnInvalidUser()
    {
        var request = new LoginRequestBuilder().AsInvalidUser().Build();
        _response = _loginPage.Submit(request);
    }

    [When(@"I attempt login with wrong credentials (\d+) times for user ""(.*)""")]
    public void WhenIAttemptLoginWithWrongCredentials(int times, string username)
    {
        for (var i = 0; i < times; i++)
        {
            var request = new LoginRequestBuilder()
                .WithUsername(username)
                .WithPassword("wrong_password")
                .Build();
            _response = _loginPage.Submit(request);
        }
    }

    [Then("the login should succeed")]
    public void ThenTheLoginShouldSucceed()
    {
        _response.Should().NotBeNull();
        LoginResponseValidator.ShouldBeSuccessful(_response!);
    }

    [Then("I should receive an access token")]
    public void ThenIShouldReceiveAnAccessToken()
    {
        _response!.AccessToken.Should().NotBeNullOrWhiteSpace();
    }

    [Then(@"the login should fail with error ""(.*)""")]
    public void ThenTheLoginShouldFailWithError(string errorCode)
    {
        _response.Should().NotBeNull();
        LoginResponseValidator.ShouldFailWith(_response!, errorCode);
    }

    [Then("an error message should be shown")]
    public void ThenAnErrorMessageShouldBeShown()
    {
        _loginPage.IsErrorMessageDisplayed().Should().BeTrue();
    }

    [Then("the account should be locked")]
    public void ThenTheAccountShouldBeLocked()
    {
        _response.Should().NotBeNull();
        LoginResponseValidator.ShouldBeLocked(_response!);
    }
}
