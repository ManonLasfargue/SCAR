from flask import Flask, render_template, request
from emission_factors import FACTORS

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('scar_lasfargue.html')

@app.route('/form')
def form():
    return render_template('form_scar.html')

@app.route('/results', methods=['POST'])
def results():
    data = {k: float(request.form.get(k, 0) or 0) for k in FACTORS.keys()}
    results = {k: v * data[k] for k, v in FACTORS.items()}
    total = sum(results.values())
    results = {k: round(v, 2) for k, v in results.items() if v > 0}

    return render_template('results.html', total=round(total, 2), results=results)


if __name__ == '__main__':
    app.run(debug=True, port=5002)

