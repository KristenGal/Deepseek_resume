from flask import Flask, flash, render_template, redirect, url_for, render_template_string, session
from forms import ResumeForm
from api import deepseek_api

app = Flask(__name__)
app.secret_key = "XPoFGUfCaV5EX4-US-BE7N-E7jVZEZn18zzSipMhen0"


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/resume/")
def resume():
    html_code = session.get('generated_html')
    return render_template_string(html_code) if html_code else "Not found your resume"


@app.route("/form/", methods=["GET", "POST"])
def form():
    form = ResumeForm()
    if form.validate_on_submit():
        d = form.data
        api = deepseek_api(d)
        print(api)
        if api:
            session['generated_html'] = api
            return redirect(url_for("resume"))
    return render_template("form.html", form=form)





if __name__ == "__main__":
    app.run(debug=True)
