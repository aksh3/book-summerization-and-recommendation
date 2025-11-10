import uvicorn
from asgiref.wsgi import WsgiToAsgi

from app.main import create_app

app = create_app()
asgi_app = WsgiToAsgi(app)
if __name__ == "__main__":
    uvicorn.run(asgi_app, host="127.0.0.1", port=5000)
