import os


def _clean_env(value: str | None, default: str) -> str:
    if value is None:
        return default
    return value.strip().strip("\"'")


DATABASE_URL = _clean_env(
    os.getenv("DATABASE_URL"),
    "postgresql+psycopg://blogmkt:blogmkt@localhost:5432/blogmkt",
)
JWT_SECRET_KEY = _clean_env(
    os.getenv("JWT_SECRET_KEY") or os.getenv("jwt_secret"),
    "change-me-in-production",
)
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"),
)
