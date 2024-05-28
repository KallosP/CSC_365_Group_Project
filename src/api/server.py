from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import task, user, sort, tags, summary, analytics, scheduler
import json
import logging
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

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# NOTE: This is where endpoints are added
app.include_router(task.router)
app.include_router(user.router)
app.include_router(summary.router)
app.include_router(sort.router)
app.include_router(tags.router)
app.include_router(summary.router)
app.include_router(analytics.router)
app.include_router(scheduler.router)

# Handle server errors
@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

# Home page message
@app.get("/")
async def root():
    return {"message": "Task Manager API."}
