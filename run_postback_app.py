import uvicorn

from app.init_app import app


if __name__ == '__main__':
    uvicorn.run('run_postback_app:app', host='0.0.0.0', port=8535)