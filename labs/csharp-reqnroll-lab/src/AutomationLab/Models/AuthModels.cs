namespace AutomationLab.Models;

public sealed class LoginRequest
{
    public required string Username { get; init; }
    public required string Password { get; init; }
    public string? ClientId { get; init; }
}

public sealed class LoginResponse
{
    public required bool Success { get; init; }
    public string? AccessToken { get; init; }
    public string? ErrorCode { get; init; }
    public string? ErrorMessage { get; init; }
    public bool IsLocked { get; init; }
}

public sealed class UserProfile
{
    public required string Username { get; init; }
    public required string DisplayName { get; init; }
    public required string Role { get; init; }
}
