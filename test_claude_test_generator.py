import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from pathlib import Path
import anyio
from claude_test_generator import ClaudeTestGenerator, demo_interactive


class TestClaudeTestGenerator:
    
    def test_init_with_default_cwd(self):
        generator = ClaudeTestGenerator()
        assert generator.cwd == Path.cwd()
        assert generator.max_turns == 3
        assert generator.options.max_turns == 3
        assert generator.options.cwd == Path.cwd()
        assert generator.options.allowed_tools == ["Read", "Write", "Bash"]
        assert generator.options.permission_mode == "acceptEdits"

    def test_init_with_custom_cwd(self):
        custom_cwd = "/tmp/test"
        generator = ClaudeTestGenerator(cwd=custom_cwd)
        assert generator.cwd == Path(custom_cwd)
        assert generator.max_turns == 3

    def test_init_with_custom_max_turns(self):
        generator = ClaudeTestGenerator(max_turns=5)
        assert generator.max_turns == 5
        assert generator.options.max_turns == 5

    def test_init_with_both_params(self):
        custom_cwd = "/tmp/test"
        max_turns = 10
        generator = ClaudeTestGenerator(cwd=custom_cwd, max_turns=max_turns)
        assert generator.cwd == Path(custom_cwd)
        assert generator.max_turns == max_turns

    def test_analyze_python_file_exists(self, tmp_path):
        test_file = tmp_path / "test.py"
        test_content = "def test_function():\n    pass\n"
        test_file.write_text(test_content)
        
        generator = ClaudeTestGenerator()
        result = generator.analyze_python_file(str(test_file))
        assert result == test_content

    def test_analyze_python_file_not_exists(self):
        generator = ClaudeTestGenerator()
        with pytest.raises(FileNotFoundError, match="File not found: nonexistent.py"):
            generator.analyze_python_file("nonexistent.py")

    @pytest.mark.asyncio
    async def test_generate_tests_basic(self):
        generator = ClaudeTestGenerator()
        
        mock_message = Mock()
        mock_content = Mock()
        mock_content.text = "import pytest\ndef test_example():\n    assert True"
        mock_message.content = [mock_content]
        
        with patch('claude_test_generator.query') as mock_query:
            mock_query.return_value = [mock_message]
            
            result = await generator.generate_tests("test.py")
            
            assert "import pytest" in result
            assert "def test_example():" in result
            mock_query.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_tests_with_code_blocks(self):
        generator = ClaudeTestGenerator()
        
        mock_message = Mock()
        mock_content = Mock()
        mock_content.text = "```python\nimport pytest\ndef test_example():\n    assert True\n```"
        mock_message.content = [mock_content]
        
        with patch('claude_test_generator.query') as mock_query:
            mock_query.return_value = [mock_message]
            
            result = await generator.generate_tests("test.py")
            
            assert "import pytest" in result
            assert "def test_example():" in result
            assert "```" not in result

    @pytest.mark.asyncio
    async def test_generate_tests_custom_framework(self):
        generator = ClaudeTestGenerator()
        
        mock_message = Mock()
        mock_content = Mock()
        mock_content.text = "import unittest\nclass TestExample(unittest.TestCase):\n    def test_method(self):\n        self.assertTrue(True)"
        mock_message.content = [mock_content]
        
        with patch('claude_test_generator.query') as mock_query:
            mock_query.return_value = [mock_message]
            
            result = await generator.generate_tests("test.py", test_framework="unittest")
            
            assert "import unittest" in result
            mock_query.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_tests_no_content(self):
        generator = ClaudeTestGenerator()
        
        mock_message = Mock()
        mock_message.content = []
        
        with patch('claude_test_generator.query') as mock_query:
            mock_query.return_value = [mock_message]
            
            result = await generator.generate_tests("test.py")
            
            assert result == ""

    @pytest.mark.asyncio
    async def test_generate_tests_no_text_attribute(self):
        generator = ClaudeTestGenerator()
        
        mock_message = Mock()
        mock_content = Mock()
        del mock_content.text
        mock_message.content = [mock_content]
        
        with patch('claude_test_generator.query') as mock_query:
            mock_query.return_value = [mock_message]
            
            result = await generator.generate_tests("test.py")
            
            assert result == ""

    @pytest.mark.asyncio
    async def test_generate_tests_for_directory_basic(self, tmp_path):
        # Create test directory structure
        test_dir = tmp_path / "src"
        test_dir.mkdir()
        
        # Create Python files
        file1 = test_dir / "module1.py"
        file1.write_text("def function1():\n    pass")
        
        file2 = test_dir / "module2.py"
        file2.write_text("def function2():\n    pass")
        
        # Create files to ignore
        test_file = test_dir / "test_existing.py"
        test_file.write_text("def test_something():\n    pass")
        
        init_file = test_dir / "__init__.py"
        init_file.write_text("")
        
        generator = ClaudeTestGenerator()
        
        mock_message = Mock()
        mock_content = Mock()
        mock_content.text = "import pytest\ndef test_generated():\n    assert True"
        mock_message.content = [mock_content]
        
        with patch('claude_test_generator.query') as mock_query:
            mock_query.return_value = [mock_message]
            
            result = await generator.generate_tests_for_directory(str(test_dir))
            
            assert len(result) == 2
            assert str(tmp_path / "tests" / "test_module1.py") in result
            assert str(tmp_path / "tests" / "test_module2.py") in result

    @pytest.mark.asyncio
    async def test_generate_tests_for_directory_custom_output(self, tmp_path):
        test_dir = tmp_path / "src"
        test_dir.mkdir()
        
        file1 = test_dir / "module1.py"
        file1.write_text("def function1():\n    pass")
        
        generator = ClaudeTestGenerator()
        
        mock_message = Mock()
        mock_content = Mock()
        mock_content.text = "import pytest\ndef test_generated():\n    assert True"
        mock_message.content = [mock_content]
        
        with patch('claude_test_generator.query') as mock_query:
            mock_query.return_value = [mock_message]
            
            result = await generator.generate_tests_for_directory(str(test_dir), "custom_tests")
            
            assert len(result) == 1
            assert str(tmp_path / "custom_tests" / "test_module1.py") in result

    @pytest.mark.asyncio
    async def test_generate_tests_for_directory_not_exists(self):
        generator = ClaudeTestGenerator()
        
        with pytest.raises(FileNotFoundError, match="Directory not found: nonexistent"):
            await generator.generate_tests_for_directory("nonexistent")

    @pytest.mark.asyncio
    async def test_generate_tests_for_directory_with_error(self, tmp_path, capsys):
        test_dir = tmp_path / "src"
        test_dir.mkdir()
        
        file1 = test_dir / "module1.py"
        file1.write_text("def function1():\n    pass")
        
        generator = ClaudeTestGenerator()
        
        with patch('claude_test_generator.query') as mock_query:
            mock_query.side_effect = Exception("Test error")
            
            result = await generator.generate_tests_for_directory(str(test_dir))
            
            assert result == []
            captured = capsys.readouterr()
            assert "Error generating tests for" in captured.out
            assert "Test error" in captured.out

    @pytest.mark.asyncio
    async def test_generate_tests_for_directory_nested(self, tmp_path):
        # Create nested directory structure
        test_dir = tmp_path / "src"
        test_dir.mkdir()
        
        sub_dir = test_dir / "sub"
        sub_dir.mkdir()
        
        file1 = test_dir / "module1.py"
        file1.write_text("def function1():\n    pass")
        
        file2 = sub_dir / "module2.py"
        file2.write_text("def function2():\n    pass")
        
        generator = ClaudeTestGenerator()
        
        mock_message = Mock()
        mock_content = Mock()
        mock_content.text = "import pytest\ndef test_generated():\n    assert True"
        mock_message.content = [mock_content]
        
        with patch('claude_test_generator.query') as mock_query:
            mock_query.return_value = [mock_message]
            
            result = await generator.generate_tests_for_directory(str(test_dir))
            
            assert len(result) == 2
            assert any("test_module1.py" in path for path in result)
            assert any("test_module2.py" in path for path in result)


@pytest.mark.asyncio
async def test_demo_interactive_with_file_input(tmp_path):
    test_file = tmp_path / "test_module.py"
    test_file.write_text("def test_function():\n    pass")
    
    mock_message = Mock()
    mock_content = Mock()
    mock_content.text = "import pytest\ndef test_generated():\n    assert True"
    mock_message.content = [mock_content]
    
    with patch('builtins.input', return_value=str(test_file)), \
         patch('claude_test_generator.query') as mock_query, \
         patch('builtins.print') as mock_print:
        
        mock_query.return_value = [mock_message]
        
        await demo_interactive()
        
        mock_query.assert_called_once()
        mock_print.assert_called()

@pytest.mark.asyncio
async def test_demo_interactive_with_empty_input(tmp_path):
    mock_message = Mock()
    mock_content = Mock()
    mock_content.text = "import pytest\ndef test_generated():\n    assert True"
    mock_message.content = [mock_content]
    
    with patch('builtins.input', return_value=""), \
         patch('claude_test_generator.query') as mock_query, \
         patch('builtins.print') as mock_print:
        
        mock_query.return_value = [mock_message]
        
        await demo_interactive()
        
        mock_query.assert_called_once()
        mock_print.assert_called()

@pytest.mark.asyncio
async def test_demo_interactive_with_exception():
    with patch('builtins.input', return_value="test.py"), \
         patch('claude_test_generator.ClaudeTestGenerator') as mock_generator, \
         patch('builtins.print') as mock_print:
        
        mock_generator.side_effect = Exception("Test error")
        
        await demo_interactive()
        
        mock_print.assert_called()
        print_calls = [call.args[0] for call in mock_print.call_args_list]
        assert any("Error: Test error" in call for call in print_calls)

def test_main_execution():
    with patch('claude_test_generator.anyio.run') as mock_run:
        import claude_test_generator
        exec(open('claude_test_generator.py').read())
        mock_run.assert_called_once_with(demo_interactive)