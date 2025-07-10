#!/usr/bin/env python3
"""
Claude Test Generator - A demo tool to generate tests for existing Python
projects.
"""

import anyio
from pathlib import Path
from typing import List, Optional
from claude_code_sdk import query, ClaudeCodeOptions
from dotenv import load_dotenv


load_dotenv()


class ClaudeTestGenerator:
    """Demo class for generating tests using Claude Code SDK."""

    def __init__(self, cwd: Optional[str] = None, max_turns: int = 10):
        """
        Initialize the Claude test generator.

        Args:
            cwd: Working directory for Claude Code operations. Defaults to
                current directory.
            max_turns: Maximum number of turns for conversation with Claude.
        """
        self.cwd = Path(cwd) if cwd else Path.cwd()
        self.max_turns = max_turns
        self.options = ClaudeCodeOptions(
            max_turns=self.max_turns,
            cwd=self.cwd,
            allowed_tools=["Read", "Write"],
            permission_mode="acceptEdits"
        )

    def analyze_python_file(self, file_path: str) -> str:
        """Read and return the contents of a Python file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        return path.read_text()

    async def generate_tests(
        self, python_file_path: str, test_framework: str = "pytest"
    ) -> str:
        """
        Generate tests for a Python file using Claude.

        Args:
            python_file_path: Path to the Python file to generate tests for
            test_framework: Testing framework to use (pytest, unittest, etc.)

        Returns:
            Generated test code as a string
        """
        # Create the prompt for Claude
        test_file_name = f"test_{Path(python_file_path).stem}.py"
        prompt = f"""
Please analyze the Python file at {python_file_path} and generate \
comprehensive unit tests using {test_framework}.

Please generate tests that:
1. Cover all functions and methods
2. Test edge cases and error conditions
3. Use appropriate assertions
4. Follow {test_framework} best practices
5. Include proper imports and setup

Create a test file named {test_file_name} with the generated test code.
"""

        # Send request to Claude Code SDK
        messages = []
        async for message in query(prompt=prompt, options=self.options):
            messages.append(message)

        # The test file should have been created by Claude via the Write tool
        # Let's check if it exists and read it
        test_file_path = Path(f"test_{Path(python_file_path).stem}.py")

        if test_file_path.exists():
            test_code = test_file_path.read_text()
            return test_code
        else:
            return ""

    async def generate_tests_for_directory(
        self, directory_path: str, output_dir: str = "tests"
    ) -> List[str]:
        """
        Generate tests for all Python files in a directory.

        Args:
            directory_path: Path to directory containing Python files
            output_dir: Directory to save generated tests

        Returns:
            List of generated test file paths
        """
        directory = Path(directory_path)
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        generated_files = []

        # Find all Python files
        for python_file in directory.glob("**/*.py"):
            # Skip test files and __init__.py
            if (python_file.name.startswith("test_") or
                    python_file.name == "__init__.py"):
                continue

            print(f"Generating tests for: {python_file}")

            try:
                # Generate tests
                test_code = await self.generate_tests(str(python_file))

                # Create output file name
                test_file_name = f"test_{python_file.stem}.py"
                test_file_path = output_path / test_file_name

                # Write test file
                test_file_path.write_text(test_code)
                generated_files.append(str(test_file_path))

                print(f"✓ Generated: {test_file_path}")

            except Exception as e:
                print(f"✗ Error generating tests for {python_file}: {e}")

        return generated_files


async def demo_interactive():
    """Interactive demo function for use in Python REPL."""
    print("Claude Test Generator Demo")
    print("=" * 30)

    try:
        generator = ClaudeTestGenerator()

        # Get file path from user
        file_path = input("Enter path to Python file: ").strip()

        if not file_path:
            print("Using demo example...")
            # Create a simple demo file
            demo_code = '''def add(a, b):
    """Add two numbers."""
    return a + b

def multiply(a, b):
    """Multiply two numbers."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a * b

class Calculator:
    """Simple calculator class."""

    def __init__(self):
        self.history = []

    def calculate(self, operation, a, b):
        """Perform calculation and store in history."""
        if operation == "add":
            result = add(a, b)
        elif operation == "multiply":
            result = multiply(a, b)
        else:
            raise ValueError("Unsupported operation")

        self.history.append(f"{a} {operation} {b} = {result}")
        return result
'''

            # Write demo file
            demo_file = Path("demo_calculator.py")
            demo_file.write_text(demo_code)
            file_path = str(demo_file)
            print(f"Created demo file: {file_path}")

        # Generate tests
        print("\\nGenerating tests...")
        test_code = await generator.generate_tests(file_path)

        # Display results
        print("\\nGenerated Tests:")
        print("=" * 50)
        print(test_code)

        # Save to file
        test_file = Path(f"test_{Path(file_path).stem}.py")
        test_file.write_text(test_code)
        print(f"\\nTests saved to: {test_file}")

    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have installed the Claude Code CLI: "
              "npm install -g @anthropic-ai/claude-code")


if __name__ == "__main__":
    anyio.run(demo_interactive)
