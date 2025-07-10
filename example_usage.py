#!/usr/bin/env python3
"""
Example usage of the Claude Test Generator with Claude Code SDK.
"""

import anyio
from pathlib import Path
from claude_test_generator import ClaudeTestGenerator


# Example 1: Generate tests for a single file
async def example_single_file():
    """Example of generating tests for a single Python file."""
    generator = ClaudeTestGenerator()

    # Use the demo_calculator.py file as an example
    file_path = "demo_calculator.py"

    try:
        test_code = await generator.generate_tests(file_path)
        print("Generated test code:")
        print(test_code)

        # Save to file
        test_file = Path(f"test_{Path(file_path).stem}.py")
        test_file.write_text(test_code)
        print(f"Tests saved to: {test_file}")

    except Exception as e:
        print(f"Error: {e}")


# Example 2: Generate tests for an entire directory
async def example_directory():
    """Example of generating tests for all Python files in a directory."""
    generator = ClaudeTestGenerator()

    # Create a temporary directory with Python files for demonstration
    test_dir = Path("example_project")
    test_dir.mkdir(exist_ok=True)

    # Create a sample Python file
    sample_file = test_dir / "utils.py"
    sample_code = '''def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"

def calculate_area(length, width):
    """Calculate the area of a rectangle."""
    if length <= 0 or width <= 0:
        raise ValueError("Dimensions must be positive")
    return length * width
'''
    sample_file.write_text(sample_code)

    try:
        generated_files = await generator.generate_tests_for_directory(
            str(test_dir))
        print(f"Generated {len(generated_files)} test files:")
        for file_path in generated_files:
            print(f"  - {file_path}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        import shutil
        shutil.rmtree(test_dir, ignore_errors=True)


# Example 3: Interactive REPL usage
def repl_example():
    """
    Example of how to use this in a Python REPL.

    In your Python REPL, run:

    >>> import anyio
    >>> from claude_test_generator import ClaudeTestGenerator
    >>> generator = ClaudeTestGenerator()
    >>>
    >>> # Generate tests for a specific file (async)
    >>> async def test_generation():
    ...     test_code = await generator.generate_tests("my_module.py")
    ...     print(test_code)
    >>>
    >>> anyio.run(test_generation)
    >>>
    >>> # Or run the interactive demo
    >>> from claude_test_generator import demo_interactive
    >>> anyio.run(demo_interactive)
    """
    pass


# Example 4: Custom configuration
async def example_custom_config():
    """Example with custom configuration options."""
    generator = ClaudeTestGenerator(
        cwd=Path.cwd(),  # Use current directory
        max_turns=15     # Increase turns for complex projects
    )

    try:
        test_code = await generator.generate_tests(
            "demo_calculator.py", test_framework="unittest")
        print("Generated unittest code:")
        preview = (test_code[:500] + "..." if len(test_code) > 500
                   else test_code)
        print(preview)
    except Exception as e:
        print(f"Error: {e}")


# Example 5: Working with existing files
async def example_existing_files():
    """Example using the actual files in this project."""
    generator = ClaudeTestGenerator()

    # Generate tests for the main module
    try:
        print("Generating tests for claude_test_generator.py...")
        test_code = await generator.generate_tests("claude_test_generator.py")

        # Save with a different name to avoid overwriting existing tests
        test_file = Path("test_claude_test_generator_example.py")
        test_file.write_text(test_code)
        print(f"Tests saved to: {test_file}")

        # Show first few lines
        lines = test_code.split('\n')
        print("First 10 lines of generated tests:")
        for i, line in enumerate(lines[:10]):
            print(f"  {i+1:2d}: {line}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up the example test file
        example_file = Path("test_claude_test_generator_example.py")
        if example_file.exists():
            example_file.unlink()


async def main():
    """Run all examples."""
    print("=" * 60)
    print("Claude Test Generator - Example Usage")
    print("=" * 60)

    print("\nExample 1: Single file test generation")
    print("-" * 40)
    await example_single_file()

    print("\nExample 2: Directory test generation")
    print("-" * 40)
    await example_directory()

    print("\nExample 4: Custom configuration")
    print("-" * 40)
    await example_custom_config()

    print("\nExample 5: Working with existing files")
    print("-" * 40)
    await example_existing_files()


if __name__ == "__main__":
    print("Claude Test Generator - Example Usage")
    print("=" * 60)
    print("This file demonstrates various ways to use the Claude Test "
          "Generator.")
    print("You can run individual functions or all examples at once.")
    print("\nTo run all examples:")
    print("  python example_usage.py")
    print("\nTo run the interactive demo:")
    print("  python claude_test_generator.py")
    print("\nTo run individual examples in Python REPL:")
    print("  >>> import anyio")
    print("  >>> from example_usage import example_single_file")
    print("  >>> anyio.run(example_single_file)")
    print("\nRunning all examples now...")
    print("=" * 60)
    anyio.run(main)
