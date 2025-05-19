FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install watchgod

# Copiar el código de la aplicación
COPY . .

# Configurar variables de entorno
ENV PYTHONPATH=/app
ENV FLASK_APP=app
ENV FLASK_ENV=development

# Exponer el puerto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0", "--reload"]
