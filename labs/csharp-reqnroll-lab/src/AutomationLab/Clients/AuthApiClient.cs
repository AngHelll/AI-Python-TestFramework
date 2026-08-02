using AutomationLab.Models;

namespace AutomationLab.Clients;

public interface IAuthApi
{
    LoginResponse Login(LoginRequest request);
    LoginResponse RefreshToken(string refreshToken);
    UserProfile? GetProfile(string accessToken);
}

/// <summary>
/// Deterministic in-memory Auth API for the lab (no network).
/// </summary>
public sealed class FakeAuthApi : IAuthApi
{
    private readonly Dictionary<string, int> _failedAttempts = new(StringComparer.OrdinalIgnoreCase);
    private const int LockoutThreshold = 3;

    public LoginResponse Login(LoginRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Username) || string.IsNullOrWhiteSpace(request.Password))
        {
            return Fail("INVALID_INPUT", "Username and password are required.");
        }

        if (_failedAttempts.TryGetValue(request.Username, out var attempts) && attempts >= LockoutThreshold)
        {
            return new LoginResponse
            {
                Success = false,
                IsLocked = true,
                ErrorCode = "ACCOUNT_LOCKED",
                ErrorMessage = "Account locked after multiple failed attempts."
            };
        }

        var valid = request.Username == "valid_user" && request.Password == "valid_password";
        if (!valid)
        {
            _failedAttempts[request.Username] = attempts + 1;
            if (_failedAttempts[request.Username] >= LockoutThreshold)
            {
                return new LoginResponse
                {
                    Success = false,
                    IsLocked = true,
                    ErrorCode = "ACCOUNT_LOCKED",
                    ErrorMessage = "Account locked after multiple failed attempts."
                };
            }

            return Fail("INVALID_CREDENTIALS", "Invalid username or password.");
        }

        _failedAttempts.Remove(request.Username);
        return new LoginResponse
        {
            Success = true,
            AccessToken = $"lab-token-{request.Username}",
            IsLocked = false
        };
    }

    public LoginResponse RefreshToken(string refreshToken)
    {
        // Intentionally incomplete surface for AUTH-TOKEN-REFRESH planning scenarios.
        if (string.IsNullOrWhiteSpace(refreshToken) || !refreshToken.StartsWith("lab-refresh-", StringComparison.Ordinal))
        {
            return Fail("INVALID_REFRESH", "Refresh token is invalid.");
        }

        return new LoginResponse
        {
            Success = true,
            AccessToken = "lab-token-refreshed",
            IsLocked = false
        };
    }

    public UserProfile? GetProfile(string accessToken)
    {
        if (string.IsNullOrWhiteSpace(accessToken) || !accessToken.StartsWith("lab-token-", StringComparison.Ordinal))
        {
            return null;
        }

        return new UserProfile
        {
            Username = "valid_user",
            DisplayName = "Lab User",
            Role = "tester"
        };
    }

    private static LoginResponse Fail(string code, string message) => new()
    {
        Success = false,
        ErrorCode = code,
        ErrorMessage = message,
        IsLocked = false
    };
}

public sealed class AuthApiClient(IAuthApi api)
{
    public LoginResponse Login(LoginRequest request) => api.Login(request);

    public LoginResponse RefreshToken(string refreshToken) => api.RefreshToken(refreshToken);

    public UserProfile? GetProfile(string accessToken) => api.GetProfile(accessToken);
}
