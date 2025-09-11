import os

from app import create_app

app = create_app()


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "postgresql://postgres:1234@localhost:5432/user_db"
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
