import os
from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    script_path = 'cfu_counting_filter_dbscan.py'
    
    # Use subprocess to run the script
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    
    if result.returncode == 0:
        output = result.stdout
    else:
        output = result.stderr

    return render_template('main.html', output=output)


if __name__ == '__main__':
    app.run(debug=True)
