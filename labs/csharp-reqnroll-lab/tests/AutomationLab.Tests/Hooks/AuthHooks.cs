using AutomationLab.Clients;
using Reqnroll;

namespace AutomationLab.Tests.Hooks;

[Binding]
public sealed class AuthHooks
{
    private readonly ScenarioContext _scenarioContext;

    public AuthHooks(ScenarioContext scenarioContext)
    {
        _scenarioContext = scenarioContext;
    }

    [BeforeScenario]
    public void BeforeScenario()
    {
        // Fresh fake API per scenario → deterministic failed-attempt counters.
        _scenarioContext.Set<IAuthApi>(new FakeAuthApi(), "AuthApi");
    }
}
