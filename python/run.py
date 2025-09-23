from app import create_app

app = create_app()

# Punto di ingresso principale dell'applicazione
if __name__ == "__main__":
    app.run()