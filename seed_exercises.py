"""
Script to seed the database with initial exercise data.
"""

import requests
from models import db, Exercise

URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"


def seed():
    """Seed exercises from external source into the database."""
    try:
        if Exercise.query.count() > 0:
            print("DB ya poblada de ejercicios.")
            return

        print("Descargando datos masivos...")
        try:
            r = requests.get(URL, timeout=15)
            if r.status_code == 200:
                data = r.json()
                count = 0
                for ex in data:
                    new_ex = Exercise(
                        name=(ex.get("name") or "")[:255],
                        level=(ex.get("level") or "")[:50],
                        force=(ex.get("force") or "")[:50],
                        equipment=(ex.get("equipment") or "")[:100],
                        primary_muscles=",".join(
                            ex.get("primaryMuscles") or []
                        )[:255],
                        instructions=" ".join(ex.get("instructions") or [])[
                            :2000
                        ],
                        category=(ex.get("category") or "")[:100],
                        image_url=(
                            (
                                "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/"
                                + ex.get("images")[0]
                            )
                            if ex.get("images") and len(ex.get("images")) > 0
                            else "https://images.pexels.com/photos/1552242/pexels-photo-1552242.jpeg?auto=compress&cs=tinysrgb&w=600"
                        ),
                    )
                    db.session.add(new_ex)
                    count += 1
                db.session.commit()
                print(f"Éxito: {count} ejercicios listos.")
            else:
                print("Error:", r.status_code)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print("Hubo un error de conexión:", e)
    except Exception as main_e:
        print("Error general en seed:", main_e)


if __name__ == "__main__":
    from app import app
    with app.app_context():
        seed()
