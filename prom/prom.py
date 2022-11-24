from flask import Response, Flask, request
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter,  Gauge
import time
import shortuuid
import datetime
import requests

app = Flask(__name__)

_INF = float("inf")

# METRIC_REQUESTS = Counter('requests','Requests',['endpoint','method'])

graphs = {}
graphs["REQUEST_COUNT"] = Counter('Hello_World_Request_count', 'App_Request_Total_Count',['endpoint','method','service_name'])
graphs["SUCCESSFUL_REQUEST_COUNT"] = Counter('Hello_World_Success_count', 'Total_Successfull_Requests',['endpoint','method','service_name'])
graphs["FAILURE_REQUEST_COUNT"] = Counter('Hello_World_Failure_count', 'Total_Failed_Requests',['endpoint','method','service_name'])

graphs["INPROCESS_REQUESTS"] = Gauge("Hello_world_inprocess_request","No_of_requests_inprogress")
graphs["LAST_SERVED_REQUEST_TIME"] = Gauge("Hello_world_request_served_last_time","when_was_last_request_served")

graphs["LATENCY"] = Summary("Latency","Time_Taken_To_Complete_Request")

# graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets=(1, 2, 5, 6, 10, _INF))
ipr = graphs["INPROCESS_REQUESTS"].track_inprogress()

@app.route("/")
@ipr
def hello():
    start = time.time()
    # graphs["INPROCESS_REQUESTS"].inc()
    request_id = shortuuid.uuid()
    timestamp = datetime.datetime.now().ctime()
    method = request.method
    endpoint = request.endpoint
    service_name = "hello1"
    # request_data = request.headers
    # extra = {"Timestamp":timestamp,"Method":request.method,"RequestPath":request.full_path,"Host":request.host,"RequestID":request_id,"ServiceName":"Hello_World-Service"}
    
    graphs["REQUEST_COUNT"].labels(endpoint,method,service_name).inc()

    time.sleep(5)
    end = time.time()
    total_time = end-start
    graphs["LATENCY"].observe(total_time)
    # graphs["INPROCESS_REQUESTS"].dec()
    graphs["LAST_SERVED_REQUEST_TIME"].set_to_current_time()
    # graphs['h'].observe(end - start)
    # print(type(request_data))
    #requests.post(url="http://logger-service:9050/")
    # requests.post(url="http://192.168.31.128:9050/",json={"Data":{"INFO":extra}})
    try:
        # requests.get(url="http://prom2-service:7000/",json={"RequestID":request_id})
        requests.get(url="http://192.168.59.102:30800/",json={"RequestID":request_id})
        graphs["SUCCESSFUL_REQUEST_COUNT"].labels(endpoint,method,service_name).inc()

    except Exception as Argument:
        graphs["FAILURE_REQUEST_COUNT"].labels(endpoint,method,service_name).inc()
        # requests.post(url="http://192.168.31.128:9050/",json={"Data":{"ERROR":str(Argument),"RequestID":request_id}})
        # SUCCESSFUL_REQUEST_COUNT.labels(endpoint,method,service_name).inc()
    return "Hello World!"

@app.route("/metrics")
def requests_count():
    res = []
    for v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")



if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
