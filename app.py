from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = "change-this-secret-key-before-deployment"
DATABASE = "construction.db"

# Demo login: admin / balaji123
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "balaji123"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def setup_database():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            project_type TEXT,
            location TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            project_type TEXT,
            location TEXT,
            status TEXT DEFAULT 'Planning',
            description TEXT
        )
    """)

    project_count = connection.execute(
        "SELECT COUNT(*) FROM projects"
    ).fetchone()[0]

    if project_count == 0:
        sample_projects = [
            ("Balaji Residence", "Residential", "Tirupati", "In Progress",
             "Sample residential project. Replace this with real project details."),
            ("Sri Balaji Commercial Space", "Commercial", "Puttur", "Planning",
             "Sample commercial project for demonstration.")
        ]
        connection.executemany("""
            INSERT INTO projects (name, project_type, location, status, description)
            VALUES (?, ?, ?, ?, ?)
        """, sample_projects)

    connection.commit()
    connection.close()


def admin_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("login"))
        return view_function(*args, **kwargs)
    return wrapped_view


@app.route("/")
def home():
    connection = get_db()
    projects = connection.execute(
        "SELECT * FROM projects ORDER BY id DESC LIMIT 3"
    ).fetchall()
    connection.close()
    return render_template("index.html", projects=projects)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/projects")
def projects_page():
    connection = get_db()
    projects = connection.execute(
        "SELECT * FROM projects ORDER BY id DESC"
    ).fetchall()
    connection.close()
    return render_template("projects.html", projects=projects)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        project_type = request.form.get("project_type", "").strip()
        location = request.form.get("location", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not phone:
            flash("Please enter your name and phone number.", "error")
            return redirect(url_for("contact"))

        connection = get_db()
        connection.execute("""
            INSERT INTO enquiries (name, phone, email, project_type, location, message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, phone, email, project_type, location, message))
        connection.commit()
        connection.close()

        flash("Thank you! Your enquiry has been submitted.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("dashboard"))

        flash("Incorrect username or password.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/admin")
@admin_required
def dashboard():
    connection = get_db()
    enquiries = connection.execute(
        "SELECT * FROM enquiries ORDER BY id DESC"
    ).fetchall()
    projects = connection.execute(
        "SELECT * FROM projects ORDER BY id DESC"
    ).fetchall()
    enquiry_count = connection.execute(
        "SELECT COUNT(*) FROM enquiries"
    ).fetchone()[0]
    project_count = connection.execute(
        "SELECT COUNT(*) FROM projects"
    ).fetchone()[0]
    connection.close()

    return render_template(
        "dashboard.html",
        enquiries=enquiries,
        projects=projects,
        enquiry_count=enquiry_count,
        project_count=project_count
    )


@app.route("/admin/projects/add", methods=["POST"])
@admin_required
def add_project():
    name = request.form.get("name", "").strip()
    project_type = request.form.get("project_type", "").strip()
    location = request.form.get("location", "").strip()
    status = request.form.get("status", "Planning").strip()
    description = request.form.get("description", "").strip()

    if name:
        connection = get_db()
        connection.execute("""
            INSERT INTO projects (name, project_type, location, status, description)
            VALUES (?, ?, ?, ?, ?)
        """, (name, project_type, location, status, description))
        connection.commit()
        connection.close()
        flash("Project added successfully.", "success")
    else:
        flash("Project name is required.", "error")

    return redirect(url_for("dashboard"))


@app.route("/admin/projects/delete/<int:project_id>", methods=["POST"])
@admin_required
def delete_project(project_id):
    connection = get_db()
    connection.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    connection.commit()
    connection.close()
    flash("Project deleted.", "success")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    setup_database()
    app.run(debug=True)
