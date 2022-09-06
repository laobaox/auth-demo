import os


def get_host():
    return os.environ.get("API_HOST", "127.0.0.1")


def get_port():
    return int(os.environ.get('API_PORT', 8000))


def get_api_url():
    host = get_host()
    port = get_port()
    return f"http://{host}:{port}"


def get_token_expire_seconds():
    return int(os.environ.get('TOKEN_EXPIRE_SECONDS', 7200))