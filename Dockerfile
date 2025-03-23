# Dockerfile
FROM python:3.10

# Ustawiamy katalog roboczy
WORKDIR /app

# Kopiujemy plik z zależnościami
COPY requirements.txt .

# Instalujemy zależności (tu właśnie powinien się zainstalować uvicorn)
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy resztę kodu do kontenera
COPY . .

# Uruchamiamy aplikację (zakładam, że plik główny to 'main.py' w tym samym folderze)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
