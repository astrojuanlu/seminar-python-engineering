import os

from flask import Flask, request

from rcs import rcs_switch_off, is_consistent, edm_altitude

PORT = int(os.environ["PORT"])
COLORS = {
    "GREEN": "#22bb00",
    "RED": "#ff0000",
}

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, world!"


@app.route("/rcs_off")
def rcs_off():
    rda_range = float(request.args["rda_range"])
    pitch = float(request.args["pitch"])
    vertical_velocity = float(request.args["velocity"])

    try:
        is_rcs_off = rcs_switch_off(rda_range, pitch, vertical_velocity)
    except:
        return "Invalid altitude", 400
    altitude = edm_altitude(rda_range, pitch)
    consistent = is_consistent(rda_range, pitch)
    color = COLORS["GREEN"] if consistent else COLORS["RED"]

    return f"""<b>Altitude</b>: {altitude:.3f} m
<b>Velocity</b>: {vertical_velocity:.3f} m/s
<b>RCS status</b>: {'OFF' if is_rcs_off else 'ON'}
<b>Consistent sensor</b>: <span style='color: {color}'><b>{'YES' if consistent else 'NO'}</b></span>
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
