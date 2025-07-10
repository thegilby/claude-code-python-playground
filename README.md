# Claude Test Generator

A Python tool that uses the Claude Code SDK to automatically generate unit tests for existing Python projects. This tool leverages Claude's advanced code understanding capabilities to analyze Python files and create comprehensive test suites using popular testing frameworks like pytest.

## Features

- Generate unit tests for individual Python files
- Process entire directories of Python files
- Support for multiple testing frameworks (pytest, unittest, etc.)
- Interactive demo mode for easy experimentation
- Comprehensive test coverage with edge cases
- REPL-friendly design for interactive development
- Powered by Claude Code SDK for enhanced code understanding

## Prerequisites

- Python 3.10+
- Node.js (for Claude Code CLI)
- Claude Code CLI: `npm install -g @anthropic-ai/claude-code`

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the Claude Code CLI:
```bash
npm install -g @anthropic-ai/claude-code
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Anthropic API key (if required):
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY if needed
```

## Usage

### From Python REPL

```python
import anyio
from claude_test_generator import ClaudeTestGenerator

# Initialize the generator
generator = ClaudeTestGenerator()

# Generate tests for a single file (async)
async def generate_tests():
    test_code = await generator.generate_tests("path/to/your/file.py")
    print(test_code)

anyio.run(generate_tests)

# Generate tests for an entire directory (async)
async def generate_directory_tests():
    generated_files = await generator.generate_tests_for_directory("path/to/your/project")
    print(f"Generated {len(generated_files)} test files")

anyio.run(generate_directory_tests)
```

### Interactive Demo

Run the interactive demo to try the tool:

```bash
python claude_test_generator.py
```

Or from Python REPL:

```python
import anyio
from claude_test_generator import demo_interactive
anyio.run(demo_interactive)
```

### Command Line Usage

```bash
# Run interactive demo
python claude_test_generator.py

# See example usage patterns
python example_usage.py
```

## API Reference

### ClaudeTestGenerator

Main class for generating tests using Claude Code SDK.

#### Methods

- `__init__(cwd: Optional[str] = None, max_turns: int = 10)`: Initialize with working directory and conversation limits
- `async generate_tests(python_file_path: str, test_framework: str = "pytest") -> str`: Generate tests for a single file
- `async generate_tests_for_directory(directory_path: str, output_dir: str = "tests") -> List[str]`: Generate tests for all Python files in a directory
- `analyze_python_file(file_path: str) -> str`: Read and return Python file contents

#### Configuration Options

- `cwd`: Working directory for Claude Code operations
- `max_turns`: Maximum conversation turns with Claude (default: 10)
- `allowed_tools`: Tools Claude can use (Read, Write)
- `permission_mode`: Permission level for tool usage

## Examples

### Generate Tests for a Calculator Module

```python
import anyio
from claude_test_generator import ClaudeTestGenerator

async def generate_calculator_tests():
    # Your calculator.py file
    calculator_code = """
def add(a, b):
    return a + b

def multiply(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a * b

class Calculator:
    def __init__(self):
        self.history = []
    
    def calculate(self, operation, a, b):
        if operation == "add":
            result = add(a, b)
        elif operation == "multiply":
            result = multiply(a, b)
        else:
            raise ValueError("Unsupported operation")
        
        self.history.append(f"{a} {operation} {b} = {result}")
        return result
"""

    # Generate tests
    generator = ClaudeTestGenerator()
    test_code = await generator.generate_tests("calculator.py")
    print(test_code)

anyio.run(generate_calculator_tests)
```

### Process Multiple Files

```python
import anyio
from claude_test_generator import ClaudeTestGenerator

async def generate_project_tests():
    # Generate tests for all Python files in a project
    generator = ClaudeTestGenerator()
    test_files = await generator.generate_tests_for_directory("my_project/", "tests/")

    for test_file in test_files:
        print(f"Generated: {test_file}")

anyio.run(generate_project_tests)
```

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key (may be required depending on Claude Code CLI setup)

### Supported Testing Frameworks

- pytest (default)
- unittest
- Custom frameworks (specify as parameter)

## Requirements

- Python 3.10+
- Node.js (for Claude Code CLI)
- claude-code-sdk>=0.0.14
- python-dotenv>=1.0.0
- anyio>=3.0.0
- pytest>=8.0.0 (for running tests)
- pytest-asyncio>=1.0.0 (for async test support)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License.
