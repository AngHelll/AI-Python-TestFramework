using AutomationLab.Models;

namespace AutomationLab.Builders;

/// <summary>
/// Canonical builder for Auth login requests. Prefer extending this over creating a duplicate.
/// </summary>
public sealed class LoginRequestBuilder
{
    private string _username = "valid_user";
    private string _password = "valid_password";
    private string? _clientId = "lab-client";

    public LoginRequestBuilder WithUsername(string username)
    {
        _username = username;
        return this;
    }

    public LoginRequestBuilder WithPassword(string password)
    {
        _password = password;
        return this;
    }

    public LoginRequestBuilder WithClientId(string? clientId)
    {
        _clientId = clientId;
        return this;
    }

    public LoginRequestBuilder AsValidUser()
    {
        _username = "valid_user";
        _password = "valid_password";
        return this;
    }

    public LoginRequestBuilder AsInvalidUser()
    {
        _username = "invalid_user";
        _password = "wrong_password";
        return this;
    }

    public LoginRequest Build() => new()
    {
        Username = _username,
        Password = _password,
        ClientId = _clientId
    };
}
