from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/flowbook')
def flowbook():
    return render_template('flowbook.html')


@app.route('/continuous-ai')
def continuous_ai():
    return render_template('continuous-ai.html')


@app.route('/italian-lakes')
def italian_lakes():
    return render_template('italian-lakes.html')


@app.route('/perseverance')
def perseverance():
    return render_template('perseverance.html')


@app.route('/steppr-arch')
def steppr_arch():
    return render_template('steppr-arch.html')


@app.route('/city-comparison-styled')
def city_comparison_styled():
    return render_template('city-comparison-styled.html')


if __name__ == '__main__':
    app.run(debug=True)
