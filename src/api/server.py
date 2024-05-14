from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import task_crud, user, sort, tags, summary
import json
import logging
import sys
from starlette.middleware.cors import CORSMiddleware

description = """
General purpose Task Manager API.
"""

app = FastAPI(
    title="Task Manager",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
)

#origins = ["https://potion-exchange.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    #allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

#app.include_router(inventory.router)
#app.include_router(carts.router)
#app.include_router(catalog.router)
#app.include_router(bottler.router)
#app.include_router(barrels.router)
#app.include_router(admin.router)
#app.include_router(info.router)

# NOTE: This is where endpoints are added
app.include_router(task_crud.router)
app.include_router(user.router)
app.include_router(sort.router)
app.include_router(tags.router)
app.include_router(summary.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Task Manager API."}
