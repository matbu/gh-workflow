#!/usr/bin/env python3
"""
Test file with intentional security vulnerabilities
for testing the security scan workflow
"""

import os
import subprocess

# VULNERABILITY 1: Hardcoded credentials
DATABASE_PASSWORD = "SuperSecret123!"
API_KEY = "sk-1234567890abcdef"

# VULNERABILITY 2: SQL Injection
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    # This is vulnerable to SQL injection
    return execute_query(query)

# VULNERABILITY 3: Command Injection
def process_file(filename):
    # Dangerous - user input directly in shell command
    cmd = f"cat {filename}"
    return subprocess.run(cmd, shell=True, capture_output=True)

# VULNERABILITY 4: Path Traversal
def read_file(user_path):
    # No validation - user could access any file with ../
    with open(f"/var/data/{user_path}", 'r') as f:
        return f.read()

# VULNERABILITY 5: Weak cryptography
def encrypt_password(password):
    # MD5 is cryptographically broken
    import hashlib
    return hashlib.md5(password.encode()).hexdigest()

def execute_query(query):
    # Dummy function
    pass
