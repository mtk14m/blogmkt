FROM ghcr.io/astral-sh/uv:python3.12-alpine
# Définir le répertoire de travail
WORKDIR /app

# Empêcher Python de générer des fichiers .pyc et forcer l'affichage des logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copier uniquement les fichiers de dépendances pour profiter du cache Docker
COPY pyproject.toml uv.lock ./

# Installer les dépendances sans créer de venv (plus simple en Docker)
RUN uv sync --frozen --no-cache

# Copier le reste du code source
COPY . .

# Exposer le port par défaut de FastAPI
EXPOSE 8000

# Lancer l'application avec uv run
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]