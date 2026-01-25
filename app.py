from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# PIN code for city comparison page
CITY_COMPARISON_PIN = '2026'


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
    # Check if user is authenticated
    if not session.get('city_comparison_authenticated'):
        return redirect(url_for('city_comparison_login'))
    return render_template('city-comparison-styled.html')


@app.route('/city-comparison-login', methods=['GET', 'POST'])
def city_comparison_login():
    error = None
    if request.method == 'POST':
        pin = request.form.get('pin', '')
        if pin == CITY_COMPARISON_PIN:
            session['city_comparison_authenticated'] = True
            return redirect(url_for('city_comparison_styled'))
        else:
            error = 'Incorrect PIN. Please try again.'
    return render_template('city-comparison-login.html', error=error)


@app.route('/city-comparison-logout')
def city_comparison_logout():
    session.pop('city_comparison_authenticated', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
