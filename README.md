# 🤖 AI-Powered Python Selenium Automation Framework

**Production-ready test automation framework with complete AI assistance context for code generation, debugging, and learning.**

---

## ✨ What Makes This Framework Special?

This isn't just another test framework - it's **AI-enhanced** with ~70KB of technical context that enables AI assistants (ChatGPT, Claude, Copilot) to:
- 🎯 Generate tests following framework patterns
- 🐛 Debug issues with framework-specific knowledge
- 📝 Write code matching your conventions
- 🎓 Teach you automation concepts
- 🚀 Accelerate development 10x

---

## 🚀 Key Features

### **Core Framework**
- **Page Object Model (POM)** - Clean separation of test logic and page structure
- **Dual Test Approaches** - Pytest (technical) + Behave (BDD)
- **Multi-Browser Support** - Chrome, Firefox, Edge
- **Parallel Execution** - Run tests concurrently for faster feedback
- **Retry Mechanisms** - Handle flaky tests automatically
- **Screenshot Capture** - Auto-capture on failures
- **Comprehensive Logging** - Detailed execution logs
- **Environment Configuration** - Flexible `.env`-based setup
- **Docker Ready** - Containerized execution for CI/CD

### **🤖 AI-Powered Features** ⭐ NEW!
- **Complete AI Context** - ~70KB of technical documentation
- **Framework Knowledge** - Architecture, patterns, best practices
- **Code Generation** - AI can generate page objects, tests, utilities
- **Intelligent Debugging** - AI understands framework-specific issues
- **Learning Assistant** - Built-in tutorials and examples
- **Few-Shot Examples** - Training data for consistent code generation

---

## AI evolution lab (roadmap)

Evolución de few-shot → plataforma gobernada (Analyst → Planner → Builder → Reviewer + gates).  
Índice: [docs/ai-evolution/README.md](docs/ai-evolution/README.md) · Blueprint portable: [PORTABLE-BLUEPRINT.md](docs/ai-evolution/PORTABLE-BLUEPRINT.md).

```bash
bash scripts/run_all_smokes.sh
cd labs/csharp-reqnroll-lab && dotnet test
```

Credenciales solo en local: `cp .env.example .env` (el archivo `.env` no se versiona).

## 🤖 AI Assistant Integration

### **What's Included:**

```
prompts/
├── context/              # 📚 Complete technical reference
│   ├── FRAMEWORK.md     # Complete framework guide (200+ lines)
│   ├── architecture.md  # Design patterns and architecture
│   ├── bdd_with_behave.md # BDD implementation guide
│   ├── best_practices.md  # Coding standards
│   └── troubleshooting.md # Problem-solving guide
│
├── system/              # 🎯 AI behavior instructions
│   └── SYSTEM_PROMPT.md # How AI should assist
│
└── examples/            # 💡 Training examples
    └── few_shot_examples.json # Q&A pairs
```

### **How to Use with AI:**

#### **ChatGPT / Claude:**
```
1. Copy context from prompts/context/FRAMEWORK.md
2. Paste into chat
3. Ask: "Generate a page object for login"
4. AI generates code following your patterns!
```

#### **GitHub Copilot:**
```
1. Open prompts/context/ files in IDE
2. Copilot learns your framework
3. Get context-aware suggestions
4. Autocomplete matches your style
```

#### **Cursor AI:**
```
1. Reference prompts/context/ files
2. Cursor understands framework context
3. Chat with framework knowledge
4. Generate tests matching patterns
```

### **Example AI Interaction:**

**You:** "Create a checkout page object"

**AI (with framework context):**
```python
# pages/checkout_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import TestSettings

class CheckoutPage(BasePage):
    """Checkout page object"""
    
    LOCATORS = {
        'total_price': (By.ID, "total"),
        'checkout_button': (By.ID, "checkout-btn"),
    }
    
    def _get_page_url(self) -> str:
        return f"{TestSettings.BASE_URL}/checkout"
    
    def is_page_loaded(self) -> bool:
        return self.is_element_visible(*self.LOCATORS['checkout_button'])
```

✅ **Perfect framework pattern!**
✅ **Correct imports!**
✅ **Follows conventions!**
✅ **Ready to use!**

---

## 📦 Quick Start

### **1. Installation**

```bash
# Clone repository
git clone <repository-url>
cd AutomationFramework

# Install dependencies
pip install -r requirements.txt

# Setup configuration
cp .env.example .env
# Edit .env with your settings
```

### **2. Run Tests**

```bash
# Pytest (technical tests)
pytest                          # All tests
pytest -n auto                  # Parallel execution
pytest -v                       # Verbose output
pytest tests/test_login.py      # Specific file

# Behave (BDD tests)
behave                          # All BDD scenarios
behave --tags=smoke            # Smoke tests only
behave features/login.feature  # Specific feature
```

### **3. With Docker**

```bash
# Build image
docker build -t automation-framework .

# Run tests
docker run automation-framework pytest -v
docker run automation-framework behave
```

---

## 🎯 Project Structure

```
AutomationFramework/
├── 📁 config/                 # Framework configuration
│   ├── settings.py           # Centralized settings
│   └── browser_setup.py      # Browser initialization
│
├── 📁 pages/                  # Page Object Model
│   ├── base_page.py          # Abstract base class
│   └── *_page.py             # Concrete page objects
│
├── 📁 tests/                  # Pytest test suites
│   └── test_*.py             # Test files
│
├── 📁 features/               # BDD test suites
│   ├── *.feature             # Gherkin scenarios
│   ├── steps/                # Step definitions
│   └── environment.py        # Behave hooks
│
├── 📁 utils/                  # Utilities
│   ├── logger.py             # Logging utility
│   ├── retry_mechanism.py    # Retry logic
│   ├── screenshot_capture.py # Screenshots
│   └── test_data_loader.py   # Test data
│
├── 📁 prompts/ ⭐ AI Context  # AI-powered assistance
│   ├── context/              # Technical documentation
│   ├── examples/             # Few-shot learning
│   └── system/               # AI instructions
│
├── 📁 docs/                   # Documentation
│   ├── GUIA_NOVATOS.md       # Spanish beginner guide
│   ├── DOCKER_GUIDE.md       # Docker usage guide
│   └── CI_COMPARISON.md      # CI/CD comparison
│
└── 📁 test_data/              # Test data
    └── test_data.json        # JSON test data
```

---

## ⚙️ Configuration

Edit `.env` file:

```env
# Browser Settings
BROWSER=chrome              # chrome|firefox|edge
HEADLESS=true              # Run without GUI

# Timeouts
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20

# Features
SCREENSHOT_ON_FAILURE=true
RETRY_COUNT=3
RETRY_DELAY=2

# Environment
TEST_ENV=staging
BASE_URL=https://example.com
```

---

## 📝 Writing Tests

### **Pytest Test Example:**

```python
import pytest
from pages.login_page import LoginPage

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup_test(self, driver):
        self.login_page = LoginPage(driver)
    
    def test_successful_login(self):
        """Test user can login with valid credentials"""
        self.login_page.navigate_to_page()
        self.login_page.login("user", "password")
        assert self.login_page.is_login_successful()
```

### **BDD Test Example:**

```gherkin
# features/login.feature
Feature: User Login
  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    Then I should be logged in
```

---

## 🤖 AI-Assisted Development

### **Ask AI to:**

#### **Generate Code:**
```
"Create a page object for the dashboard"
"Write a test for user registration"
"Add a utility function to generate test data"
```

#### **Debug Issues:**
```
"Why is my test failing with ElementNotFound?"
"How do I wait for dynamic elements?"
"Best way to handle popups in this framework?"
```

#### **Learn Concepts:**
```
"Explain how the retry mechanism works"
"What's the difference between Pytest and Behave tests?"
"How does the Page Object Model improve maintainability?"
```

#### **Optimize Code:**
```
"Make this test run faster"
"How to parallelize these tests?"
"Best practices for test data management?"
```

### **AI Gives You:**
- ✅ Code matching framework patterns
- ✅ Solutions using framework utilities
- ✅ Explanations with framework context
- ✅ Best practices for this specific framework

---

## 🐳 Docker Support

### **Local Docker Usage:**

```bash
# Build
docker build -t automation-framework .

# Run tests
docker run automation-framework pytest -v
docker run automation-framework behave

# With reports
docker run -v $(pwd)/reports:/app/reports automation-framework
```

### **CI/CD Docker Usage:**

Framework includes two GitHub Actions workflows:
- ⚡ **ci.yml** - Direct approach (fast, recommended)
- 🐳 **ci-with-docker.yml** - Docker approach (for learning)

Both include extensive comments explaining every step!

---

## 📚 Documentation

### **📖 For Humans:**
- **[README.md](README.md)** - This file (quick start)
- **[docs/GUIA_NOVATOS.md](docs/GUIA_NOVATOS.md)** - Spanish beginner guide (20KB)
- **[docs/DOCKER_GUIDE.md](docs/DOCKER_GUIDE.md)** - Complete Docker guide (626 lines)
- **[docs/CI_COMPARISON.md](docs/CI_COMPARISON.md)** - CI/CD approaches compared

### **🤖 For AI Assistants:**
- **[prompts/FRAMEWORK.md](prompts/context/FRAMEWORK.md)** - Complete technical reference
- **[prompts/architecture.md](prompts/context/architecture.md)** - Architecture deep dive
- **[prompts/bdd_with_behave.md](prompts/context/bdd_with_behave.md)** - BDD guide
- **[prompts/best_practices.md](prompts/context/best_practices.md)** - Coding standards
- **[prompts/troubleshooting.md](prompts/context/troubleshooting.md)** - Problem solving

### **📊 Navigation:**

| Need | Go To |
|------|-------|
| Get started | This README |
| Learn framework (Spanish) | `docs/GUIA_NOVATOS.md` |
| Use Docker | `docs/DOCKER_GUIDE.md` |
| Compare CI approaches | `docs/CI_COMPARISON.md` |
| **AI code generation** | **`prompts/context/FRAMEWORK.md`** ⭐ |
| Technical deep dive | `prompts/context/` |
| Version history | `CHANGELOG.md` |

---

## 🎓 Learning Path

### **Beginner:**
1. Read this README
2. Run example tests: `pytest tests/test_login.py`
3. Check `docs/GUIA_NOVATOS.md` (Spanish guide)
4. Ask AI: "Explain how this framework works"

### **Intermediate:**
1. Create your first page object
2. Write custom tests
3. Use AI to generate code
4. Read `prompts/context/FRAMEWORK.md`

### **Advanced:**
1. Add new utilities
2. Integrate with CI/CD
3. Use Docker for testing
4. Contribute to framework

---

## 🚀 CI/CD Integration

### **GitHub Actions:**

Framework includes documented workflows:

```yaml
# .github/workflows/ci.yml
# ⚡ Fast direct approach (recommended)
# - Every step explained
# - Emoji indicators
# - Debugging tips included

# .github/workflows/ci-with-docker.yml  
# 🐳 Docker approach (for learning)
# - Complete tutorial format
# - 3 jobs: Docker, Direct, Comparison
# - Performance analysis included
```

Both workflows:
- ✅ Run automatically on push
- ✅ Support manual triggers
- ✅ Generate HTML reports
- ✅ Include comprehensive comments

---

## 💡 Pro Tips

### **Use AI for Rapid Development:**
```bash
# 1. Load AI context
cat prompts/context/FRAMEWORK.md | pbcopy

# 2. Paste in ChatGPT/Claude

# 3. Generate code:
"Create a page object for search functionality"
"Write 5 tests for the shopping cart"
"Add error handling to the login test"

# 4. Copy generated code → Use immediately!
```

### **Debug with AI:**
```bash
# When test fails:
# 1. Copy error message
# 2. Share with AI (has framework context loaded)
# 3. Get framework-specific solution
# 4. Fix in seconds!
```

### **Learn Continuously:**
```bash
# Ask AI (with context):
"What's the best way to handle dynamic content?"
"Show me examples of data-driven tests"
"Explain the retry mechanism implementation"

# Get answers specific to YOUR framework!
```

---

## 📈 Framework Stats

- **Test Execution:** 14 passed, 2 skipped (87.5% pass rate)
- **BDD Scenarios:** 3 feature files with multiple scenarios
- **Documentation:** ~150KB total (human + AI)
- **AI Context:** ~70KB optimized for code generation
- **Languages:** English + Spanish
- **CI/CD:** 2 workflows (direct + Docker)

---

## 🤝 Why This Framework?

### **For Solo Developers:**
- ✅ AI assistance accelerates development
- ✅ Learn best practices from generated code
- ✅ Quick setup and execution
- ✅ Comprehensive documentation

### **For Teams:**
- ✅ Consistent code patterns (AI enforces)
- ✅ Fast onboarding with AI help
- ✅ Self-documenting with AI context
- ✅ Scales from 1 to 1000 tests

### **For Learning:**
- ✅ Real-world framework structure
- ✅ AI explains every concept
- ✅ Multiple documentation levels
- ✅ Practical examples included

---

## 🎯 Next Steps

### **1. Start Using:**
```bash
pytest -v          # Run tests
behave            # Run BDD scenarios
```

### **2. Use AI Assistance:**
```bash
# Load prompts/context/FRAMEWORK.md into AI
# Ask: "Generate a test for X"
# Get production-ready code!
```

### **3. Explore Documentation:**
```bash
ls docs/          # Human guides
ls prompts/       # AI context
```

### **4. Extend Framework:**
```bash
# Ask AI: "How do I add a new page object?"
# Follow generated instructions
# Add your own tests!
```

---

## 🌟 Special Features

- 🤖 **AI-First Design** - Built with AI assistance in mind
- 📚 **Self-Documenting** - Code and docs together
- 🎓 **Educational** - Learn while building
- 🚀 **Production-Ready** - Used in real projects
- 🐳 **Container-Ready** - Docker support included
- ⚡ **Fast** - Parallel execution by default
- 🔄 **Reliable** - Retry mechanisms built-in
- 📊 **Observable** - Comprehensive logging

---

## 📞 Support

- 📖 **Read docs:** `docs/` directory
- 🤖 **Ask AI:** Load `prompts/context/FRAMEWORK.md`
- 🐛 **Debug:** Check `prompts/context/troubleshooting.md`
- 🎓 **Learn:** Spanish guide in `docs/GUIA_NOVATOS.md`

---

## ⭐ Requirements

- Python 3.9+
- Chrome/Firefox/Edge browser
- pip package manager
- (Optional) Docker for containerized testing

---

## 📄 License

[Add your license here]

---

## 🎉 What You Get

✅ **Production-ready framework**  
✅ **AI-powered code generation**  
✅ **Comprehensive documentation**  
✅ **Real-world patterns**  
✅ **Learning resources**  
✅ **CI/CD ready**  
✅ **Docker support**  
✅ **Active development**

---

**🚀 Start automating with AI assistance today!**

```bash
# Quick start
git clone <your-repo>
cd AutomationFramework
pip install -r requirements.txt
pytest -v  # You're running tests!

# With AI help
# 1. Open prompts/context/FRAMEWORK.md
# 2. Copy to ChatGPT/Claude
# 3. Ask: "Generate a test for user login"
# 4. Get production-ready code instantly!
```

---

**Framework Version:** 1.2.0  
**Status:** ✅ Production Ready | 🤖 AI-Enhanced  
**Made with:** ❤️  + 🤖 AI Collaboration
