namespace AutomationLab.Tests.Support;

/// <summary>
/// Access-token fixtures aligned with FakeAuthApi (prefix lab-token-*).
/// Prefer this or login reuse over inventing a parallel HTTP client.
/// </summary>
public static class AccessTokenData
{
    public const string Valid = "lab-token-valid_user";
    public const string FromRefresh = "lab-token-refreshed";
    public const string Invalid = "bad-token";
    public const string Empty = "";
}
