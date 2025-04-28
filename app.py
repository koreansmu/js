from flask import Flask, request, send_file, jsonify
from utils import setup_logging, get_env_var
from jobs import queue_download
from loguru import logger
import os
from dotenv import load_dotenv
import time

load_dotenv()
setup_logging()

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "YouTube Audio Downloader API Powered By @BillaSpace"}), 200

@app.route("/download-audio/<video_id>", methods=["GET"])
def download(video_id):
    proxy = get_env_var("SOCKS5_PROXY", "")
    file_path = f"downloads/{video_id}.mp3"

    if os.path.exists(file_path):
        logger.info(f"File already exists: {file_path}")
        return send_file(file_path, as_attachment=True)

    logger.info(f"File not found. Queueing download for: {video_id}")
    queue_download(video_id, proxy)
    return jsonify({
        "status": "queued",
        "message": "Download started in background. Retry this endpoint after a few seconds.",
        "video_id": video_id
    }), 202

@app.errorhandler(404)
def not_found(e):
    logger.warning(f"404 Not Found: {request.path}")
    return jsonify({"error": "Endpoint not found", "path": request.path}), 404

@app.errorhandler(Exception)
def global_error_handler(e):
    logger.error(f"Unhandled error: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    host = get_env_var("FLASK_HOST", "127.0.0.1")
    port = int(get_env_var("FLASK_PORT", 5000))
    app.run(host=host, port=port)
