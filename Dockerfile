# 1. Usamos una imagen oficial, segura y ligera de Python
FROM python:3.11-slim

# 2. Variables de entorno para optimizar Python en contenedores
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro de nuestro "paquete"
WORKDIR /app

# 4. Instalamos dependencias del sistema necesarias para compilar psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiamos la lista de dependencias y las instalamos
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. Copiamos el código de la aplicación al contenedor
COPY . /app/

# 7. Exponemos el puerto estándar
EXPOSE 8000

# 8. Comando de producción: Gunicorn gestionando workers de Uvicorn
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
