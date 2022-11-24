import logging
from flask import Flask, request

app = Flask(__name__)

@app.route("/",methods=['POST'])
def logger():
    logging.getLogger('werkzeug').disabled = True
    logging.basicConfig(filename='./logger/prom.log', filemode='a', format="%(message)s",level=logging.INFO)
    logs = request.get_json()["Data"]
    logging.info(f"{logs}")
    return "Log Insrted"

if __name__=='__main__':
    import logging
    app.run(host='0.0.0.0', port=9050, debug=True)