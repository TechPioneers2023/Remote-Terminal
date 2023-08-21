from flask import Flask, render_template, request
import serial
import time

app = Flask(__name__)

arduino_serial = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
time.sleep(2)  # 等待串行连接稳定

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    
    if request.method == 'POST':
        cmd = request.form.get('command')
        if cmd:
            arduino_serial.write(cmd.encode())
            time.sleep(1)  # 等待Arduino响应
            if arduino_serial.inWaiting() > 0:
                response = arduino_serial.readline().decode().strip()

    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
