# AXON Programming Language Installation Guide

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation Methods

### Method 1: Install from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/axon-lang/axon.git
   cd axon
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

3. Verify the installation:
   ```bash
   axon --version
   ```

### Method 2: Manual Setup

1. Download the source code or clone the repository.

2. Make sure all the files are in the same directory:
   - `axon.py`
   - `axon_parser.py`
   - `run_axon.py`

3. Run AXON programs using:
   ```bash
   python run_axon.py your_program.axon
   ```

## Directory Structure

After installation, your AXON setup should have the following structure:

```
axon/
├── axon.py              # Main interpreter
├── axon_parser.py       # Parser for AXON language
├── run_axon.py          # Runner script
├── setup.py             # Installation script
├── requirements.txt     # Dependencies
├── README.md            # Overview documentation
├── INSTALL.md           # This installation guide
├── docs/                # Documentation
│   └── AXON_LANGUAGE_REFERENCE.md  # Language reference
└── examples/            # Example AXON programs
    ├── hello_world.axon
    ├── memory_threading.axon
    ├── rtos_kernel.axon
    └── advanced_system.axon
```

## Running AXON Programs

### Command Line

Run an AXON program:
```bash
axon your_program.axon
```

Run with debug mode:
```bash
axon your_program.axon -d
```

### Interactive Mode

Start the interactive AXON shell:
```bash
axon
```

In interactive mode, you can:
- Execute AXON commands directly
- Load and run AXON programs
- Get help with the `help` command
- Exit with the `exit` command

## Troubleshooting

### Common Issues

1. **Command not found**: If the `axon` command is not found, make sure the installation was successful and the Python scripts directory is in your PATH.

2. **Import errors**: If you see import errors, make sure all required files are in the same directory or properly installed.

3. **Permission issues**: If you encounter permission errors when running AXON, try running with elevated privileges or check file permissions.

### Getting Help

If you encounter any issues with installation or running AXON programs, please:

1. Check the documentation in the `docs/` directory
2. Look for similar issues in the GitHub repository
3. Open a new issue on GitHub if your problem persists

## Uninstallation

To uninstall AXON:

```bash
pip uninstall axon-lang
``` 