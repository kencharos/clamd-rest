import os
import logging
import sys
import timeit

from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth

import clamd

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger("clamd-rest")

app = Flask("clamd-rest")

auth = HTTPBasicAuth()

auth_user = os.environ.get("AUTH_USER")
auth_password = os.environ.get("AUTH_PASSWORD")

clamd_client = clamd.ClamdUnixSocket(path="/run/clamav/clamd.sock")

@auth.verify_password
def verify_password(username, password):

    if username == auth_user and password == auth_password:
        return True
    else:
        return False

@app.route("/", methods=["GET"])
def healthcheck():

    try:
        clamd_client.ping()
        return "OK"
    except clamd.ConnectionError:
        return "NG", 500

@app.route("/scan", methods=["POST"])
@auth.login_required
def scan_v2():

    if len(request.files) != 1:
        return "Provide a single file", 400

    _, file_data = list(request.files.items())[0]

    start_time = timeit.default_timer()
    resp = clamd_client.instream(file_data)
    elapsed = timeit.default_timer() - start_time

    status, reason = resp["stream"]

    response = {
        'valid': status == "OK",
        'reason': reason,
        'time': elapsed
    }

    logger.info("Scan for  {file_name} complete. Took: {elapsed}. valid file?: {status}, reason: {reason}".format(
        file_name=file_data.filename,
        elapsed=elapsed,
        status=status,
        reason=reason
    ))

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")