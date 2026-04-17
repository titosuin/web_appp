"""
Utility functions for the application.
"""


def calculate_macros(weight, height, activity_level, goal):
    """Calculate daily macro requirements based on physical stats."""
    bmr = (10 * weight) + (6.25 * height) - (5 * 25) + 5

    am = {
        "Sedentario": 1.2,
        "Ligero": 1.375,
        "Moderado": 1.55,
        "Fuerte": 1.725,
    }.get(activity_level, 1.55)

    tdee = bmr * am

    if goal == "Volumen":
        cals = tdee + 400
    elif goal == "Déficit":
        cals = tdee - 500
    else:
        cals = tdee

    protein = weight * 2.2
    fat = (cals * 0.25) / 9
    carbs = (cals - (protein * 4) - (fat * 9)) / 4

    return {
        "calories": int(cals),
        "protein": int(protein),
        "fat": int(fat),
        "carbs": int(max(carbs, 0)),
    }


def calculate_rank(sq_rm, bp_rm, dl_rm, body_weight):
    """Calculate the user's lifting rank based on 1RMs and body weight."""
    total = sq_rm + bp_rm + dl_rm
    if total == 0:
        return "Pendiente de Test"
    ratio = total / body_weight if body_weight > 0 else 0

    if ratio >= 3.5:
        return "Élite"
    if ratio >= 2.8:
        return "Avanzado"
    if ratio >= 2.0:
        return "Intermedio"
    return "Novato"


def generate_routine(days_per_week, goal="Composición"):
    """Generate a workout schedule based on days available and goal."""
    # pylint: disable=too-many-return-statements
    if goal == "Powerlifting":
        if days_per_week <= 3:
            return {
                "name": "Powerlifting Básico 3 Días",
                "description": "Fuerza máxima para SBD (Squat, Bench, Deadlift). Prioriza intensidad sobre volumen.",
                "schedule": [
                    "Día 1: Sentadilla + 3 Auxiliares",
                    "Día 2: Press Banca + 4 Auxiliares",
                    "Día 3: Peso Muerto + 3 Auxiliares",
                ],
            }
        return {
            "name": "Powerlifting Texas/Candito",
            "description": "Distribución avanzada con control de cargas máximas. 5-6 ejercicios por sesión en total.",
            "schedule": [
                "Lunes: Sentadilla (Pesado) + 2 Acces.",
                "Martes: Banca (Volumen) + 4 Acces.",
                "Jueves: Peso Muerto (Pesado) + 2 Acces.",
                "Viernes: Banca (Pesado) + 3 Acces.",
            ],
        }

    if days_per_week <= 2:
        return {
            "name": "Full Body (Cuerpo Completo)",
            "description": "Rutina de entrenamiento de ~7 ejercicios por sesión. Ideal para mantener fuerza global.",
            "schedule": [
                "Día 1: Full Body A",
                "Día 2: Descanso",
                "Día 3: Descanso",
                "Día 4: Full Body B",
                "Día 5, 6, 7: Descanso",
            ],
        }
    if days_per_week == 3:
        return {
            "name": "Full Body Avanzado (Arnold Base)",
            "description": "Rutina de hipertrofia de ~6-8 ejercicios por sesión.",
            "schedule": [
                "Lunes: Push Completo",
                "Miércoles: Pull Completo",
                "Viernes: Pierna y Core",
            ],
        }
    if days_per_week == 4:
        return {
            "name": "Upper / Lower (Torso/Pierna)",
            "description": "Dividimos el cuerpo en dos mitades (6 ejercicios por día). Recomendado para estética.",
            "schedule": [
                "Lunes: Torso",
                "Martes: Pierna",
                "Jueves: Torso",
                "Viernes: Pierna",
            ],
        }
    if days_per_week >= 5:
        return {
            "name": "Push / Pull / Legs (PPL)",
            "description": "Alta frecuencia y volumen. 5-7 ejercicios por día para pura Hipertrofia.",
            "schedule": [
                "Día 1: Push",
                "Día 2: Pull",
                "Día 3: Legs",
                "Día 4: Push",
                "Día 5: Pull",
                "Día 6: Legs",
                "Día 7: Descanso",
            ],
        }
    return {
        "name": "Rutina General",
        "description": "Por favor ajusta tus días de disponibilidad.",
        "schedule": [],
    }
