# Installation Instructions

## Prerequisites

1. **Python 3.10+** 
2. **Node.js** (for Claude Code CLI)
3. **Git** (for cloning the repository)

## Quick Setup

### 1. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Claude Code CLI

```bash
npm install -g @anthropic-ai/claude-code
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment (optional)

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY if needed
```

## Verification

Test that everything is installed correctly:

```bash
# Test Claude Code CLI
claude-code --version

# Test Python imports
python -c "import anyio; print('✓ anyio works')"
python -c "from claude_code_sdk import query; print('✓ claude-code-sdk works')"

# Test the tool
python claude_test_generator.py
```

## Troubleshooting

### Python Version Issues
If you're on Python 3.9 or lower, you may need to upgrade to Python 3.10+:

```bash
# On macOS with Homebrew
brew install python@3.10

# On Ubuntu/Debian
sudo apt update
sudo apt install python3.10
```

### Package Not Found
If `claude-code-sdk` is not available on PyPI yet:

1. Check the GitHub repository for the latest installation instructions
2. Use the fallback anthropic SDK temporarily
3. Install from source: `pip install git+https://github.com/anthropics/claude-code-sdk-python.git`

### Node.js and npm Issues
If you don't have Node.js installed:

```bash
# On macOS with Homebrew
brew install node

# On Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```