FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app

COPY requirements.txt ./
RUN uv pip install --system --no-cache -r requirements.txt

COPY export.py run.sh ./
RUN chmod +x run.sh

# The export is a scheduled task, not a service: the container idles and
# Coolify execs run.sh into it on the cron expression.
CMD ["sleep", "infinity"]
