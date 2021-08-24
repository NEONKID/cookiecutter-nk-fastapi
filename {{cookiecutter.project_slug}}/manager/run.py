import uvicorn

from manager.src.app import create_app

if __name__ == "__main__":
    uvicorn.run(create_app(), host="127.0.0.1", port=5001, log_level="debug")