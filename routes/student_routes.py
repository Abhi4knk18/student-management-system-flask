from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import student_model as db

student_bp = Blueprint("student", __name__)

# ---------- HOME (PUBLIC) ----------
@student_bp.route("/")
def home():
    return render_template("home.html")


# ---------- DASHBOARD (ADMIN + USER) ----------
@student_bp.route("/dashboard", methods=["GET", "POST"])
def index():
    # 🔐 Auth check
    if "user" not in session:
        return redirect(url_for("auth.login"))

    # ---------- ADMIN-ONLY WRITE ACTIONS ----------
    if request.method == "POST":
        if session.get("role") != "admin":
            flash("Access denied", "error")
            return redirect(url_for("student.index"))

        name = request.form["name"]
        roll = request.form["roll"]
        branch = request.form["branch"]

        # ✅ NEW (SAFE): attendance with fallback
        attendance = int(request.form.get("attendance", 0))

        if request.form.get("is_edit") == "1":
            # 🔁 extended but not breaking
            db.update_student(name, roll, branch, attendance)
            flash("Student updated successfully", "success")
        else:
            if db.add_student(name, roll, branch):
                flash("Student added successfully", "success")
            else:
                flash("Roll already exists", "error")

        return redirect(url_for("student.index"))

    # ---------- READ (ADMIN + USER) ----------
    search = request.args.get("search", "").lower()
    branch_filter = request.args.get("branch", "ALL")

    students = db.fetch_students()  # now includes attendance

    if search:
        students = [
            s for s in students
            if search in s[0].lower()
            or search in s[1].lower()
            or search in s[2].lower()
        ]

    if branch_filter != "ALL":
        students = [s for s in students if s[2] == branch_filter]

    branches = sorted({s[2] for s in db.fetch_students()})

    # 📊 DASHBOARD STATS
    total_students = len(students)
    total_branches = len(set(s[2] for s in students))

    return render_template(
        "index.html",
        students=students,
        edit_student=None,
        branches=branches,
        total_students=total_students,
        total_branches=total_branches
    )


# ---------- STUDENT DETAIL (VIEW ONLY) ----------
@student_bp.route("/student/<roll>")
def student_detail(roll):
    if "user" not in session:
        return redirect(url_for("auth.login"))

    student = db.get_student(roll)
    if not student:
        flash("Student not found", "error")
        return redirect(url_for("student.index"))

    return render_template("student_detail.html", student=student)


# ---------- EDIT (ADMIN ONLY) ----------
@student_bp.route("/edit/<roll>")
def edit(roll):
    if "user" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        flash("Access denied", "error")
        return redirect(url_for("student.index"))

    students = db.fetch_students()
    edit_student = db.get_student(roll)
    branches = sorted({s[2] for s in students})

    total_students = len(students)
    total_branches = len(set(s[2] for s in students))

    return render_template(
        "index.html",
        students=students,
        edit_student=edit_student,
        branches=branches,
        total_students=total_students,
        total_branches=total_branches
    )


# ---------- DELETE (ADMIN ONLY) ----------
@student_bp.route("/delete/<roll>")
def delete(roll):
    if "user" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        flash("Access denied", "error")
        return redirect(url_for("student.index"))

    db.delete_student(roll)
    flash("Student deleted successfully", "success")
    return redirect(url_for("student.index"))
