from fastapi import FastAPI, APIRouter
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.users import users_router as users
from app.auth import auth_router as login
from app.questions import questions_router as questions
from app.answers import answers_router as answers


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

api_router = APIRouter(prefix=settings.API_V1_STR)

api_router.include_router(users.router)
api_router.include_router(login.router)
api_router.include_router(questions.router)
api_router.include_router(router=answers.router)
app.include_router(api_router)


router = APIRouter(tags=["health-check"])


@router.get("/health-check/")
async def health_check() -> bool:
    return True


app.include_router(router)
