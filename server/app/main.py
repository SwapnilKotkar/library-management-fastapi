from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user_routes, book_routes
from app.core.middleware import limiter, limiter_middleware

app = FastAPI()
app.state.limiter = limiter
app.add_middleware(limiter_middleware)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(user_routes.router, prefix="/api", tags=["Users"])
app.include_router(book_routes.router, prefix="/api", tags=["Books"])
