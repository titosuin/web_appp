"""
Application routing module.
"""

import re
import urllib.request
import urllib.parse
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import emit
from deep_translator import GoogleTranslator
from models import User, PhysicalStats, Exercise, WorkoutLog
from utils import calculate_rank, generate_routine, calculate_macros


def register_routes(app, db, socketio):
    """Registers all application routes."""

    # pylint: disable=too-many-locals,too-many-statements
    @app.route("/", methods=["GET", "POST"])
    def login():
        if "user_id" in session:
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            action = request.form.get("action")  # 'login' or 'register'

            if action == "register":
                if User.query.filter_by(username=username).first():
                    flash("El usuario ya existe.")
                else:
                    new_user = User(
                        username=username,
                        email=username + "@ironmind.com",
                        password_hash=generate_password_hash(password),
                    )
                    db.session.add(new_user)
                    db.session.commit()
                    session["user_id"] = new_user.id
                    return redirect(url_for("onboarding"))
            elif action == "login":
                user = User.query.filter_by(username=username).first()
                if user and check_password_hash(user.password_hash, password):
                    session["user_id"] = user.id
                    return redirect(url_for("dashboard"))
                flash("Credenciales incorrectas.")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/onboarding", methods=["GET", "POST"])
    def onboarding():
        if "user_id" not in session:
            return redirect(url_for("login"))
        user = User.query.get(session["user_id"])
        if not user:
            session.clear()
            return redirect(url_for("login"))

        if request.method == "POST":
            try:
                weight = float(request.form.get("weight"))
                height = float(request.form.get("height"))
                activity = request.form.get("activity_level")
                goal = request.form.get("goal")
                days = int(request.form.get("days_per_week", 3))

                stats = PhysicalStats(
                    user_id=user.id,
                    weight=weight,
                    height=height,
                    activity_level=activity,
                    goal=goal,
                )
                db.session.add(stats)
                user.onboarded = True
                session["days_per_week"] = days
                db.session.commit()
                return redirect(url_for("dashboard"))
            except ValueError:
                flash("Por favor ingresa valores válidos.")

        return render_template("onboarding.html", user=user)

    @app.route("/dashboard")
    def dashboard():
        if "user_id" not in session:
            return redirect(url_for("login"))
        user = User.query.get(session["user_id"])
        if not user:
            session.clear()
            return redirect(url_for("login"))
        if not user.onboarded:
            return redirect(url_for("onboarding"))

        days = session.get("days_per_week", 3)
        routine = generate_routine(days, user.stats.goal)
        macros = calculate_macros(
            user.stats.weight,
            user.stats.height,
            user.stats.activity_level,
            user.stats.goal,
        )

        return render_template(
            "dashboard.html", user=user, routine=routine, macros=macros
        )

    @app.route("/settings", methods=["GET", "POST"])
    def settings():
        if "user_id" not in session:
            return redirect(url_for("login"))
        user = User.query.get(session["user_id"])
        if not user:
            session.clear()
            return redirect(url_for("login"))

        if request.method == "POST":
            try:
                user.stats.weight = float(
                    request.form.get("weight") or user.stats.weight
                )
                user.stats.activity_level = (
                    request.form.get("activity_level")
                    or user.stats.activity_level
                )
                user.stats.goal = request.form.get("goal") or user.stats.goal
                days = int(request.form.get("days_per_week") or 3)
                session["days_per_week"] = days
                db.session.commit()
                flash(
                    "Tus preferencias de rutina y nutrición han sido actualizadas exitosamente."
                )
                return redirect(url_for("dashboard"))
            except ValueError:
                flash("Por favor, ingresa los valores correctamente.")

        return render_template(
            "settings.html",
            user=user,
            current_days=session.get("days_per_week", 3),
        )

    @app.route("/tour_complete", methods=["POST"])
    def tour_complete():
        if "user_id" in session:
            u = User.query.get(session["user_id"])
            if u:
                u.tour_completed = True
                db.session.commit()
        return jsonify({"status": "ok"})

    @app.route("/strength_test", methods=["GET", "POST"])
    def strength_test():
        if "user_id" not in session:
            return redirect(url_for("login"))
        user = User.query.get(session["user_id"])

        if request.method == "POST":
            try:
                user.stats.sq_rm = float(request.form.get("sq_rm", 0))
                user.stats.bp_rm = float(request.form.get("bp_rm", 0))
                user.stats.dl_rm = float(request.form.get("dl_rm", 0))
                user.stats.rank = calculate_rank(
                    user.stats.sq_rm,
                    user.stats.bp_rm,
                    user.stats.dl_rm,
                    user.stats.weight,
                )
                db.session.commit()
                flash(
                    "Niveles de fuerza actualizados. Eres rango: "
                    + user.stats.rank
                )
                return redirect(url_for("dashboard"))
            except ValueError:
                flash("Valores inválidos.")

        return render_template("strength_test.html", user=user)

    @app.route("/exercises")
    def exercises():
        if "user_id" not in session:
            return redirect(url_for("login"))
        user = User.query.get(session["user_id"])
        if not user:
            session.clear()
            return redirect(url_for("login"))

        page = request.args.get("page", 1, type=int)
        query = request.args.get("q", "")

        if query:
            exercises_query = Exercise.query.filter(
                Exercise.name.ilike(f"%{query}%")
            ).paginate(page=page, per_page=12, error_out=False)
        else:
            exercises_query = Exercise.query.paginate(
                page=page, per_page=12, error_out=False
            )

        return render_template(
            "exercises.html", user=user, exercises=exercises_query, query=query
        )

    @app.route("/exercise/<int:ex_id>")
    def exercise_detail(ex_id):
        if "user_id" not in session:
            return redirect(url_for("login"))
        user = User.query.get(session["user_id"])
        if not user:
            session.clear()
            return redirect(url_for("login"))

        ex = Exercise.query.get_or_404(ex_id)

        if not ex.instructions_es and ex.instructions:
            try:
                translated = GoogleTranslator(
                    source="en", target="es"
                ).translate(ex.instructions[:2000])
                ex.instructions_es = translated
                db.session.commit()
            except Exception as e:  # pylint: disable=broad-exception-caught
                print("Translation error:", e)
                ex.instructions_es = (
                    "Error en traducción temporal. " + ex.instructions
                )

        if not ex.video_id:
            try:
                search_query = urllib.parse.quote_plus(
                    f"{ex.name} ejercicio tecnica español"
                )
                url = f"https://www.youtube.com/results?search_query={search_query}"
                req = urllib.request.Request(
                    url, headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(req) as html:
                    video_ids = re.findall(
                        r"watch\?v=(\S{11})", html.read().decode()
                    )
                if video_ids:
                    ex.video_id = video_ids[0]
                    db.session.commit()
            except Exception as e:  # pylint: disable=broad-exception-caught
                print("Youtube Scrape Error:", e)

        final_id = (
            ex.video_id if ex.video_id else "YopfdAf1_ac"
        )  # Squat fallback
        video_url = (
            f"https://www.youtube.com/embed/{final_id}?autoplay=1&mute=1"
        )

        return render_template(
            "exercise_detail.html", user=user, ex=ex, video_url=video_url
        )

    @app.route("/chat")
    def chat():
        if "user_id" not in session:
            return redirect(url_for("login"))
        user = User.query.get(session["user_id"])
        return render_template("chat.html", user=user)

    @app.route("/progress")
    def progress():
        if "user_id" not in session:
            return redirect(url_for("login"))
        user = User.query.get(session["user_id"])
        return render_template("progress.html", user=user)

    @app.route("/api/progress", methods=["GET", "POST"])
    def api_progress():
        if "user_id" not in session:
            return jsonify({"error": "Unauthorized"}), 401

        if request.method == "GET":
            logs = WorkoutLog.query.filter_by(user_id=session["user_id"]).all()
            return jsonify(
                [
                    {
                        "id": l.id,
                        "title": "Entrenado",
                        "date": l.date,
                        "color": "#10b981",
                    }
                    for l in logs
                ]
            )

        if request.method == "POST":
            data = request.json
            date_str = data.get("date")
            existing = WorkoutLog.query.filter_by(
                user_id=session["user_id"], date=date_str
            ).first()
            if existing:
                db.session.delete(existing)
            else:
                new_log = WorkoutLog(
                    user_id=session["user_id"],
                    date=date_str,
                    status="completed",
                )
                db.session.add(new_log)
            db.session.commit()
            return jsonify({"status": "success"})

        return jsonify({"error": "Method not allowed"}), 405

    @socketio.on("message")
    def handle_message(data):
        user = User.query.get(session.get("user_id"))
        if user:
            emit(
                "message",
                {"user": user.username, "msg": data["msg"]},
                broadcast=True,
            )
