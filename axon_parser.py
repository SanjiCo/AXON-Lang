#!/usr/bin/env python3
"""
AXON Programming Language Parser
"""
import re
import sys

class AxonToken:
    """Token class for AXON language."""
    
    def __init__(self, token_type, value, line_number):
        self.type = token_type
        self.value = value
        self.line_number = line_number
    
    def __str__(self):
        return f"Token({self.type}, '{self.value}', line {self.line_number})"

class AxonParser:
    """Parser for AXON programming language."""
    
    def __init__(self):
        # Token types
        self.TOKEN_TYPES = {
            'KEYWORD': [
                'if', 'while', 'function', 'call', 'print', 'heap', 'stack', 'vmem',
                'paging', 'swap', 'gc', 'thread', 'join', 'threadpool', 'lock', 'unlock',
                'task', 'syscall', 'file', 'mkdir', 'rmdir', 'rtos', 'process', 'scheduler',
                'memory', 'priority', 'after', 'in', 'out', 'alloc', 'free', 'push', 'pop',
                'run', 'start', 'create', 'terminate', 'schedule', 'execute', 'write', 'read',
                'delete', 'copy', 'move'
            ],
            'OPERATOR': ['=', '+', '-', '*', '/', '%', '>', '<', '>=', '<=', '==', '!=', '&&', '||', '!'],
            'DELIMITER': [':', ',', '(', ')', '[', ']', '{', '}'],
            'IDENTIFIER': r'^[a-zA-Z_][a-zA-Z0-9_]*$',
            'NUMBER': r'^[0-9]+(\.[0-9]+)?$',
            'STRING': r'^".*"$',
            'COMMENT': r'^#.*$'
        }
    
    def tokenize(self, code):
        """Convert AXON code into tokens."""
        tokens = []
        lines = code.split('\n')
        
        for line_number, line in enumerate(lines, 1):
            # Skip empty lines
            if not line.strip():
                continue
            
            # Check for comments
            if line.strip().startswith('#'):
                tokens.append(AxonToken('COMMENT', line.strip(), line_number))
                continue
            
            # Calculate indentation
            indent = len(line) - len(line.lstrip())
            if indent > 0:
                tokens.append(AxonToken('INDENT', ' ' * indent, line_number))
            
            # Tokenize the line
            line = line.strip()
            i = 0
            while i < len(line):
                # Skip whitespace
                if line[i].isspace():
                    i += 1
                    continue
                
                # Check for strings
                if line[i] == '"':
                    end = line.find('"', i + 1)
                    if end != -1:
                        tokens.append(AxonToken('STRING', line[i:end+1], line_number))
                        i = end + 1
                        continue
                
                # Check for operators
                for op in sorted(self.TOKEN_TYPES['OPERATOR'], key=len, reverse=True):
                    if line[i:i+len(op)] == op:
                        tokens.append(AxonToken('OPERATOR', op, line_number))
                        i += len(op)
                        break
                else:
                    # Check for delimiters
                    if line[i] in self.TOKEN_TYPES['DELIMITER']:
                        tokens.append(AxonToken('DELIMITER', line[i], line_number))
                        i += 1
                        continue
                    
                    # Check for keywords, identifiers, and numbers
                    word = ''
                    while i < len(line) and not line[i].isspace() and line[i] not in self.TOKEN_TYPES['DELIMITER'] and not any(line[i:i+len(op)] == op for op in self.TOKEN_TYPES['OPERATOR']):
                        word += line[i]
                        i += 1
                    
                    if word:
                        if word in self.TOKEN_TYPES['KEYWORD']:
                            tokens.append(AxonToken('KEYWORD', word, line_number))
                        elif re.match(self.TOKEN_TYPES['NUMBER'], word):
                            tokens.append(AxonToken('NUMBER', word, line_number))
                        elif re.match(self.TOKEN_TYPES['IDENTIFIER'], word):
                            tokens.append(AxonToken('IDENTIFIER', word, line_number))
                        else:
                            tokens.append(AxonToken('UNKNOWN', word, line_number))
            
            tokens.append(AxonToken('NEWLINE', '\n', line_number))
        
        return tokens
    
    def parse(self, tokens):
        """Parse tokens into an abstract syntax tree (AST)."""
        # This is a simplified parser that groups tokens by line
        ast = []
        current_line = []
        
        for token in tokens:
            if token.type == 'NEWLINE':
                if current_line:
                    ast.append(current_line)
                    current_line = []
            else:
                current_line.append(token)
        
        # Add the last line if it exists
        if current_line:
            ast.append(current_line)
        
        return ast
    
    def analyze_syntax(self, ast):
        """Perform syntax analysis on the AST."""
        errors = []
        
        for line_tokens in ast:
            if not line_tokens:
                continue
            
            # Check for basic syntax errors
            line_number = line_tokens[0].line_number
            
            # Check variable assignment syntax
            if any(token.type == 'OPERATOR' and token.value == '=' for token in line_tokens):
                # Should have identifier before '='
                equals_index = next(i for i, token in enumerate(line_tokens) if token.type == 'OPERATOR' and token.value == '=')
                if equals_index == 0 or line_tokens[equals_index-1].type != 'IDENTIFIER':
                    errors.append(f"Line {line_number}: Invalid variable assignment, expected identifier before '='")
                
                # Should have a value after '='
                if equals_index == len(line_tokens) - 1:
                    errors.append(f"Line {line_number}: Invalid variable assignment, expected value after '='")
            
            # Check if statement syntax
            if line_tokens[0].type == 'KEYWORD' and line_tokens[0].value == 'if':
                # Should end with ':'
                if line_tokens[-1].type != 'DELIMITER' or line_tokens[-1].value != ':':
                    errors.append(f"Line {line_number}: If statement should end with ':'")
                
                # Should have a condition
                if len(line_tokens) < 3:
                    errors.append(f"Line {line_number}: If statement missing condition")
            
            # Check while loop syntax
            if line_tokens[0].type == 'KEYWORD' and line_tokens[0].value == 'while':
                # Should end with ':'
                if line_tokens[-1].type != 'DELIMITER' or line_tokens[-1].value != ':':
                    errors.append(f"Line {line_number}: While loop should end with ':'")
                
                # Should have a condition
                if len(line_tokens) < 3:
                    errors.append(f"Line {line_number}: While loop missing condition")
            
            # Check function definition syntax
            if line_tokens[0].type == 'KEYWORD' and line_tokens[0].value == 'function':
                # Should have a name
                if len(line_tokens) < 2 or line_tokens[1].type != 'IDENTIFIER':
                    errors.append(f"Line {line_number}: Function definition missing name")
                
                # Should end with ':'
                if line_tokens[-1].type != 'DELIMITER' or line_tokens[-1].value != ':':
                    errors.append(f"Line {line_number}: Function definition should end with ':'")
            
            # Check function call syntax
            if line_tokens[0].type == 'KEYWORD' and line_tokens[0].value == 'call':
                # Should have a function name
                if len(line_tokens) < 2 or line_tokens[1].type != 'IDENTIFIER':
                    errors.append(f"Line {line_number}: Function call missing function name")
            
            # Check print statement syntax
            if line_tokens[0].type == 'KEYWORD' and line_tokens[0].value == 'print':
                # Should have something to print
                if len(line_tokens) < 2:
                    errors.append(f"Line {line_number}: Print statement missing argument")
        
        return errors
    
    def process_file(self, filename):
        """Process an AXON source file."""
        try:
            with open(filename, 'r') as f:
                code = f.read()
            
            tokens = self.tokenize(code)
            ast = self.parse(tokens)
            errors = self.analyze_syntax(ast)
            
            if errors:
                print("Syntax errors found:")
                for error in errors:
                    print(error)
                return False
            
            return ast
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
            return False
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python axon_parser.py <filename>")
        return
    
    filename = sys.argv[1]
    parser = AxonParser()
    ast = parser.process_file(filename)
    
    if ast:
        print(f"Successfully parsed {filename}")
        print(f"Found {len(ast)} lines of code")

if __name__ == "__main__":
    main() 