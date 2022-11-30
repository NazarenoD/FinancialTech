from fastapi import FastAPI
from routers import capm
app = FastAPI()


app.include_router(capm.router)