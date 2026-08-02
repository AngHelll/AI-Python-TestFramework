namespace AutomationLab.Tests.Support;

/// <summary>
/// Deterministic refresh-token fixtures for the lab. Not a request Builder —
/// LoginRequestBuilder remains the canonical login payload builder.
/// </summary>
public static class RefreshTokenData
{
    public const string Valid = "lab-refresh-demo";
    public const string Invalid = "not-a-refresh-token";
    public const string Empty = "";
}
