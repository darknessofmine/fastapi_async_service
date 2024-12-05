from fastapi import FastAPI

from api.auth.views import router as auth_router
from api.subscriptions.views import router as sub_router
from api.users.views import router as user_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(sub_router)
