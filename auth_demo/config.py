import os


def get_host():
    return os.environ.get("API_HOST", "localhost")

def get_port():
    return os.environ.get('API_PORT', 8000)

def get_api_url():
    host = get_host()
    port = get_port()
    return f"http://{host}:{port}"