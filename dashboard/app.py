import json
import os
import sys
import subprocess
from flask import Flask, render_template, jsonify
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)

# Project root is one level up from dashboard/
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

LOG_FILE_PATH = os.path.join(
    PROJECT_ROOT, "log", "fraud_log.json"
)

UPLOAD_FOLDER = os.path.join(
    PROJECT_ROOT, "data", "uploads"
)

APP_FOLDER = os.path.join(
    PROJECT_ROOT, "app"
)

ALLOWED_EXTENSIONS = {"mp4", "avi", "mov", "mkv"}

# Track the running detection process
detection_process = None


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def load_log_data():

    if not os.path.exists(LOG_FILE_PATH):

        return None

    with open(LOG_FILE_PATH, "r") as file:

        data = json.load(file)

    return data


def is_detection_running():

    global detection_process

    if detection_process is None:

        return False

    # Check if process is still running
    poll_result = detection_process.poll()

    if poll_result is None:

        return True

    else:

        detection_process = None

        return False


# ---- ROUTES ----


@app.route("/")
def index():

    running = is_detection_running()

    log_exists = os.path.exists(LOG_FILE_PATH)

    return render_template(
        "index.html",
        running=running,
        log_exists=log_exists,
    )


@app.route("/start", methods=["POST"])
def start_detection():

    global detection_process

    if is_detection_running():

        return redirect(url_for("running"))

    source_type = request.form.get(
        "source_type", "webcam"
    )

    # Build the command to run main.py
    python_exe = sys.executable

    if source_type == "webcam":

        command = [
            python_exe,
            "main.py",
            "webcam",
        ]

    else:

        video_path = request.form.get(
            "video_path", ""
        )

        command = [
            python_exe,
            "main.py",
            "file",
            video_path,
        ]

    print(f"Starting detection: {command}")

    detection_process = subprocess.Popen(
        command,
        cwd=APP_FOLDER,
    )

    return redirect(url_for("running"))


@app.route("/upload", methods=["POST"])
def upload_video():

    if "video_file" not in request.files:

        return redirect(url_for("index"))

    file = request.files["video_file"]

    if file.filename == "":

        return redirect(url_for("index"))

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        if not os.path.exists(UPLOAD_FOLDER):

            os.makedirs(UPLOAD_FOLDER)

        filepath = os.path.join(
            UPLOAD_FOLDER, filename
        )

        file.save(filepath)

        print(f"Video uploaded: {filepath}")

        return render_template(
            "index.html",
            running=False,
            log_exists=os.path.exists(LOG_FILE_PATH),
            uploaded_file=filepath,
            uploaded_name=filename,
        )

    return redirect(url_for("index"))


@app.route("/running")
def running():

    running = is_detection_running()

    return render_template(
        "running.html",
        running=running,
    )


@app.route("/results")
def results():

    data = load_log_data()

    if data is None:

        return render_template(
            "results.html",
            summary=None,
            events=[],
        )

    summary = data.get("summary", {})

    events = data.get("events", [])

    return render_template(
        "results.html",
        summary=summary,
        events=events,
    )


@app.route("/api/events")
def api_events():

    data = load_log_data()

    if data is None:

        return jsonify(
            {"error": "No log file found."}
        )

    return jsonify(data)


if __name__ == "__main__":

    print("=" * 50)
    print("  Fraud Detection Dashboard")
    print("  Open http://localhost:5000")
    print("=" * 50)

    app.run(
        debug=True,
        port=5000,
    )
