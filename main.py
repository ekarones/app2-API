from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crud import advice, auth, disease, user, utils, record, admin, notification

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(advice.router, tags=["Advice"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(disease.router, tags=["Disease"])
app.include_router(user.router, tags=["User"])
app.include_router(utils.router, tags=["Utils"])
app.include_router(record.router, tags=["Record"])
app.include_router(admin.router, tags=["Admin"])
app.include_router(notification.router, tags=["Notification"])
