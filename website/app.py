from flask import Flask, render_template, send_file

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('main.html')

@app.route('/sum_map.html')
def map():
    return render_template('sum_map.html')

@app.route('/download_app')
def download_file():
    my_file = "EpidemLab-1.0.tar.gz"
    return send_file(my_file, as_attachment=True)

@app.route('/download_doc')
def download():
    my_file = "documentary.pdf"
    return send_file(my_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
