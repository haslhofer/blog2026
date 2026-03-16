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


@app.route('/cities-hub')
def cities_hub():
    return render_template('cities-hub.html')


@app.route('/city-javea')
def city_javea():
    return render_template('city-javea.html')


@app.route('/city-como')
def city_como():
    return render_template('city-como.html')


@app.route('/city-cernobbio')
def city_cernobbio():
    return render_template('city-cernobbio.html')


@app.route('/city-laglio')
def city_laglio():
    return render_template('city-laglio.html')


@app.route('/city-altea')
def city_altea():
    return render_template('city-altea.html')


@app.route('/city-calpe')
def city_calpe():
    return render_template('city-calpe.html')


@app.route('/city-torno')
def city_torno():
    return render_template('city-torno.html')


@app.route('/city-moltrasio')
def city_moltrasio():
    return render_template('city-moltrasio.html')


@app.route('/city-brienno')
def city_brienno():
    return render_template('city-brienno.html')


@app.route('/city-argegno')
def city_argegno():
    return render_template('city-argegno.html')


@app.route('/city-canet-de-mar')
def city_canet_de_mar():
    return render_template('city-canet-de-mar.html')


@app.route('/city-platja-daro')
def city_platja_daro():
    return render_template('city-platja-daro.html')


@app.route('/city-calella')
def city_calella():
    return render_template('city-calella.html')


@app.route('/us-options')
def us_options():
    if not session.get('city_comparison_authenticated'):
        return redirect(url_for('city_comparison_login'))
    return render_template('us-options.html')


@app.route('/cities-comparison-all')
def cities_comparison_all():
    # Check if user is authenticated
    if not session.get('city_comparison_authenticated'):
        return redirect(url_for('city_comparison_login'))
    return render_template('cities-comparison-all.html')


@app.route('/italy-itinerary')
def italy_itinerary():
    return render_template('italy-itinerary.html')


@app.route('/challenges-slide')
def challenges_slide():
    return render_template('challenges-slide.html')


if __name__ == '__main__':
    app.run(debug=True)
