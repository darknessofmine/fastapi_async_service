import uvicorn
from fastapi import FastAPI

from api.auth.views import router as auth_router
from api.comments.views import router as comment_router
from api.subscriptions.views import router as sub_router
from api.posts.views import router as post_router
from api.users.views import router as user_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(sub_router)
app.include_router(post_router)
app.include_router(comment_router)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
