import uvicorn

from src.config import settings
from src.core.app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "src.__main__:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )