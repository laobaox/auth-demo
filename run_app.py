import uvicorn
from auth_demo.app import app
from auth_demo import config


def main():
    uvicorn.run(app, host='0.0.0.0', port=config.get_port())


if __name__ == '__main__':
    main()