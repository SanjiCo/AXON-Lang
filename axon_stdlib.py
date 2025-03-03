#!/usr/bin/env python3

import math
import time
import os
import sys
import json
import random
import datetime
import platform
import subprocess

class AxonStdLib:
    def __init__(self, interpreter):
        """Initialize the standard library."""
        self.interpreter = interpreter
        self.functions = {}
        self.register_stdlib_functions()
    
    def register_stdlib_functions(self):
        """Register all standard library functions."""
        self.register_math_functions()
        self.register_string_functions()
        self.register_time_functions()
        self.register_system_functions()
        self.register_file_functions()
        self.register_json_functions()
        self.register_random_functions()
    
    def register_math_functions(self):
        """Register math functions."""
        # Math functions
        self.functions["math_sin"] = self.math_sin
        self.functions["math_cos"] = self.math_cos
        self.functions["math_tan"] = self.math_tan
        self.functions["math_sqrt"] = self.math_sqrt
        self.functions["math_pow"] = self.math_pow
        self.functions["math_abs"] = self.math_abs
        self.functions["math_floor"] = self.math_floor
        self.functions["math_ceil"] = self.math_ceil
        self.functions["math_round"] = self.math_round
        self.functions["math_max"] = self.math_max
        self.functions["math_min"] = self.math_min
        self.functions["math_log"] = self.math_log
        self.functions["math_log10"] = self.math_log10
        self.functions["math_exp"] = self.math_exp
        self.functions["math_pi"] = self.math_pi
        self.functions["math_e"] = self.math_e
    
    def register_string_functions(self):
        """Register string functions."""
        # String functions
        self.functions["string_length"] = self.string_length
        self.functions["string_concat"] = self.string_concat
        self.functions["string_upper"] = self.string_upper
        self.functions["string_lower"] = self.string_lower
        self.functions["string_replace"] = self.string_replace
        self.functions["string_split"] = self.string_split
        self.functions["string_join"] = self.string_join
        self.functions["string_trim"] = self.string_trim
        self.functions["string_substring"] = self.string_substring
        self.functions["string_startswith"] = self.string_startswith
        self.functions["string_endswith"] = self.string_endswith
    
    def register_time_functions(self):
        """Register time functions."""
        # Time functions
        self.functions["time_now"] = self.time_now
        self.functions["time_sleep"] = self.time_sleep
        self.functions["time_date"] = self.time_date
        self.functions["time_timestamp"] = self.time_timestamp
        self.functions["time_format"] = self.time_format
    
    def register_system_functions(self):
        """Register system functions."""
        # System functions
        self.functions["system_os"] = self.system_os
        self.functions["system_env"] = self.system_env
        self.functions["system_exit"] = self.system_exit
        self.functions["system_exec"] = self.system_exec
    
    def register_file_functions(self):
        """Register file functions."""
        # File functions
        self.functions["file_exists"] = self.file_exists
        self.functions["file_read"] = self.file_read
        self.functions["file_write"] = self.file_write
        self.functions["file_append"] = self.file_append
        self.functions["file_delete"] = self.file_delete
        self.functions["file_size"] = self.file_size
        self.functions["file_readlines"] = self.file_readlines
    
    def register_json_functions(self):
        """Register JSON functions."""
        # JSON functions
        self.functions["json_parse"] = self.json_parse
        self.functions["json_stringify"] = self.json_stringify
    
    def register_random_functions(self):
        """Register random functions."""
        # Random functions
        self.functions["random_int"] = self.random_int
        self.functions["random_float"] = self.random_float
        self.functions["random_choice"] = self.random_choice
        self.functions["random_bool"] = self.random_bool
    
    # Math functions
    def math_sin(self, args):
        """Calculate the sine of a number."""
        if len(args) != 1:
            return "Error: math.sin() takes exactly 1 argument"
        try:
            return math.sin(float(args[0]))
        except:
            return "Error: Invalid argument for math.sin()"
    
    def math_cos(self, args):
        """Calculate the cosine of a number."""
        if len(args) != 1:
            return "Error: math.cos() takes exactly 1 argument"
        try:
            return math.cos(float(args[0]))
        except:
            return "Error: Invalid argument for math.cos()"
    
    def math_tan(self, args):
        """Calculate the tangent of a number."""
        if len(args) != 1:
            return "Error: math.tan() takes exactly 1 argument"
        try:
            return math.tan(float(args[0]))
        except:
            return "Error: Invalid argument for math.tan()"
    
    def math_sqrt(self, args):
        """Calculate the square root of a number."""
        if len(args) != 1:
            return "Error: math.sqrt() takes exactly 1 argument"
        try:
            return math.sqrt(float(args[0]))
        except:
            return "Error: Invalid argument for math.sqrt()"
    
    def math_pow(self, args):
        """Calculate the power of a number."""
        if len(args) != 2:
            return "Error: math.pow() takes exactly 2 arguments"
        try:
            return math.pow(float(args[0]), float(args[1]))
        except:
            return "Error: Invalid arguments for math.pow()"
    
    def math_abs(self, args):
        """Calculate the absolute value of a number."""
        if len(args) != 1:
            return "Error: math.abs() takes exactly 1 argument"
        try:
            return abs(float(args[0]))
        except:
            return "Error: Invalid argument for math.abs()"
    
    def math_floor(self, args):
        """Calculate the floor of a number."""
        if len(args) != 1:
            return "Error: math.floor() takes exactly 1 argument"
        try:
            return math.floor(float(args[0]))
        except:
            return "Error: Invalid argument for math.floor()"
    
    def math_ceil(self, args):
        """Calculate the ceiling of a number."""
        if len(args) != 1:
            return "Error: math.ceil() takes exactly 1 argument"
        try:
            return math.ceil(float(args[0]))
        except:
            return "Error: Invalid argument for math.ceil()"
    
    def math_round(self, args):
        """Round a number to the nearest integer."""
        if len(args) != 1:
            return "Error: math.round() takes exactly 1 argument"
        try:
            return round(float(args[0]))
        except:
            return "Error: Invalid argument for math.round()"
    
    def math_max(self, args):
        """Return the maximum of two numbers."""
        if len(args) != 2:
            return "Error: math.max() takes exactly 2 arguments"
        try:
            return max(float(args[0]), float(args[1]))
        except:
            return "Error: Invalid arguments for math.max()"
    
    def math_min(self, args):
        """Return the minimum of two numbers."""
        if len(args) != 2:
            return "Error: math.min() takes exactly 2 arguments"
        try:
            return min(float(args[0]), float(args[1]))
        except:
            return "Error: Invalid arguments for math.min()"
    
    def math_log(self, args):
        """Calculate the natural logarithm of a number."""
        if len(args) != 1:
            return "Error: math.log() takes exactly 1 argument"
        try:
            return math.log(float(args[0]))
        except:
            return "Error: Invalid argument for math.log()"
    
    def math_log10(self, args):
        """Calculate the base-10 logarithm of a number."""
        if len(args) != 1:
            return "Error: math.log10() takes exactly 1 argument"
        try:
            return math.log10(float(args[0]))
        except:
            return "Error: Invalid argument for math.log10()"
    
    def math_exp(self, args):
        """Calculate the exponential of a number."""
        if len(args) != 1:
            return "Error: math.exp() takes exactly 1 argument"
        try:
            return math.exp(float(args[0]))
        except:
            return "Error: Invalid argument for math.exp()"
    
    def math_pi(self, args):
        """Return the value of pi."""
        if len(args) != 0:
            return "Error: math.pi() takes no arguments"
        return math.pi
    
    def math_e(self, args):
        """Return the value of e."""
        if len(args) != 0:
            return "Error: math.e() takes no arguments"
        return math.e
    
    # String functions
    def string_length(self, args):
        """Return the length of a string."""
        if len(args) != 1:
            return "Error: string.length() takes exactly 1 argument"
        try:
            return len(str(args[0]))
        except:
            return "Error: Invalid argument for string.length()"
    
    def string_concat(self, args):
        """Concatenate two strings."""
        if len(args) != 2:
            return "Error: string.concat() takes exactly 2 arguments"
        try:
            return str(args[0]) + str(args[1])
        except:
            return "Error: Invalid arguments for string.concat()"
    
    def string_upper(self, args):
        """Convert a string to uppercase."""
        if len(args) != 1:
            return "Error: string.upper() takes exactly 1 argument"
        try:
            return str(args[0]).upper()
        except:
            return "Error: Invalid argument for string.upper()"
    
    def string_lower(self, args):
        """Convert a string to lowercase."""
        if len(args) != 1:
            return "Error: string.lower() takes exactly 1 argument"
        try:
            return str(args[0]).lower()
        except:
            return "Error: Invalid argument for string.lower()"
    
    def string_replace(self, args):
        """Replace a substring in a string."""
        if len(args) != 3:
            return "Error: string.replace() takes exactly 3 arguments"
        try:
            return str(args[0]).replace(str(args[1]), str(args[2]))
        except:
            return "Error: Invalid arguments for string.replace()"
    
    def string_split(self, args):
        """Split a string by a delimiter."""
        if len(args) != 2:
            return "Error: string.split() takes exactly 2 arguments"
        try:
            return str(args[0]).split(str(args[1]))
        except:
            return "Error: Invalid arguments for string.split()"
    
    def string_join(self, args):
        """Join a list of strings with a delimiter."""
        if len(args) != 2:
            return "Error: string.join() takes exactly 2 arguments"
        try:
            return str(args[0]).join(args[1])
        except:
            return "Error: Invalid arguments for string.join()"
    
    def string_trim(self, args):
        """Trim whitespace from a string."""
        if len(args) != 1:
            return "Error: string.trim() takes exactly 1 argument"
        try:
            return str(args[0]).strip()
        except:
            return "Error: Invalid argument for string.trim()"
    
    def string_substring(self, args):
        """Get a substring from a string."""
        if len(args) != 3:
            return "Error: string.substring() takes exactly 3 arguments"
        try:
            return str(args[0])[int(args[1]):int(args[2])]
        except:
            return "Error: Invalid arguments for string.substring()"
    
    def string_startswith(self, args):
        """Check if a string starts with a substring."""
        if len(args) != 2:
            return "Error: string.startswith() takes exactly 2 arguments"
        try:
            return str(args[0]).startswith(str(args[1]))
        except:
            return "Error: Invalid arguments for string.startswith()"
    
    def string_endswith(self, args):
        """Check if a string ends with a substring."""
        if len(args) != 2:
            return "Error: string.endswith() takes exactly 2 arguments"
        try:
            return str(args[0]).endswith(str(args[1]))
        except:
            return "Error: Invalid arguments for string.endswith()"
    
    # Time functions
    def time_now(self, args):
        """Return the current time."""
        if len(args) != 0:
            return "Error: time.now() takes no arguments"
        return datetime.datetime.now().strftime("%H:%M:%S")
    
    def time_sleep(self, args):
        """Sleep for a specified number of seconds."""
        if len(args) != 1:
            return "Error: time.sleep() takes exactly 1 argument"
        try:
            time.sleep(float(args[0]))
            return None
        except:
            return "Error: Invalid argument for time.sleep()"
    
    def time_date(self, args):
        """Return the current date."""
        if len(args) != 0:
            return "Error: time.date() takes no arguments"
        return datetime.datetime.now().strftime("%Y-%m-%d")
    
    def time_timestamp(self, args):
        """Return the current timestamp."""
        if len(args) != 0:
            return "Error: time.timestamp() takes no arguments"
        return time.time()
    
    def time_format(self, args):
        """Format a datetime object."""
        if len(args) != 1:
            return "Error: time.format() takes exactly 1 argument"
        try:
            return datetime.datetime.now().strftime(str(args[0]))
        except:
            return "Error: Invalid argument for time.format()"
    
    # System functions
    def system_os(self, args):
        """Return the operating system name."""
        if len(args) != 0:
            return "Error: system.os() takes no arguments"
        return platform.system()
    
    def system_env(self, args):
        """Return the value of an environment variable."""
        if len(args) != 1:
            return "Error: system.env() takes exactly 1 argument"
        try:
            return os.environ.get(str(args[0]), "")
        except:
            return "Error: Invalid argument for system.env()"
    
    def system_exit(self, args):
        """Exit the program."""
        if len(args) > 1:
            return "Error: system.exit() takes at most 1 argument"
        try:
            sys.exit(int(args[0]) if args else 0)
        except:
            return "Error: Invalid argument for system.exit()"
    
    def system_exec(self, args):
        """Execute a system command."""
        if len(args) != 1:
            return "Error: system.exec() takes exactly 1 argument"
        try:
            return subprocess.getoutput(str(args[0]))
        except:
            return "Error: Invalid argument for system.exec()"
    
    # File functions
    def file_exists(self, args):
        """Check if a file exists."""
        if len(args) != 1:
            return "Error: file.exists() takes exactly 1 argument"
        try:
            return os.path.exists(str(args[0]))
        except:
            return "Error: Invalid argument for file.exists()"
    
    def file_read(self, args):
        """Read the contents of a file."""
        if len(args) != 1:
            return "Error: file.read() takes exactly 1 argument"
        try:
            with open(str(args[0]), 'r') as f:
                return f.read()
        except:
            return "Error: Invalid argument for file.read()"
    
    def file_write(self, args):
        """Write to a file."""
        if len(args) != 2:
            return "Error: file.write() takes exactly 2 arguments"
        try:
            with open(str(args[0]), 'w') as f:
                f.write(str(args[1]))
            return True
        except:
            return "Error: Invalid arguments for file.write()"
    
    def file_append(self, args):
        """Append to a file."""
        if len(args) != 2:
            return "Error: file.append() takes exactly 2 arguments"
        try:
            with open(str(args[0]), 'a') as f:
                f.write(str(args[1]))
            return True
        except:
            return "Error: Invalid arguments for file.append()"
    
    def file_delete(self, args):
        """Delete a file."""
        if len(args) != 1:
            return "Error: file.delete() takes exactly 1 argument"
        try:
            os.remove(str(args[0]))
            return True
        except:
            return "Error: Invalid argument for file.delete()"
    
    def file_size(self, args):
        """Return the size of a file."""
        if len(args) != 1:
            return "Error: file.size() takes exactly 1 argument"
        try:
            return os.path.getsize(str(args[0]))
        except:
            return "Error: Invalid argument for file.size()"
    
    def file_readlines(self, args):
        """Read the lines of a file."""
        if len(args) != 1:
            return "Error: file.readlines() takes exactly 1 argument"
        try:
            with open(str(args[0]), 'r') as f:
                return f.readlines()
        except:
            return "Error: Invalid argument for file.readlines()"
    
    # JSON functions
    def json_parse(self, args):
        """Parse a JSON string."""
        if len(args) != 1:
            return "Error: json.parse() takes exactly 1 argument"
        try:
            return json.loads(str(args[0]))
        except:
            return "Error: Invalid argument for json.parse()"
    
    def json_stringify(self, args):
        """Convert an object to a JSON string."""
        if len(args) != 1:
            return "Error: json.stringify() takes exactly 1 argument"
        try:
            return json.dumps(args[0])
        except:
            return "Error: Invalid argument for json.stringify()"
    
    # Random functions
    def random_int(self, args):
        """Generate a random integer."""
        if len(args) != 2:
            return "Error: random.int() takes exactly 2 arguments"
        try:
            return random.randint(int(args[0]), int(args[1]))
        except:
            return "Error: Invalid arguments for random.int()"
    
    def random_float(self, args):
        """Generate a random float."""
        if len(args) != 0:
            return "Error: random.float() takes no arguments"
        return random.random()
    
    def random_choice(self, args):
        """Choose a random element from a list."""
        if len(args) != 1:
            return "Error: random.choice() takes exactly 1 argument"
        try:
            return random.choice(args[0])
        except:
            return "Error: Invalid argument for random.choice()"
    
    def random_bool(self, args):
        """Generate a random boolean."""
        if len(args) != 0:
            return "Error: random.bool() takes no arguments"
        return random.choice([True, False]) 