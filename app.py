#Main file

from functools import wraps
from random import sample

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
import app_utils

# Import the database tables from models.py.
from models import db, User, Category, Question, Attempt
# Import the starter categories and questions.
from seed_data import add_sample_data

app = Flask(__name__)

CATEGORY_DETAILS = {
    "Anime": {"icon": "🎌", "description": "From shonen heroes to Studio Ghibli favorites."},
    "Video Games": {"icon": "🎮", "description": "Games, characters, consoles, and classic gaming facts."},
    "Movies & TV": {"icon": "🎬", "description": "Popular movies, shows, characters, and memorable moments."},
    "Music": {"icon": "🎵", "description": "Artists, songs, instruments, albums, and music basics."},
    "Internet Culture": {"icon": "💻", "description": "Memes, platforms, online terms, and digital life."},
}

RANDOM_CATEGORY_NAME = "Random Mix"

app.config["SECRET_KEY"] = "change-this-before-deployment"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trivia.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

#Track what user is logged in
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# datetime -> 3 hours ago
@app.template_filter("time_ago")
def time_ago_filter(dt):
    return app_utils.time_ago(dt)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def admin_required(view_function):
    #Protects admin only pages
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        #Send visitors to login if they are not signed in
        if not current_user.is_authenticated:
            return login_manager.unauthorized()

        #Regular users cannot open admin pages.
        if not current_user.is_admin:
            flash("Admin access is required for that page.")
            return redirect(url_for("home"))

        return view_function(*args, **kwargs)

    return wrapped_view


#Home page.
@app.route("/")
def home():
    return render_template("home.html")


#Register a new player account.
@app.route("/register", methods=["GET", "POST"])
def register():
    #Do not show registration to users who are already logged in
    if current_user.is_authenticated:
        return redirect(url_for("categories"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please fill in every field.")
        elif User.query.filter_by(username=username).first():
            flash("That username is already taken.")
        else:
            #Hashing passwords
            new_user = User(
                username=username,
                password_hash=generate_password_hash(password),
                is_admin=False,
            )
            db.session.add(new_user)
            db.session.commit()

            #Log in the new player
            login_user(new_user)
            return redirect(url_for("categories"))

    return render_template("register.html")


#Log an existing player into the site.
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("categories"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        #Look for a user with this username.
        user = User.query.filter_by(username=username).first()

        #Checks entered password compared to hash
        if user and check_password_hash(user.password_hash, password):
            login_user(user)

            #Send admin to admin page
            if user.is_admin:
                return redirect(url_for("admin_questions"))

            return redirect(url_for("categories"))

        flash("Incorrect username or password.")

    return render_template("login.html")


#Log out the current user
@app.route("/logout")
@login_required
def logout():
    logout_user()
    # Remove any quiz information that was temporarily stored in the session.
    clear_quiz_session()
    return redirect(url_for("home"))

# Upload or delete a profile picture for the current user
@app.route("/profile-picture", methods=["POST"])
@login_required
def profile_picture():
    if "upload" in request.form:
        file = request.files.get("profile_pic")
        if not file or file.filename == "":
            flash("No file selected.")
            return redirect(url_for("profile"))

        app_utils.validate_save_pfp(file.stream, str(current_user.id))
        flash("Profile picture uploaded.")
    elif "delete" in request.form:
        app_utils.delete_pfp(str(current_user.id))
        flash("Profile picture deleted.")
    return redirect(url_for("profile"))


#Show trivia categories
@app.route("/categories")
@login_required
def categories():
    # Do not show the saved Random Mix category as a normal category card.
    all_categories = Category.query.filter(Category.name != RANDOM_CATEGORY_NAME).order_by(Category.name).all()
    return render_template(
        "categories.html",
        categories=all_categories,
        category_details=CATEGORY_DETAILS,
    )


def save_quiz_to_session(selected_questions, category_id, is_random_quiz=False):
    # Store the selected question IDs and the score information for the current quiz.
    session["question_ids"] = [question.id for question in selected_questions]
    session["question_index"] = 0
    session["quiz_score"] = 0
    session["category_id"] = category_id
    session["is_random_quiz"] = is_random_quiz


# Starts a new quiz from one category.
@app.route("/start/<int:category_id>")
@login_required
def start_quiz(category_id):
    category = db.session.get(Category, category_id)
    questions = Question.query.filter_by(category_id=category_id).all()

    # The quiz needs at least 15 questions to work.
    if not category or category.name == RANDOM_CATEGORY_NAME or len(questions) < 15:
        flash("This category does not have enough questions for a 15-question quiz.")
        return redirect(url_for("categories"))

    # Choose 15 random questions from this category.
    selected = sample(questions, 15)
    save_quiz_to_session(selected, category.id)

    return redirect(url_for("quiz"))


# Starts a mixed quiz using questions from every regular category.
@app.route("/start-random")
@login_required
def start_random_quiz():
    random_category = Category.query.filter_by(name=RANDOM_CATEGORY_NAME).first()
    regular_categories = Category.query.filter(Category.name != RANDOM_CATEGORY_NAME).all()
    regular_category_ids = [category.id for category in regular_categories]
    questions = Question.query.filter(Question.category_id.in_(regular_category_ids)).all()

    if not random_category or len(questions) < 15:
        flash("There are not enough questions for a random quiz yet.")
        return redirect(url_for("categories"))

    # Pick from all regular categories, not just one topic.
    selected = sample(questions, 15)
    save_quiz_to_session(selected, random_category.id, is_random_quiz=True)

    return redirect(url_for("quiz"))


#Show the current quiz question
@app.route("/quiz")
@login_required
def quiz():
    question_ids = session.get("question_ids")
    question_index = session.get("question_index")

    #If there is no quiz in progress, return to categories
    if not question_ids or question_index is None:
        return redirect(url_for("categories"))

    #Move to the results page when the player has answered all questions.
    if question_index >= len(question_ids):
        return redirect(url_for("finish_quiz"))

    #Get the current question and category from db
    question = db.session.get(Question, question_ids[question_index])
    category = db.session.get(Category, session["category_id"])

    return render_template(
        "quiz.html",
        question=question,
        category=category,
        question_number=question_index + 1,
        total_questions=len(question_ids),
        score=session["quiz_score"],
    )


#Receive the answer submitted from the quiz page
@app.route("/answer", methods=["POST"])
@login_required
def answer():
    question_ids = session.get("question_ids")
    question_index = session.get("question_index")

    if not question_ids or question_index is None:
        return redirect(url_for("categories"))

    #Find the current question and the answer letter selected by the player.
    question = db.session.get(Question, question_ids[question_index])
    chosen_answer = request.form.get("answer", "")

    #The browser sends the number of seconds still left on the timer.
    # A player gets more points when they answer a question faster.
    seconds_left = request.form.get("seconds_left", "0")

    try:
        seconds_left = int(seconds_left)
    except ValueError:
        seconds_left = 0

    # Keep the timer value between 0 and 15.
    seconds_left = max(0, min(seconds_left, 15))

    #Wrong answers and timeouts get 0 points.
    #Correct answers get 100 base points plus 5 points for every second left.
    is_correct = chosen_answer == question.correct_answer
    points_earned = 0

    if is_correct:
        points_earned = 100 + (seconds_left * 5)
        session["quiz_score"] += points_earned

    # Save answer feedback so the player can see whether the answer was correct.
    session["answer_feedback"] = {
        "question_id": question.id,
        "chosen_answer": chosen_answer,
        "is_correct": is_correct,
        "points_earned": points_earned,
        "timed_out": chosen_answer == "",
    }

    #Move to the feedback page before showing the next question.
    session["question_index"] += 1
    return redirect(url_for("answer_feedback"))


# Show whether the last answer was correct before continuing the quiz.
@app.route("/feedback")
@login_required
def answer_feedback():
    feedback = session.get("answer_feedback")

    if not feedback:
        return redirect(url_for("quiz"))

    question = db.session.get(Question, feedback["question_id"])
    correct_answer_text = getattr(question, "option_" + question.correct_answer.lower())
    return render_template(
        "feedback.html",
        feedback=feedback,
        question=question,
        correct_answer_text=correct_answer_text,
    )


# Continue from the feedback page to the next question.
@app.route("/next-question", methods=["POST"])
@login_required
def next_question():
    session.pop("answer_feedback", None)
    return redirect(url_for("quiz"))


# Save the completed quiz score in the db
@app.route("/finish")
@login_required
def finish_quiz():
    category_id = session.get("category_id")
    score = session.get("quiz_score")

    if category_id is None or score is None:
        return redirect(url_for("categories"))

    #Creates a record so the score appears in the profile and leaderboard
    new_attempt = Attempt(
        user_id=current_user.id,
        category_id=category_id,
        score=score,
    )
    db.session.add(new_attempt)
    db.session.commit()

    category = db.session.get(Category, category_id)
    is_random_quiz = session.get("is_random_quiz", False)
    clear_quiz_session()
    return render_template(
        "results.html",
        score=score,
        category=category,
        is_random_quiz=is_random_quiz,
    )


# Build the statistics used on both a player's own profile and public player profiles.
def get_profile_data(profile_user):
    # Get this player's newest quiz attempts first.
    attempts = Attempt.query.filter_by(user_id=profile_user.id).order_by(Attempt.completed_at.desc()).all()

    # Simple profile statistics calculated from the saved attempts.
    total_quizzes = len(attempts)
    total_score = sum(attempt.score for attempt in attempts)
    best_score = max((attempt.score for attempt in attempts), default=0)
    average_score = round(total_score / total_quizzes) if total_quizzes else 0

    # Count how often the player has completed each category.
    category_counts = {}
    for attempt in attempts:
        category_name = attempt.category.name
        category_counts[category_name] = category_counts.get(category_name, 0) + 1

    # The most played category becomes the player's favorite category.
    favorite_category = "No quizzes yet"
    if category_counts:
        favorite_category = max(category_counts, key=category_counts.get)

    # Find the player's best Random Mix score if they have played that category.
    random_mix_best = 0
    for attempt in attempts:
        if attempt.category.name == RANDOM_CATEGORY_NAME and attempt.score > random_mix_best:
            random_mix_best = attempt.score

    return {
        "attempts": attempts,
        "total_quizzes": total_quizzes,
        "total_score": total_score,
        "best_score": best_score,
        "average_score": average_score,
        "favorite_category": favorite_category,
        "random_mix_best": random_mix_best,
    }


# Show saved quiz scores and simple statistics for the logged-in player.
@app.route("/profile")
@login_required
def profile():
    profile_data = get_profile_data(current_user)
    return render_template("profile.html", profile_user=current_user, **profile_data)


# Lets logged-in players view another player's public quiz statistics.
@app.route("/profile/<username>")
@login_required
def public_profile(username):
    profile_user = User.query.filter_by(username=username).first()

    if not profile_user:
        abort(404)

    # Send a player back to their normal profile page when viewing their own name.
    if profile_user.id == current_user.id:
        return redirect(url_for("profile"))

    profile_data = get_profile_data(profile_user)
    return render_template("profile.html", profile_user=profile_user, **profile_data)


#Show the top ten scores for all users or one selected category.
@app.route("/leaderboard")
def leaderboard():
    all_categories = Category.query.order_by(Category.name).all()
    selected_category_id = request.args.get("category_id", type=int)
    selected_category = None

    query = Attempt.query

    if selected_category_id:
        selected_category = db.session.get(Category, selected_category_id)

        if selected_category:
            query = query.filter_by(category_id=selected_category.id)
        else:
            selected_category_id = None

    attempts = query.order_by(Attempt.score.desc()).limit(10).all()
    return render_template(
        "leaderboard.html",
        attempts=attempts,
        categories=all_categories,
        selected_category_id=selected_category_id,
        selected_category=selected_category,
    )

# Admin question pages
# -----------------------

# List questions in separate category sections so the admin can manage one category at a time.
@app.route("/admin")
@admin_required
def admin_questions():
    all_categories = Category.query.order_by(Category.name).all()
    questions_by_category = {}

    for category in all_categories:
        questions_by_category[category.id] = Question.query.filter_by(category_id=category.id).order_by(Question.id).all()

    return render_template(
        "admin_questions.html",
        categories=all_categories,
        questions_by_category=questions_by_category,
    )

# Adds a new trivia question.
@app.route("/admin/add", methods=["GET", "POST"])
@admin_required
def admin_add_question():
    categories = Category.query.order_by(Category.name).all()

    if request.method == "POST":
        # Read the form values and make a Question object.
        new_question = get_question_from_form()

        if new_question is None:
            flash("Please fill in every question field and choose A, B, C, or D.")
        else:
            db.session.add(new_question)
            db.session.commit()
            flash("Question added.")
            return redirect(url_for("admin_questions"))

    return render_template("admin_question_form.html", categories=categories, question=None)


#Edit an existing question
@app.route("/admin/edit/<int:question_id>", methods=["GET", "POST"])
@admin_required
def admin_edit_question(question_id):
    question = db.session.get(Question, question_id)
    if not question:
        abort(404)

    categories = Category.query.order_by(Category.name).all()

    if request.method == "POST":
        # Make a temporary Question object from the new form information.
        updated_question = get_question_from_form()

        if updated_question is None:
            flash("Please fill in every question field and choose A, B, C, or D.")
        else:
            # Copy the new values into the existing database row.
            question.category_id = updated_question.category_id
            question.question_text = updated_question.question_text
            question.option_a = updated_question.option_a
            question.option_b = updated_question.option_b
            question.option_c = updated_question.option_c
            question.option_d = updated_question.option_d
            question.correct_answer = updated_question.correct_answer
            db.session.commit()
            flash("Question updated.")
            return redirect(url_for("admin_questions"))

    return render_template("admin_question_form.html", categories=categories, question=question)


#Delete a question from the database
@app.route("/admin/delete/<int:question_id>", methods=["POST"])
@admin_required
def admin_delete_question(question_id):
    question = db.session.get(Question, question_id)
    if not question:
        abort(404)

    db.session.delete(question)
    db.session.commit()
    flash("Question deleted.")
    return redirect(url_for("admin_questions"))


def get_question_from_form():
    #Read the add/edit question form
    #Return a Question object when valid, otherwise return None
    category_id = request.form.get("category_id", "")
    question_text = request.form.get("question_text", "").strip()
    option_a = request.form.get("option_a", "").strip()
    option_b = request.form.get("option_b", "").strip()
    option_c = request.form.get("option_c", "").strip()
    option_d = request.form.get("option_d", "").strip()
    correct_answer = request.form.get("correct_answer", "").upper().strip()

    #Make sure each required field has a value
    if (
        not category_id
        or not question_text
        or not option_a
        or not option_b
        or not option_c
        or not option_d
        or correct_answer not in {"A", "B", "C", "D"}
    ):
        return None

    return Question(
        category_id=int(category_id),
        question_text=question_text,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        correct_answer=correct_answer,
    )


def clear_quiz_session():
    # Remove the temporary quiz values after a game ends or a user logs out.
    session.pop("question_ids", None)
    session.pop("question_index", None)
    session.pop("quiz_score", None)
    session.pop("category_id", None)
    session.pop("is_random_quiz", None)
    session.pop("answer_feedback", None)


def create_admin_account():
    # Create the starter admin account only if it does not already exist.
    existing_admin = User.query.filter_by(username="admin").first()

    if not existing_admin:
        admin_user = User(
            username="admin",
            password_hash=generate_password_hash("admin123"),
            is_admin=True,
        )
        db.session.add(admin_user)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        add_sample_data()
        create_admin_account()
    app.run(debug=True)
