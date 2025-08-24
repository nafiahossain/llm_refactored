# Tool-Using Agent

A robust, production-ready agent that intelligently uses different tools to answer various types of queries including calculations, weather lookups, knowledge base searches, and translations.

## Features

- **Calculator**: Mathematical expressions, percentages, natural language math
- **Weather**: Temperature lookups for cities worldwide  
- **Knowledge Base**: Searchable information database
- **Translator**: Multi-language translation support
- **Robust Error Handling**: Recovers from malformed responses and invalid inputs
- **Extensible Architecture**: Easy to add new tools
- **Type Safety**: Full Pydantic validation throughout
- **Comprehensive Testing**: 95%+ test coverage

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Agent System                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐    ┌──────────────┐    ┌──────────────────┐    │
│  │  Agent  │───►│ LLM Service  │───►│ Response Parser  │    │
│  │         │    │              │    │                  │    │
│  └─────────┘    └──────────────┘    └──────────────────┘    │
│       │                                       │             │
│       ▼                                       │             │
│  ┌─────────────────┐                          │             │
│  │ Tool Registry   │◄─────────────────────────┘             │
│  │                 │                                        │
│  │ ┌─────────────┐ │                                        │
│  │ │ Calculator  │ │                                        │
│  │ │ Weather     │ │                                        │
│  │ │ Knowledge   │ │                                        │
│  │ │ Translator  │ │                                        │
│  │ └─────────────┘ │                                        │
│  └─────────────────┘                                        │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd tool-using-agent

# Option 1: Traditional setup
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Option 2: Modern setup (recommended)
pip install -e ".[dev]"
```

### Basic Usage

```bash
# Mathematical calculations
python main.py "What is 12.5% of 243?"
python main.py "What is 15 + 27 * 3?"

# Weather queries  
python main.py "What's the temperature in Paris?"
python main.py "Weather in London"

# Knowledge base lookups
python main.py "Who is Ada Lovelace?"
python main.py "Who is Alan Turing?"

# Translations
python main.py "Translate hello to Spanish"
python main.py "Translate goodbye to French"

# Complex queries
python main.py "Add 10 to the temperature in Paris"
```

### Using the Makefile

```bash
# Show all available commands
make help

# Setup development environment
make setup

# Run tests
make test          # Quick tests
make test-v        # Verbose output
make test-cov      # With coverage report

# Code quality
make fmt           # Format code with black/isort
make lint          # Run linting checks

# Run examples
make run           # Single example
make examples  # Multiple examples

# # Docker
# make docker-build  # Build container
# make docker-run    # Run example in container

# Cleanup
make clean         # Remove build artifacts
```

## Development

### Project Structure

```
tool-using-agent/
├── agent/                  # Main package
│   ├── __init__.py        
│   ├── agent.py           # Main agent orchestration
│   ├── schemas.py         # Pydantic data models
│   ├── llm.py             # LLM service abstraction
│   ├── parser.py          # Response parsing with error recovery
│   ├── tool_registry.py   # Tool management
│   └── tools/             # Tool implementations
│       ├── __init__.py
│       ├── base.py        # Abstract base class
│       ├── calculator.py  # Mathematical operations
│       ├── weather.py     # Weather lookups
│       ├── knowledge_base.py # KB searches
│       └── translator.py  # Language translation
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_tools.py      # Tool unit tests
│   ├── test_agent.py      # Agent tests
│   ├── test_integration.py # End-to-end tests
│   ├── test_schemas.py    # Data validation tests
│   └── test_parser.py     # Response parsing tests
├── data/                  # Data files
│   └── kb.json           # Knowledge base entries
├── main.py               # CLI entry point
├── Makefile              # Build automation
├── pyproject.toml        # Modern Python project config
├── Dockerfile            # Container definition
└── requirements.txt      # Core dependencies
```

### Adding New Tools

1. **Create Tool Class**:

```python
from agent.tools.base import BaseTool
from agent.schemas import ToolResult
from typing import Dict, Any

class MyNewTool(BaseTool):
    @property
    def name(self) -> str:
        return "mynew"
    
    def validate_args(self, args: Dict[str, Any]) -> bool:
        return "input" in args and isinstance(args["input"], str)
    
    def execute(self, args: Dict[str, Any]) -> ToolResult:
        if not self.validate_args(args):
            return ToolResult(
                success=False,
                result="",
                error="Invalid arguments",
                tool_used=self.name
            )
        
        # Your tool logic here
        result = process_input(args["input"])
        
        return ToolResult(
            success=True,
            result=result,
            tool_used=self.name
        )
```

2. **Update Schema** (add to `ToolType` enum in `schemas.py`):

```python
class ToolType(str, Enum):
    # ... existing tools ...
    MYNEW = "mynew"
```

3. **Register Tool** (in `tool_registry.py`):

```python
def _register_default_tools(self):
    default_tools = [
        # ... existing tools ...
        MyNewTool()
    ]
```

4. **Add Tests**:

```python
class TestMyNewTool:
    def setup_method(self):
        self.tool = MyNewTool()
    
    def test_basic_functionality(self):
        result = self.tool.execute({"input": "test"})
        assert result.success
        assert result.result == "expected_output"
```

### Testing

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_tools.py -v          # Tool tests
pytest tests/test_integration.py -v    # Integration tests  
pytest tests/test_agent.py -v          # Agent tests

# Run with coverage
pytest --cov=agent --cov-report=html

# Test specific functionality
pytest -k "calculator" -v              # Only calculator tests
pytest -k "integration" -v             # Only integration tests
```

## 🐳 Docker Usage

### Basic Docker Commands

```bash
# Build the image
docker build -t tool-agent .

# Run single query
docker run --rm tool-agent python main.py "What is 2 + 2?"

# Interactive mode
docker run -it --rm tool-agent bash

# Using docker-compose for development
docker-compose up tool-agent
docker-compose exec tool-agent python main.py "test query"
```

### Docker Features

- **Security**: Runs as non-root user
- **Optimization**: Multi-layer caching for faster builds  
- **Health checks**: Container monitoring
- **Development**: Volume mounting for live development

## API Usage

### Programmatic Usage

```python
from agent.agent import Agent

# Create agent instance
agent = Agent(use_fake_llm=True)

# Ask questions
result = agent.answer("What is 15% of 200?")
print(result)  # "30.0"

result = agent.answer("Weather in Tokyo")  
print(result)  # "22.0°C"

result = agent.answer("Who is Grace Hopper?")
print(result)  # "Grace Hopper was a computer programming pioneer..."
```

### Direct Tool Usage

```python
from agent.tools import CalculatorTool, TranslatorTool

# Use tools directly
calc = CalculatorTool()
result = calc.execute({"expr": "10 + 5"})
print(result.result)  # 15.0

translator = TranslatorTool()
result = translator.execute({
    "text": "hello", 
    "target_language": "spanish"
})
print(result.result)  # "hola"
```

## Configuration

### Environment Variables

```bash
# Optional environment variables
export PYTHONPATH=/path/to/project
export PYTHONUNBUFFERED=1  # For Docker
```

### LLM Configuration

```python
# Use fake LLM (default, for development)
agent = Agent(use_fake_llm=True)

# Use real LLM (extend for production)
agent = Agent(use_fake_llm=False)
```

### Knowledge Base

Edit `data/kb.json` to add new knowledge entries:

```json
{
  "entries": [
    {
      "name": "Your Person",
      "summary": "Description of the person..."
    }
  ]
}
```

## Dependencies

### Core Dependencies (`requirements.txt`)
```
pydantic>=2.0.0  # Data validation and settings management
pytest>=7.0.0    # Testing framework
```

### Development Dependencies (`requirements-dev.txt`)
```
pytest-cov>=4.0.0  # Test coverage
black>=23.0.0       # Code formatting
isort>=5.0.0        # Import sorting
flake8>=6.0.0       # Linting
mypy>=1.0.0         # Type checking
```

### Installation Options

```bash
# Minimal install
pip install .

# Development install (recommended for contributors)
pip install -e ".[dev]"

# Testing only
pip install -e ".[test]"

# Linting tools only  
pip install -e ".[lint]"
```

## Testing Strategy

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end system testing  
- **Robustness Tests**: Error conditions and edge cases
- **Schema Tests**: Data validation testing
- **Parser Tests**: Response parsing with malformed inputs

### Test Coverage

Current test coverage: **95%+**

```bash
# Generate coverage report
make test-cov

# View detailed HTML report
open htmlcov/index.html
```

### Continuous Integration

The project includes GitHub Actions workflow for:
- Multi-Python version testing (3.10, 3.11, 3.12)
- Code quality checks (black, isort, flake8, mypy)
- Test coverage reporting
- Docker image building and testing

## Error Handling

### Robust Response Parsing

The system handles various LLM response formats:

```python
# Valid JSON
'{"tool": "calc", "args": {"expr": "1+1"}}'

# Malformed JSON (automatically fixed)
'{"tool": "calc", "args": {"expr": "1+1"'  # Missing }

# Alternative formats
'TOOL:calc EXPR="1+1"'

# Direct answers
"The answer is 42"
```

### Input Validation

All tool inputs are validated:

```python
# Valid input
{"expr": "2 + 3"}  

# Invalid input  
{"expr": 123}      X -> Returns error message
{}                 X -> Returns error message
```

### Safe Execution

- **Calculator**: Prevents code injection via `eval()`
- **File Operations**: Proper error handling for missing files
- **Network**: Graceful handling of connection issues (when using real APIs)

## Performance

### Optimization Features

- **Lazy Loading**: Tools instantiated only when needed
- **Error Recovery**: System continues with partial failures
- **Type Safety**: Pydantic validation prevents runtime errors
- **Resource Management**: Proper cleanup and memory management

### Scalability Considerations

- **Async Ready**: Architecture supports async tool execution
- **Caching**: Can be extended with result caching
- **Load Balancing**: Multiple agent instances supported
- **Monitoring**: Structured logging for observability

## 📈 Future Enhancements

Potential areas for extension:

1. **Real LLM Integration**: OpenAI, Anthropic, or local LLM support
2. **Async Tools**: Long-running operations support
3. **Tool Chaining**: Execute multiple tools in sequence  
4. **Caching**: Cache expensive operations
5. **Metrics**: Usage analytics and performance monitoring
6. **Config Management**: External configuration files
7. **API Interface**: REST API wrapper
8. **Database**: Persistent storage for knowledge base
9. **Authentication**: User auth and authorization
10. **Rate Limiting**: Protection against abuse

## License

MIT License - see LICENSE file for details.

## Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/new-feature`)
3. **Add** comprehensive tests for your changes
4. **Run** quality checks (`make fmt`)
5. **Update** documentation as needed
6. **Commit** your changes (`git commit -m 'Add new feature'`)
7. **Push** to the branch (`git push origin feature/new-feature`)
8. **Open** a Pull Request

### Development Setup for Contributors

```bash
# Fork and clone the repo
git clone https://github.com/nafiahossain/llm_refactored.git
cd llm_refactored

# Setup development environment
make setup
pip install -e ".[dev]"

# Make changes and test
make check  # Run all quality checks
make test   # Run tests

# Before committing
make fmt    # Format code
make lint   # Check for issues
```

## Acknowledgments

- **Pydantic**: For excellent data validation
- **pytest**: For comprehensive testing framework
- **Python Community**: For modern packaging standards (PEP 518/621)

---
