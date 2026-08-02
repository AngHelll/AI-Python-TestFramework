using AutomationLab.Models;

namespace AutomationLab.Validators;

/// <summary>
/// Validator for UserProfile. FakeAuthApi models unauthorized as null — callers
/// must assert presence/absence explicitly (no error codes on GetProfile today).
/// </summary>
public static class UserProfileValidator
{
    public static void ShouldExist(UserProfile? profile)
    {
        if (profile is null)
        {
            throw new InvalidOperationException("Expected a user profile but was null.");
        }

        Ensure(!string.IsNullOrWhiteSpace(profile.Username), "Expected Username.");
        Ensure(!string.IsNullOrWhiteSpace(profile.DisplayName), "Expected DisplayName.");
        Ensure(!string.IsNullOrWhiteSpace(profile.Role), "Expected Role.");
    }

    public static void ShouldMatchLabUser(UserProfile? profile)
    {
        ShouldExist(profile);
        Ensure(profile!.Username == "valid_user", $"Expected username 'valid_user' but was '{profile.Username}'.");
        Ensure(profile.DisplayName == "Lab User", $"Expected display name 'Lab User' but was '{profile.DisplayName}'.");
        Ensure(profile.Role == "tester", $"Expected role 'tester' but was '{profile.Role}'.");
    }

    public static void ShouldBeAbsent(UserProfile? profile)
    {
        if (profile is not null)
        {
            throw new InvalidOperationException("Expected no user profile (unauthorized) but profile was returned.");
        }
    }

    private static void Ensure(bool condition, string message)
    {
        if (!condition)
        {
            throw new InvalidOperationException(message);
        }
    }
}
