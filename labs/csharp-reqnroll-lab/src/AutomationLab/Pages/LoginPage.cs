using AutomationLab.Clients;
using AutomationLab.Models;

namespace AutomationLab.Pages;

/// <summary>
/// Thin UI-facing facade mirroring Python LoginPage responsibilities.
/// Lab uses the fake API underneath so tests stay deterministic.
/// </summary>
public sealed class LoginPage(AuthApiClient client)
{
    private LoginResponse? _lastResponse;

    public LoginResponse? LastResponse => _lastResponse;

    public bool IsPageLoaded() => true;

    public LoginResponse Submit(LoginRequest request)
    {
        _lastResponse = client.Login(request);
        return _lastResponse;
    }

    public bool IsLoginSuccessful() => _lastResponse is { Success: true };

    public bool IsErrorMessageDisplayed() =>
        !string.IsNullOrWhiteSpace(_lastResponse?.ErrorMessage);

    public bool IsLocked() => _lastResponse is { IsLocked: true };
}
