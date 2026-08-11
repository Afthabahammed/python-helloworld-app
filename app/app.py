import os
import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Deployment App")


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "FastAPI deployed successfully!"
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
