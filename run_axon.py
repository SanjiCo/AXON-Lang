#!/usr/bin/env python3
"""
AXON Programming Language Runner
Integrates the parser and interpreter to run AXON programs
"""
import sys
import os
from axon import AxonInterpreter

def print_banner():
    """Print AXON language banner."""
    banner = """
    █████╗ ██╗  ██╗ ██████╗ ███╗   ██╗
   ██╔══██╗╚██╗██╔╝██╔═══██╗████╗  ██║
   ███████║ ╚███╔╝ ██║   ██║██╔██╗ ██║
   ██╔══██║ ██╔██╗ ██║   ██║██║╚██╗██║
   ██║  ██║██╔╝ ██╗╚██████╔╝██║ ╚████║
   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                      
   Programming Language v1.0
   """
    print(banner)

def run_file(filename):
    """Run an AXON file."""
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return
    
    with open(filename, 'r') as f:
        code = f.read()
    
    interpreter = AxonInterpreter()
    
    # Split the code into lines and execute each line
    lines = code.split('\n')
    line_number = 0
    
    try:
        while line_number < len(lines):
            line = lines[line_number]
            line_number += 1
            
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith('#'):
                continue
            
            # Execute the line
            interpreter.current_line = line_number
            result = interpreter.parse_line(line)
            
            # Handle control flow
            if isinstance(result, dict) and 'jump' in result:
                line_number = result['jump']
    except Exception as e:
        print(f"Error at line {line_number}: {e}")
        if interpreter.debug_mode:
            interpreter._debug_pause(lines[line_number-1] if line_number-1 < len(lines) else "")

def run_interactive():
    """Run AXON in interactive mode."""
    interpreter = AxonInterpreter()
    
    print("AXON Interactive Mode")
    print("Type 'exit' to quit")
    
    while True:
        try:
            line = input("axon> ")
            
            if line.lower() == 'exit':
                break
            
            # Skip empty lines
            if not line.strip():
                continue
            
            # Execute the line
            interpreter.current_line = 0
            result = interpreter.parse_line(line)
            
            if result is not None:
                print(result)
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main function."""
    if len(sys.argv) > 1:
        # Run a file
        run_file(sys.argv[1])
    else:
        # Run in interactive mode
        run_interactive()

if __name__ == "__main__":
    main() 