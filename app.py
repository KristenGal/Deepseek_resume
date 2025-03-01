import asyncio
from flask import Flask, render_template, redirect, url_for, session, send_file
from forms import ResumeForm
from api import deepseek_api
from pdf_transformer import html_to_pdf


app = Flask(__name__)
app.secret_key = "XPoFGUfCaV5EX4-US-BE7N-E7jVZEZn18zzSipMhen0"


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/form/", methods=["GET", "POST"])
def form():
    form = ResumeForm()
    if form.validate_on_submit():
        generated_html = deepseek_api(form.data)
        if generated_html:
            session['generated_html'] = generated_html
            return redirect(url_for("resume"))
    return render_template("form.html", form=form)


@app.route("/resume/")
def resume():
    html_code = session.get('generated_html')
    return render_template("resume.html", html_code=html_code)


@app.route("/download_pdf/")
def download_pdf():
    html_code = session.get('generated_html')
    if not html_code:
        return "Error: no HTML-code", 400
    pdf_data = asyncio.run(html_to_pdf(html_code))
    return send_file(pdf_data, as_attachment=True, download_name="resume.pdf", mimetype="application/pdf")




if __name__ == "__main__":
    app.run(debug=True)
