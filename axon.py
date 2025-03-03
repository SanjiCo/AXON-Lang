#!/usr/bin/env python3
"""
AXON Programming Language Interpreter
"""
import sys
import os
import re
import time
import threading
import queue
from collections import deque
import json
import random
import datetime

# Import the standard library
try:
    from axon_stdlib import AxonStdLib
except ImportError:
    # Create a dummy class if the standard library is not found
    class AxonStdLib:
        def __init__(self, interpreter):
            self.interpreter = interpreter
            self.functions = {}

class AxonInterpreter:
    def __init__(self):
        """Initialize the AXON interpreter."""
        # Variable storage
        self.variables = {}
        
        # Memory management
        self.heap = {}
        self.stack = []
        self.virtual_memory = {}
        self.memory_counter = 0
        
        # Threading
        self.threads = {}
        self.current_thread = "main"
        
        # Task scheduling
        self.tasks = []
        self.current_task = None
        
        # Process management
        self.processes = {}
        self.current_process = "main"
        
        # Object-oriented programming
        self.classes = {}
        self.objects = {}
        
        # Debugging
        self.debug_mode = False
        self.breakpoints = set()
        self.step_by_step = False
        self.current_line = 0
        self.call_stack = []
        
        # Standard library
        try:
            from axon_stdlib import AxonStdLib
            self.stdlib = AxonStdLib(self)
            self.stdlib_functions = self.stdlib.functions
        except ImportError:
            # Create a dummy class if the standard library is not found
            class DummyStdLib:
                def __init__(self):
                    self.functions = {}
            self.stdlib = DummyStdLib()
            self.stdlib_functions = {}
        
        # Command handlers
        self.command_handlers = {
            'variable_assignment': self._handle_variable_assignment,
            'print': self._handle_print,
            'if': self._handle_if,
            'while': self._handle_while,
            'function': self._handle_function,
            'call': self._handle_function_call,
            'return': self._handle_return,
            'heap': self._handle_heap,
            'stack': self._handle_stack,
            'memory': self._handle_memory,
            'thread': self._handle_thread,
            'task': self._handle_task,
            'process': self._handle_process,
            'debug': self._handle_debug,
            'breakpoint': self._handle_breakpoint,
            'class': self._handle_class,
            'object': self._handle_object,
            'import': self._handle_import,
            'export': self._handle_export,
            'try': self._handle_try,
            'catch': self._handle_catch,
            'finally': self._handle_finally,
            'throw': self._handle_throw,
        }
    
    def parse_line(self, line):
        """Parse a line of AXON code and execute the corresponding command."""
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            return
        
        # Check indentation
        indent = len(line) - len(line.lstrip())
        self.indent_level = indent // 4
        
        line = line.strip()
        
        # Debug mode: check for breakpoints and step-by-step execution
        if self.debug_mode:
            if self.current_line in self.breakpoints or self.step_by_step:
                self._debug_pause(line)
        
        # Handle return statement
        if line.startswith('return'):
            return_value = line[6:].strip()
            
            if self.debug_mode:
                print(f"DEBUG: Return value: {return_value}")
                
            if self.call_stack:
                self.call_stack.pop()
                
            return return_value
        
        # Variable assignment
        if '=' in line and not line.startswith(('if', 'while')):
            result = self._handle_variable_assignment(line)
            return result
        
        # Handle method calls (object.method())
        if '.' in line and '(' in line and ')' in line:
            # Check if it's a standard library call
            if any(line.startswith(prefix) for prefix in ['math.', 'string.', 'time.', 'system.', 'file.', 'json.', 'random.']):
                result = self._handle_stdlib_call(line)
                return result
            else:
                result = self._handle_method_call(line)
                return result
        
        # Handle print statements
        if line.startswith('print'):
            result = self._handle_print(line)
            return result
        
        # Handle commands
        for cmd in self.command_handlers:
            if line.startswith(cmd):
                result = self.command_handlers[cmd](line)
                return result
        
        # Handle if statements
        if line.startswith('if'):
            result = self.command_handlers['if'](line)
            return result
        
        # Handle while loops
        if line.startswith('while'):
            result = self.command_handlers['while'](line)
            return result
        
        # Handle function definitions
        if line.startswith('function'):
            result = self.command_handlers['function'](line)
            return result
        
        print(f"Error: Unknown command: {line}")
        return None
    
    def _handle_variable_assignment(self, line):
        """Handle variable assignment."""
        # Split the line by the first '=' character
        parts = line.split('=', 1)
        
        if len(parts) != 2:
            print(f"Error: Invalid variable assignment: {line}")
            return None
        
        var_name = parts[0].strip()
        value = parts[1].strip()
        
        # Check if value is a string literal
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            self.variables[var_name] = value[1:-1]
        # Check if value is a standard library call
        elif '.' in value and '(' in value and ')' in value:
            # Handle standard library call
            result = self._handle_stdlib_call(value)
            self.variables[var_name] = result
        # Otherwise, try to evaluate the expression
        else:
            try:
                # Check if value is a variable
                if value in self.variables:
                    self.variables[var_name] = self.variables[value]
                else:
                    # Evaluate the expression using the variables dictionary
                    self.variables[var_name] = eval(value, {"__builtins__": {}}, self.variables)
            except:
                # If evaluation fails, store the value as is
                self.variables[var_name] = value
        
        return None
    
    def _handle_if(self, line):
        """Handle if statements."""
        condition = line[2:].strip()
        if condition.endswith(':'):
            condition = condition[:-1].strip()
        
        # Evaluate the condition
        result = self._evaluate_condition(condition)
        print(f"If condition '{condition}' evaluated to {result}")
    
    def _handle_while(self, line):
        """Handle while loops."""
        condition = line[5:].strip()
        if condition.endswith(':'):
            condition = condition[:-1].strip()
        
        # Evaluate the condition
        result = self._evaluate_condition(condition)
        print(f"While condition '{condition}' evaluated to {result}")
    
    def _handle_function(self, line):
        """Handle function definitions."""
        # Extract function name and parameters
        match = re.match(r'function\s+(\w+)\s*\((.*?)\)', line)
        if not match:
            print(f"Error: Invalid function definition: {line}")
            return None
        
        function_name = match.group(1)
        params_str = match.group(2)
        
        # Parse parameters
        params = []
        if params_str:
            params = [param.strip() for param in params_str.split(',')]
        
        # Store function definition
        self.variables[function_name] = {
            'type': 'function',
            'params': params,
            'body': []
        }
        
        return None
    
    def _handle_function_call(self, line):
        """Handle function calls."""
        # Extract function name and arguments
        match = re.match(r'call\s+(\w+)\s*\((.*?)\)', line)
        if not match:
            print(f"Error: Invalid function call: {line}")
            return None
        
        function_name = match.group(1)
        args_str = match.group(2)
        
        # Check if function exists
        if function_name not in self.variables or self.variables[function_name]['type'] != 'function':
            print(f"Error: Function '{function_name}' not defined")
            return None
        
        # Parse arguments
        args = []
        if args_str:
            args = [arg.strip() for arg in args_str.split(',')]
        
        # Get function definition
        function = self.variables[function_name]
        
        # Check if number of arguments matches number of parameters
        if len(args) != len(function['params']):
            print(f"Error: Function '{function_name}' expects {len(function['params'])} arguments, but got {len(args)}")
            return None
        
        # Create a new scope for function execution
        old_variables = self.variables.copy()
        
        # Add function parameters to scope
        for i, param in enumerate(function['params']):
            # Evaluate argument
            if args[i] in self.variables:
                self.variables[param] = self.variables[args[i]]
            else:
                try:
                    self.variables[param] = eval(args[i], {"__builtins__": {}}, self.variables)
                except:
                    self.variables[param] = args[i]
        
        # Add function to call stack
        self.call_stack.append(function_name)
        
        # Execute function body
        result = None
        for line in function['body']:
            result = self.parse_line(line)
            if result is not None:
                break
        
        # Restore old scope
        self.variables = old_variables
        
        # Remove function from call stack
        self.call_stack.pop()
        
        return result
    
    def _handle_return(self, line):
        """Handle return statements."""
        # Extract return value
        return_value = line[6:].strip()
        
        # Evaluate return value
        if return_value in self.variables:
            return self.variables[return_value]
        else:
            try:
                return eval(return_value, {"__builtins__": {}}, self.variables)
            except:
                return return_value
    
    def _handle_print(self, line):
        """Handle print statements."""
        # Extract the content to print
        content = line[5:].strip()
        
        # Check if content is empty
        if not content:
            print()
            return None
        
        # Check if content is in quotes
        if (content.startswith('"') and content.endswith('"')) or (content.startswith("'") and content.endswith("'")):
            # Print the string literal
            print(content[1:-1])
            return None
        
        # Check if content contains variables or expressions
        result = []
        parts = content.split(',')
        
        for part in parts:
            part = part.strip()
            
            # Check if part is a string literal
            if (part.startswith('"') and part.endswith('"')) or (part.startswith("'") and part.endswith("'")):
                result.append(part[1:-1])
            # Check if part is a variable
            elif part in self.variables:
                result.append(str(self.variables[part]))
            # Check if part is a standard library call
            elif '.' in part and '(' in part and ')' in part:
                # Handle standard library call
                stdlib_result = self._handle_stdlib_call(part)
                result.append(str(stdlib_result))
            # Otherwise, try to evaluate the expression
            else:
                try:
                    # Evaluate the expression using the variables dictionary
                    value = eval(part, {"__builtins__": {}}, self.variables)
                    result.append(str(value))
                except:
                    result.append(part)
        
        # Print the result
        print(' '.join(result))
        return None
    
    def _handle_heap(self, line):
        """Handle heap memory operations."""
        parts = line.split()
        operation = parts[1]
        
        if operation == 'alloc':
            name = parts[2]
            size = int(parts[3])
            self.heap[name] = {'size': size, 'data': [0] * size}
            print(f"Allocated {size} bytes in heap for '{name}'")
        elif operation == 'free':
            name = parts[2]
            if name in self.heap:
                del self.heap[name]
                print(f"Freed heap memory for '{name}'")
            else:
                print(f"Error: Heap memory '{name}' not found")
    
    def _handle_stack(self, line):
        """Handle stack operations."""
        parts = line.split()
        operation = parts[1]
        
        if operation == 'push':
            value = parts[2]
            self.stack.append(value)
            print(f"Pushed '{value}' onto the stack")
        elif operation == 'pop':
            if self.stack:
                value = self.stack.pop()
                print(f"Popped '{value}' from the stack")
            else:
                print("Error: Stack is empty")
    
    def _handle_vmem(self, line):
        """Handle virtual memory operations."""
        parts = line.split()
        operation = parts[1]
        
        if operation == 'alloc':
            name = parts[2]
            size = int(parts[3])
            self.virtual_memory[name] = {'size': size, 'data': [0] * size}
            print(f"Allocated {size} bytes in virtual memory for '{name}'")
        elif operation == 'free':
            name = parts[2]
            if name in self.virtual_memory:
                del self.virtual_memory[name]
                print(f"Freed virtual memory for '{name}'")
            else:
                print(f"Error: Virtual memory '{name}' not found")
    
    def _handle_paging(self, line):
        """Handle memory paging operations."""
        parts = line.split()
        operation = parts[1]
        
        if operation == 'alloc':
            page_id = parts[2]
            size = int(parts[3])
            self.pages[page_id] = {'size': size, 'data': [0] * size}
            print(f"Allocated page '{page_id}' with size {size}")
        elif operation == 'free':
            page_id = parts[2]
            if page_id in self.pages:
                del self.pages[page_id]
                print(f"Freed page '{page_id}'")
            else:
                print(f"Error: Page '{page_id}' not found")
    
    def _handle_swap(self, line):
        """Handle swap operations."""
        parts = line.split()
        operation = parts[1]
        page_id = parts[2]
        
        if operation == 'out':
            if page_id in self.pages:
                self.swap_area[page_id] = self.pages[page_id]
                del self.pages[page_id]
                print(f"Swapped out page '{page_id}' to swap area")
            else:
                print(f"Error: Page '{page_id}' not found")
        elif operation == 'in':
            if page_id in self.swap_area:
                self.pages[page_id] = self.swap_area[page_id]
                del self.swap_area[page_id]
                print(f"Swapped in page '{page_id}' from swap area")
            else:
                print(f"Error: Page '{page_id}' not found in swap area")
    
    def _handle_gc(self, line):
        """Handle garbage collection."""
        parts = line.split()
        operation = parts[1]
        
        if operation == 'run':
            print("Running garbage collection...")
            # Simulate garbage collection
            print("Garbage collection completed")
    
    def _handle_thread(self, line):
        """Handle thread operations."""
        parts = line.split(':')
        thread_name = parts[0].split()[1].strip()
        
        self.threads[thread_name] = True
        print(f"Created thread '{thread_name}'")
    
    def _handle_join(self, line):
        """Handle thread join operations."""
        parts = line.split()
        thread_name = parts[1]
        
        if thread_name in self.threads:
            print(f"Joined thread '{thread_name}'")
        else:
            print(f"Error: Thread '{thread_name}' not found")
    
    def _handle_threadpool(self, line):
        """Handle thread pool operations."""
        parts = line.split()
        operation = parts[1]
        
        if operation == 'start':
            print("Started thread pool")
        elif operation == 'join':
            print("Joined all threads in thread pool")
    
    def _handle_lock(self, line):
        """Handle lock operations."""
        parts = line.split()
        lock_name = parts[1]
        
        self.locks[lock_name] = True
        print(f"Acquired lock '{lock_name}'")
    
    def _handle_unlock(self, line):
        """Handle unlock operations."""
        parts = line.split()
        lock_name = parts[1]
        
        if lock_name in self.locks:
            del self.locks[lock_name]
            print(f"Released lock '{lock_name}'")
        else:
            print(f"Error: Lock '{lock_name}' not found")
    
    def _handle_task(self, line):
        """Handle task operations."""
        parts = line.split()
        
        if len(parts) >= 2:
            if parts[1] == 'start':
                print("Started scheduled tasks")
                return
            
            task_name = parts[1]
            
            if 'after' in line:
                after_index = line.find('after')
                time_str = line[after_index:].split()[1]
                seconds = int(time_str.replace('s', ''))
                
                priority = 0
                if 'priority' in line:
                    priority_index = line.find('priority')
                    priority = int(line[priority_index:].split()[1])
                
                self.tasks[task_name] = {'priority': priority, 'delay': seconds}
                print(f"Scheduled task '{task_name}' with priority {priority} to run after {seconds} seconds")
    
    def _handle_syscall(self, line):
        """Handle system call operations."""
        command = line[8:].strip()
        if command.startswith('"') and command.endswith('"'):
            command = command[1:-1]
        
        print(f"Executing system call: {command}")
    
    def _handle_file(self, line):
        """Handle file operations."""
        parts = line.split()
        operation = parts[1]
        
        if operation == 'write':
            filename = parts[2]
            content_start = line.find('"')
            content_end = line.rfind('"')
            
            if content_start != -1 and content_end != -1:
                content = line[content_start+1:content_end]
                print(f"Writing to file '{filename}': {content}")
            else:
                print(f"Writing to file '{filename}'")
        
        elif operation == 'read':
            filename = parts[2]
            print(f"Reading from file '{filename}'")
        
        elif operation == 'delete':
            filename = parts[2]
            print(f"Deleting file '{filename}'")
        
        elif operation == 'copy':
            source = parts[2]
            destination = parts[3]
            print(f"Copying file from '{source}' to '{destination}'")
        
        elif operation == 'move':
            source = parts[2]
            destination = parts[3]
            print(f"Moving file from '{source}' to '{destination}'")
    
    def _handle_mkdir(self, line):
        """Handle directory creation."""
        parts = line.split()
        directory_name = parts[1]
        print(f"Creating directory '{directory_name}'")
    
    def _handle_rmdir(self, line):
        """Handle directory removal."""
        parts = line.split()
        directory_name = parts[1]
        print(f"Removing directory '{directory_name}'")
    
    def _handle_rtos(self, line):
        """Handle RTOS operations."""
        parts = line.split()
        operation = parts[1]
        
        if operation == 'schedule':
            task = parts[2]
            priority = int(parts[4])
            print(f"Scheduled RTOS task '{task}' with priority {priority}")
        
        elif operation == 'execute':
            print("Executing RTOS tasks")
    
    def _handle_process(self, line):
        """Handle process operations."""
        parts = line.split()
        operation = parts[1]
        
        if operation == 'create':
            process_name = parts[2]
            priority = int(parts[3])
            self.processes[process_name] = {'priority': priority}
            print(f"Created process '{process_name}' with priority {priority}")
        
        elif operation == 'terminate':
            process_name = parts[2]
            if process_name in self.processes:
                del self.processes[process_name]
                print(f"Terminated process '{process_name}'")
            else:
                print(f"Error: Process '{process_name}' not found")
    
    def _handle_scheduler(self, line):
        """Handle scheduler operations."""
        parts = line.split()
        operation = parts[1]
        
        if operation == 'run':
            print("Running scheduler")
    
    def _handle_memory(self, line):
        """Handle memory operations."""
        # Extract operation and arguments
        parts = line.split()
        if len(parts) < 2:
            print(f"Error: Invalid memory operation: {line}")
            return None
        
        operation = parts[1]
        
        if operation == 'allocate':
            # Allocate memory
            if len(parts) < 4:
                print(f"Error: Invalid memory allocate operation: {line}")
                return None
            
            var_name = parts[2]
            size = parts[3]
            
            # Evaluate size
            if size in self.variables:
                size = self.variables[size]
            else:
                try:
                    size = eval(size, {"__builtins__": {}}, self.variables)
                except:
                    pass
            
            # Convert size to integer
            try:
                size = int(size)
            except:
                print(f"Error: Invalid memory size: {size}")
                return None
            
            # Allocate memory
            self.memory_counter += 1
            self.heap[self.memory_counter] = [None] * size
            self.variables[var_name] = {
                'type': 'memory',
                'id': self.memory_counter,
                'size': size
            }
            
            return None
        
        elif operation == 'free':
            # Free memory
            if len(parts) < 3:
                print(f"Error: Invalid memory free operation: {line}")
                return None
            
            var_name = parts[2]
            
            # Check if variable exists
            if var_name not in self.variables or self.variables[var_name]['type'] != 'memory':
                print(f"Error: Variable '{var_name}' is not a memory block")
                return None
            
            # Free memory
            memory_id = self.variables[var_name]['id']
            del self.heap[memory_id]
            del self.variables[var_name]
            
            return None
        
        elif operation == 'read':
            # Read from memory
            if len(parts) < 4:
                print(f"Error: Invalid memory read operation: {line}")
                return None
            
            var_name = parts[2]
            index = parts[3]
            
            # Check if variable exists
            if var_name not in self.variables or self.variables[var_name]['type'] != 'memory':
                print(f"Error: Variable '{var_name}' is not a memory block")
                return None
            
            # Evaluate index
            if index in self.variables:
                index = self.variables[index]
            else:
                try:
                    index = eval(index, {"__builtins__": {}}, self.variables)
                except:
                    pass
            
            # Convert index to integer
            try:
                index = int(index)
            except:
                print(f"Error: Invalid memory index: {index}")
                return None
            
            # Read from memory
            memory_id = self.variables[var_name]['id']
            size = self.variables[var_name]['size']
            
            if index < 0 or index >= size:
                print(f"Error: Memory index out of bounds: {index}")
                return None
            
            return self.heap[memory_id][index]
        
        elif operation == 'write':
            # Write to memory
            if len(parts) < 5:
                print(f"Error: Invalid memory write operation: {line}")
                return None
            
            var_name = parts[2]
            index = parts[3]
            value = parts[4]
            
            # Check if variable exists
            if var_name not in self.variables or self.variables[var_name]['type'] != 'memory':
                print(f"Error: Variable '{var_name}' is not a memory block")
                return None
            
            # Evaluate index
            if index in self.variables:
                index = self.variables[index]
            else:
                try:
                    index = eval(index, {"__builtins__": {}}, self.variables)
                except:
                    pass
            
            # Convert index to integer
            try:
                index = int(index)
            except:
                print(f"Error: Invalid memory index: {index}")
                return None
            
            # Evaluate value
            if value in self.variables:
                value = self.variables[value]
            else:
                try:
                    value = eval(value, {"__builtins__": {}}, self.variables)
                except:
                    pass
            
            # Write to memory
            memory_id = self.variables[var_name]['id']
            size = self.variables[var_name]['size']
            
            if index < 0 or index >= size:
                print(f"Error: Memory index out of bounds: {index}")
                return None
            
            self.heap[memory_id][index] = value
            
            return None
        
        else:
            print(f"Error: Unknown memory operation: {operation}")
            return None
    
    def _handle_object(self, line):
        """Handle object operations."""
        print(f"Object operations not implemented yet: {line}")
        return None
    
    def _handle_import(self, line):
        """Handle import statements."""
        print(f"Import statements not implemented yet: {line}")
        return None
    
    def _handle_export(self, line):
        """Handle export statements."""
        print(f"Export statements not implemented yet: {line}")
        return None
    
    def _handle_try(self, line):
        """Handle try statements."""
        print(f"Try statements not implemented yet: {line}")
        return None
    
    def _handle_catch(self, line):
        """Handle catch statements."""
        print(f"Catch statements not implemented yet: {line}")
        return None
    
    def _handle_finally(self, line):
        """Handle finally statements."""
        print(f"Finally statements not implemented yet: {line}")
        return None
    
    def _handle_throw(self, line):
        """Handle throw statements."""
        print(f"Throw statements not implemented yet: {line}")
        return None
    
    def _handle_method_call(self, line):
        """Handle method call on an object."""
        # Extract object name, method name, and arguments
        dot_index = line.find('.')
        paren_open = line.find('(')
        paren_close = line.find(')')
        
        if dot_index == -1 or paren_open == -1 or paren_close == -1:
            print("Error: Invalid method call syntax")
            return
        
        object_name = line[:dot_index].strip()
        method_name = line[dot_index+1:paren_open].strip()
        
        # Extract arguments
        args_str = line[paren_open+1:paren_close].strip()
        
        # Parse arguments
        if args_str:
            arguments = [arg.strip() for arg in args_str.split(',')]
            
            # Evaluate arguments
            evaluated_args = []
            for arg in arguments:
                if arg in self.variables:
                    evaluated_args.append(self.variables[arg])
                elif arg.startswith('"') and arg.endswith('"'):
                    evaluated_args.append(arg[1:-1])
                else:
                    try:
                        evaluated_args.append(eval(arg, {"__builtins__": {}}, self.variables))
                    except:
                        evaluated_args.append(arg)
        else:
            evaluated_args = []
        
        # Check if object exists
        if object_name not in self.objects:
            print(f"Error: Object '{object_name}' not defined")
            return
        
        # Check if method exists
        if method_name not in self.objects[object_name]['methods']:
            print(f"Error: Method '{method_name}' not defined for object '{object_name}'")
            return
        
        # Call method (simplified for now)
        print(f"Calling method '{method_name}' on object '{object_name}' with arguments: {evaluated_args}")
        
        # Return a simulated return value for now
        return f"Result of {object_name}.{method_name}({', '.join(str(arg) for arg in evaluated_args)})"
    
    def _handle_debug(self, line):
        """Handle debug commands."""
        parts = line.split()
        
        if len(parts) < 2:
            print("Error: Invalid debug command")
            return
        
        command = parts[1]
        
        if command == 'on':
            self.debug_mode = True
            print("Debug mode enabled")
        
        elif command == 'off':
            self.debug_mode = False
            print("Debug mode disabled")
        
        elif command == 'step':
            self.step_by_step = True
            print("Step-by-step execution enabled")
        
        elif command == 'continue':
            self.step_by_step = False
            print("Continuing execution")
        
        elif command == 'variables':
            self._debug_show_variables()
        
        elif command == 'callstack':
            self._debug_show_call_stack()
        
        elif command == 'memory':
            self._debug_show_memory()
    
    def _handle_breakpoint(self, line):
        """Handle breakpoint commands."""
        parts = line.split()
        
        if len(parts) < 3:
            print("Error: Invalid breakpoint command")
            return
        
        command = parts[1]
        
        if command == 'set':
            try:
                line_number = int(parts[2])
                self.breakpoints.add(line_number)
                print(f"Breakpoint set at line {line_number}")
            except ValueError:
                print("Error: Invalid line number")
        
        elif command == 'clear':
            if parts[2] == 'all':
                self.breakpoints.clear()
                print("All breakpoints cleared")
            else:
                try:
                    line_number = int(parts[2])
                    if line_number in self.breakpoints:
                        self.breakpoints.remove(line_number)
                        print(f"Breakpoint at line {line_number} cleared")
                    else:
                        print(f"No breakpoint at line {line_number}")
                except ValueError:
                    print("Error: Invalid line number")
        
        elif command == 'list':
            if self.breakpoints:
                print("Breakpoints:")
                for bp in sorted(self.breakpoints):
                    print(f"  Line {bp}")
            else:
                print("No breakpoints set")
    
    def _debug_pause(self, line):
        """Pause execution for debugging."""
        print(f"\nDEBUG: Paused at line {self.current_line}: {line}")
        
        while True:
            debug_cmd = input("DEBUG> ").strip().lower()
            
            if debug_cmd == 'continue' or debug_cmd == 'c':
                self.step_by_step = False
                break
            
            elif debug_cmd == 'step' or debug_cmd == 's':
                self.step_by_step = True
                break
            
            elif debug_cmd == 'variables' or debug_cmd == 'vars':
                self._debug_show_variables()
            
            elif debug_cmd == 'callstack' or debug_cmd == 'stack':
                self._debug_show_call_stack()
            
            elif debug_cmd == 'memory' or debug_cmd == 'mem':
                self._debug_show_memory()
            
            elif debug_cmd == 'help' or debug_cmd == 'h':
                self._debug_show_help()
            
            elif debug_cmd == 'quit' or debug_cmd == 'q':
                print("Exiting debug mode")
                self.debug_mode = False
                self.step_by_step = False
                break
            
            else:
                print("Unknown debug command. Type 'help' for available commands.")
    
    def _debug_show_variables(self):
        """Show all variables in debug mode."""
        print("\nVariables:")
        if self.variables:
            for name, value in self.variables.items():
                print(f"  {name} = {value}")
        else:
            print("  No variables defined")
    
    def _debug_show_call_stack(self):
        """Show call stack in debug mode."""
        print("\nCall Stack:")
        if self.call_stack:
            for i, frame in enumerate(reversed(self.call_stack)):
                print(f"  {i}: {frame}")
        else:
            print("  Call stack is empty")
    
    def _debug_show_memory(self):
        """Show memory usage in debug mode."""
        print("\nMemory Usage:")
        print(f"  Heap objects: {len(self.heap)}")
        print(f"  Stack size: {len(self.stack)}")
        print(f"  Virtual memory objects: {len(self.virtual_memory)}")
        print(f"  Memory pages: {len(self.pages)}")
        print(f"  Swap area: {len(self.swap_area)}")
    
    def _debug_show_help(self):
        """Show debug help."""
        print("\nDebug Commands:")
        print("  continue (c) - Continue execution")
        print("  step (s) - Step to next line")
        print("  variables (vars) - Show all variables")
        print("  callstack (stack) - Show call stack")
        print("  memory (mem) - Show memory usage")
        print("  help (h) - Show this help")
        print("  quit (q) - Exit debug mode")
    
    def _handle_stdlib_call(self, line):
        """Handle standard library function calls."""
        # Extract function name and arguments
        paren_open = line.find('(')
        paren_close = line.rfind(')')
        
        if paren_open == -1 or paren_close == -1:
            print(f"Error: Invalid standard library call syntax: {line}")
            return None
        
        full_function_name = line[:paren_open].strip()
        args_str = line[paren_open+1:paren_close].strip()
        
        # Split namespace and function name
        if '.' not in full_function_name:
            print(f"Error: Invalid standard library call: {full_function_name}")
            return None
            
        namespace, function_name = full_function_name.split('.', 1)
        stdlib_function_name = f"{namespace}_{function_name}"
        
        # Parse arguments
        if args_str:
            args = [arg.strip() for arg in args_str.split(',')]
            
            # Evaluate arguments
            evaluated_args = []
            for arg in args:
                if arg in self.variables:
                    evaluated_args.append(self.variables[arg])
                elif arg.startswith('"') and arg.endswith('"'):
                    evaluated_args.append(arg[1:-1])
                else:
                    try:
                        evaluated_args.append(eval(arg, {"__builtins__": {}}, self.variables))
                    except:
                        evaluated_args.append(arg)
        else:
            evaluated_args = []
        
        # Check if the function exists in the standard library
        if stdlib_function_name in self.stdlib_functions:
            # Call the standard library function
            result = self.stdlib_functions[stdlib_function_name](evaluated_args)
            return result
        else:
            print(f"Error: Standard library function '{full_function_name}' not found")
            return None

    def _handle_class(self, line):
        """Handle class definitions."""
        # Extract class name
        match = re.match(r'class\s+(\w+)', line)
        if not match:
            print(f"Error: Invalid class definition: {line}")
            return None
        
        class_name = match.group(1)
        
        # Store class definition
        self.variables[class_name] = {
            'type': 'class',
            'attributes': {},
            'methods': {}
        }
        
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python axon.py <filename>")
        return
    
    filename = sys.argv[1]
    interpreter = AxonInterpreter()
    interpreter.run_file(filename)

if __name__ == "__main__":
    main() 