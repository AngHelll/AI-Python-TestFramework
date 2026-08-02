using AutomationLab.Models;

namespace AutomationLab.Validators;

/// <summary>
/// Canonical validator for login responses. Prefer reuse over asserting ad-hoc in steps.
/// </summary>
public static class LoginResponseValidator
{
    public static void ShouldBeSuccessful(LoginResponse response)
    {
        Ensure(response.Success, "Expected successful login.");
        Ensure(!string.IsNullOrWhiteSpace(response.AccessToken), "Expected access token.");
        Ensure(response.ErrorCode is null, "Expected no error code on success.");
        Ensure(!response.IsLocked, "Expected account not locked.");
    }

    public static void ShouldFailWith(LoginResponse response, string expectedErrorCode)
    {
        Ensure(!response.Success, "Expected login failure.");
        Ensure(response.AccessToken is null, "Expected no access token on failure.");
        Ensure(response.ErrorCode == expectedErrorCode,
            $"Expected error code '{expectedErrorCode}' but was '{response.ErrorCode}'.");
        Ensure(!string.IsNullOrWhiteSpace(response.ErrorMessage), "Expected error message.");
    }

    public static void ShouldBeLocked(LoginResponse response)
    {
        Ensure(!response.Success, "Expected login failure when locked.");
        Ensure(response.IsLocked, "Expected account locked.");
        Ensure(response.ErrorCode == "ACCOUNT_LOCKED",
            $"Expected ACCOUNT_LOCKED but was '{response.ErrorCode}'.");
    }

    private static void Ensure(bool condition, string message)
    {
        if (!condition)
        {
            throw new InvalidOperationException(message);
        }
    }
}
