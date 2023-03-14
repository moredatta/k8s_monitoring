from flask import Response, Flask, request
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import time
import datetime
import requests


app = Flask(__name__)

_INF = float("inf")

graphs = {}
graphs['c'] = Counter('python_request_operations_total', 'The total number of processed request')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets=(1, 2, 5, 6, 10, _INF))


@app.route("/")
def hello():
    timestamp = datetime.datetime.now().ctime()
    # request_data = request.headers
    #extra = {"Timestamp":timestamp,"Method":request.method,"RequestPath":request.full_path,"Host":request.host,"RequestID":request.get_json()["RequestID"],"ServiceName":"Hello_World2-Service"}
    start = time.time()
    graphs['c'].inc()
    
    time.sleep(5)
    end = time.time()
    graphs['h'].observe(end - start)
    # print(type(request_data))
    #requests.post(url="http://logger-service:9050/",json={"Data":extra})
    return "Hello World2!"

@app.route("/metrics")
def requests_count():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")



if __name__=='__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
