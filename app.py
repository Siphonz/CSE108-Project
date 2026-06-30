#Main file

from functools import wraps
from random import sample

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database tables from models.py.
from models import db, User, Category, Question, Attempt
# Import the starter categories and questions.
from seed_data import add_sample_data

app = Flask(__name__)

app.config["SECRET_KEY"] = "change-this-before-deployment"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trivia.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

DIFFICULTY_LEVELS = ["easy", "medium", "hard"]

db.init_app(app)

#Track what user is logged in
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


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


#Show trivia categories
@app.route("/categories")
@login_required
def categories():
    all_categories = Category.query.order_by(Category.name).all()
    return render_template("categories.html", categories=all_categories, difficulties=DIFFICULTY_LEVELS)


#Starts a new quiz from one category and one difficulty
@app.route("/start/<int:category_id>/<difficulty>")
@login_required
def start_quiz(category_id, difficulty):
    difficulty = difficulty.lower().strip()
    if difficulty not in DIFFICULTY_LEVELS:
        flash("Please choose a valid difficulty.")
        return redirect(url_for("categories"))

    category = db.session.get(Category, category_id)
    questions = Question.query.filter_by(category_id=category_id, difficulty=difficulty).all()

    # The quiz needs at least five questions to work
    if not category or len(questions) < 5:
        flash(f"This category does not have enough {difficulty.title()} questions.")
        return redirect(url_for("categories"))

    # Choose five random questions from this category
    selected = sample(questions, 5)

    #Store IDs of quiz information
    session["question_ids"] = [question.id for question in selected]
    session["question_index"] = 0
    session["quiz_score"] = 0
    session["category_id"] = category.id
    session["difficulty"] = difficulty

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
    difficulty = session.get("difficulty", "easy")

    return render_template(
        "quiz.html",
        question=question,
        category=category,
        difficulty=difficulty,
        question_number=question_index + 1,
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
    if chosen_answer == question.correct_answer:
        points_earned = 100 + (seconds_left * 5)
        session["quiz_score"] += points_earned

    #Moves to the next question
    session["question_index"] += 1
    return redirect(url_for("quiz"))


# Save the completed quiz score in the db
@app.route("/finish")
@login_required
def finish_quiz():
    category_id = session.get("category_id")
    score = session.get("quiz_score")
    difficulty = session.get("difficulty", "easy")

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
    clear_quiz_session()
    return render_template("results.html", score=score, category=category, difficulty=difficulty)


#Show past quiz scores for the logged-in player
@app.route("/profile")
@login_required
def profile():
    attempts = Attempt.query.filter_by(user_id=current_user.id).order_by(Attempt.completed_at.desc()).all()
    return render_template("profile.html", attempts=attempts)


#Show the top ten scores for all users
@app.route("/leaderboard")
def leaderboard():
    attempts = Attempt.query.order_by(Attempt.score.desc()).limit(10).all()
    return render_template("leaderboard.html", attempts=attempts)

# Admin question pages
# -----------------------

# List every question so the admin can edit or delete them.
@app.route("/admin")
@admin_required
def admin_questions():
    all_questions = Question.query.order_by(Question.category_id, Question.difficulty, Question.id).all()
    all_categories = Category.query.order_by(Category.name).all()
    return render_template(
        "admin_questions.html",
        questions=all_questions,
        categories=all_categories,
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
            flash("Please fill in every question field, choose a difficulty, and choose A, B, C, or D.")
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
            flash("Please fill in every question field, choose a difficulty, and choose A, B, C, or D.")
        else:
            # Copy the new values into the existing database row.
            question.category_id = updated_question.category_id
            question.question_text = updated_question.question_text
            question.option_a = updated_question.option_a
            question.option_b = updated_question.option_b
            question.option_c = updated_question.option_c
            question.option_d = updated_question.option_d
            question.correct_answer = updated_question.correct_answer
            question.difficulty = updated_question.difficulty
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
    difficulty = request.form.get("difficulty", "").lower().strip()
    question_text = request.form.get("question_text", "").strip()
    option_a = request.form.get("option_a", "").strip()
    option_b = request.form.get("option_b", "").strip()
    option_c = request.form.get("option_c", "").strip()
    option_d = request.form.get("option_d", "").strip()
    correct_answer = request.form.get("correct_answer", "").upper().strip()

    #Make sure each required field has a value
    if (
        not category_id
        or difficulty not in DIFFICULTY_LEVELS
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
        difficulty=difficulty,
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
    session.pop("difficulty", None)


def ensure_question_difficulty_column():
    # Add the difficulty column for older databases created before this feature.
    table_info = db.session.execute(text("PRAGMA table_info(question)")).fetchall()
    column_names = [column[1] for column in table_info]

    if "difficulty" not in column_names:
        db.session.execute(
            text("ALTER TABLE question ADD COLUMN difficulty TEXT NOT NULL DEFAULT 'easy'")
        )
        db.session.commit()


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
        ensure_question_difficulty_column()
        add_sample_data()
        create_admin_account()
    app.run(debug=True)
