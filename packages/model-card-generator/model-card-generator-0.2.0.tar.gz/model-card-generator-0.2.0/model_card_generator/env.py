import os

def get_env(name: str) -> str:
    """Get environment variable value"""
    
    return os.environ[name]