from flask import Flask, render_template, jsonify

app = Flask(__name__)

TITLE = "Equipment Failure Monitor"
PROCESS = "P2M"

KPIS = [
    ("Machines Affected", "18"),
    ("Downtime", "26 hrs"),
    ("OEE", "78%")
]

DATA = [
    {
        "id": "M-101",
        "entity": "Press Machine 1",
        "value": 1850,
        "issue": "Repeated motor failure",
        "status": "red"
    },
    {
        "id": "M-102",
        "entity": "Cutter Machine 2",
        "value": 920,
        "issue": "Sensor fault",
        "status": "yellow"
    },
    {
        "id": "M-103",
        "entity": "Assembly Line 3",
        "value": 430,
        "issue": "Minor temperature variation",
        "status": "green"
    }
]


def analyse(machine):

    if machine["status"] == "red":
        return (
            "High-risk failure pattern detected. "
            "Repeated motor failures are causing significant downtime. "
            "Prioritise preventive maintenance and inspect the motor."
        )

    if machine["status"] == "yellow":
        return (
            "Manual review recommended. "
            "Sensor-related downtime is moderate. "
            "Inspect the sensor before the next production cycle."
        )

    return (
        "Low-risk condition. "
        "Temperature variation is within an acceptable range. "
        "Continue monitoring during production."
    )


@app.route("/")
def home():
    return render_template(
        "index.html",
        title=TITLE,
        process=PROCESS,
        kpis=KPIS,
        data=DATA
    )


@app.route("/analyse/<id>")
def get_analysis(id):

    machine = next((x for x in DATA if x["id"] == id), None)

    if not machine:
        return jsonify({"error": "Machine not found"}), 404

    return jsonify({
        "text": analyse(machine)
    })


@app.route("/action/<id>", methods=["POST"])
def action(id):

    machine = next((x for x in DATA if x["id"] == id), None)

    if not machine:
        return jsonify({"message": "Machine not found"}), 404

    if machine["status"] == "red":
        return jsonify({
            "message":
            "ACTION REQUIRED — Schedule maintenance and inspect the failure."
        })

    if machine["status"] == "yellow":
        return jsonify({
            "message":
            "MANUAL REVIEW — Inspect the sensor before production."
        })

    return jsonify({
        "message":
        "MONITOR — Machine can continue operating with observation."
    })


if __name__ == "__main__":
    app.run(debug=True)
