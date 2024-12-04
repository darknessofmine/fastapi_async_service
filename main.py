from fastapi import FastAPI

from api.subscriptions.views import router as sub_router
from api.users.views import router as user_router


app = FastAPI()
app.include_router(user_router)
app.include_router(sub_router)
