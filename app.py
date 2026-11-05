import os
from urllib.parse import urlsplit

from authlib.integrations.base_client.errors import OAuthError
from authlib.integrations.flask_client import OAuth
from flask import Flask, abort, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY") or os.urandom(32),
    AUTH_SECRET_KEY_CONFIGURED=bool(os.environ.get("SECRET_KEY")),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=(
        os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"
    ),
    MICROSOFT_CLIENT_ID=os.environ.get("MICROSOFT_CLIENT_ID"),
    MICROSOFT_CLIENT_SECRET=os.environ.get("MICROSOFT_CLIENT_SECRET"),
    MICROSOFT_REDIRECT_URI=os.environ.get("MICROSOFT_REDIRECT_URI"),
)

ALLOWED_LOGIN_EMAIL = "haslhofer@outlook.com"
MICROSOFT_METADATA_URL = (
    "https://login.microsoftonline.com/consumers/v2.0/.well-known/openid-configuration"
)

oauth = OAuth(app)
microsoft = oauth.register(
    name="microsoft",
    client_id=app.config["MICROSOFT_CLIENT_ID"],
    client_secret=app.config["MICROSOFT_CLIENT_SECRET"],
    server_metadata_url=MICROSOFT_METADATA_URL,
    client_kwargs={"scope": "openid email profile"},
)


def _microsoft_login_configured():
    return all(
        (
            app.config["MICROSOFT_CLIENT_ID"],
            app.config["MICROSOFT_CLIENT_SECRET"],
            app.config["MICROSOFT_REDIRECT_URI"],
            app.config["AUTH_SECRET_KEY_CONFIGURED"],
        )
    )


def _safe_next_url(target):
    if not target:
        return url_for("index")
    parsed = urlsplit(target)
    if (
        target.startswith("/")
        and not target.startswith("//")
        and "\\" not in target
        and not parsed.netloc
    ):
        return target
    return url_for("index")


@app.before_request
def require_login_for_pages():
    public_endpoints = {
        "index",
        "auth_login",
        "auth_callback",
        "city_comparison_login",
        "logout",
        "static",
    }
    if (
        request.endpoint not in public_endpoints
        and request.endpoint is not None
        and session.get("authenticated_email") != ALLOWED_LOGIN_EMAIL
    ):
        next_url = request.full_path if request.query_string else request.path
        return redirect(url_for("auth_login", next=_safe_next_url(next_url)))


@app.route('/')
def index():
    return render_template(
        "index.html",
        is_authenticated=session.get("authenticated_email") == ALLOWED_LOGIN_EMAIL,
    )


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


@app.route("/login")
def auth_login():
    if session.get("authenticated_email") == ALLOWED_LOGIN_EMAIL:
        return redirect(url_for("index"))
    if not _microsoft_login_configured():
        return render_template(
            "city-comparison-login.html",
            error="Microsoft sign-in is not configured for this site yet.",
            login_url=None,
        ), 503

    next_url = _safe_next_url(request.args.get("next"))
    session["post_login_redirect"] = next_url
    return microsoft.authorize_redirect(
        app.config["MICROSOFT_REDIRECT_URI"], prompt="select_account"
    )


@app.route("/auth/callback")
def auth_callback():
    if not _microsoft_login_configured():
        abort(503)
    try:
        token = microsoft.authorize_access_token()
    except OAuthError:
        return render_template(
            "city-comparison-login.html",
            error="Microsoft sign-in could not be completed. Please try again.",
            login_url=url_for("auth_login"),
        ), 400

    userinfo = token.get("userinfo") or {}
    email = (
        userinfo.get("email") or userinfo.get("preferred_username") or ""
    ).casefold()
    if email != ALLOWED_LOGIN_EMAIL:
        next_url = _safe_next_url(session.get("post_login_redirect"))
        session.clear()
        return render_template(
            "city-comparison-login.html",
            error=f"Sign in with {ALLOWED_LOGIN_EMAIL} to access protected pages.",
            login_url=url_for("auth_login", next=next_url),
        ), 403

    next_url = _safe_next_url(session.get("post_login_redirect"))
    session.clear()
    session["authenticated_email"] = email
    return redirect(next_url)


@app.route("/city-comparison-login")
def city_comparison_login():
    return redirect(url_for("auth_login"))


@app.route("/logout")
@app.route("/city-comparison-logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


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
    return render_template('us-options.html')


@app.route('/cities-comparison-all')
def cities_comparison_all():
    return render_template('cities-comparison-all.html')


@app.route('/italy-itinerary')
def italy_itinerary():
    return render_template('italy-itinerary.html')


@app.route('/idea-visualizer')
def idea_visualizer():
    return render_template('idea-visualizer.html')


@app.route('/apps-contact')
def apps_contact():
    return render_template('apps-contact.html')


@app.route('/websites')
def websites():
    return render_template('websites.html')


@app.route('/challenges-slide')
def challenges_slide():
    return render_template('challenges-slide.html')


@app.route('/trail-running')
def trail_running():
    return render_template('trail-running.html')


@app.route('/best-value-models')
def best_value_models():
    return render_template('best-value-models.html')


if __name__ == '__main__':
    app.run(debug=True)
