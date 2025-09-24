from flask import Flask, request, jsonify, Response
from prometheus_client import Counter, Gauge, generate_latest
from selfheal.prioritizer import Prioritizer

app = Flask(__name__)
prior = Prioritizer()

tests_db = {
    "login_happy": {"recent_failures": 0, "flakiness": 0.05, "code_diff_risk": 0.2},
    "login_negative": {"recent_failures": 1, "flakiness": 0.2, "code_diff_risk": 0.5},
    "checkout_flow": {"recent_failures": 3, "flakiness": 0.4, "code_diff_risk": 0.7},
    "cart_add_remove": {"recent_failures": 0, "flakiness": 0.1, "code_diff_risk": 0.3}
}

MET_SCHEDULED = Counter('autoqa_tests_scheduled_total','Tests scheduled', ['suite'])
GA_FLAKINESS = Gauge('autoqa_flakiness_score','Avg flakiness score')

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/metrics')
def metrics():
    avg_flakiness = sum(v['flakiness'] for v in tests_db.values())/len(tests_db)
    GA_FLAKINESS.set(avg_flakiness)
    return Response(generate_latest(), mimetype='text/plain')

@app.route('/schedule', methods=['POST'])
def schedule():
    body = request.get_json(force=True)
    suite = body.get('suite', 'regression')
    order = prior.order(tests_db)
    MET_SCHEDULED.labels(suite=suite).inc(len(order))
    return jsonify({"suite": suite, "execution_order": order})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
