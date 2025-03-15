import os
import asyncio
from flask import Flask, render_template, redirect, url_for, send_file
from flask_caching import Cache
from forms import ResumeForm
from api import deepseek_api
from pdf_transformer import html_to_pdf
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config["CACHE_TYPE"] = "simple"
cache = Cache(app)
cache.init_app(app)


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/form/", methods=["GET", "POST"])
def form():
    form = ResumeForm()
    if form.validate_on_submit():
        cache.set('generated_html', None)

        def generate_resume(data):
            generated_html = deepseek_api(data)
            if generated_html:
                cache.set('generated_html', generated_html)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_in_executor(None, generate_resume, form.data)

        return redirect(url_for("waiting"))

    return render_template("form.html", form=form)


@app.route("/waiting/")
def waiting():
    return render_template("waiting.html")


@app.route("/check_status/")
def check_status():
    status = cache.get("generated_html")
    if status == "error":
        return {"error": "An error occurred while generating the resume. Please try again"}
    return {"ready": status is not None}


@app.route("/resume/")
def resume():
    html_code = cache.get('generated_html')
    if not html_code:
        return "Error: Resume is not ready yet", 400
    return render_template("resume.html", html_code=html_code)


@app.route("/download_pdf/")
def download_pdf():
    html_code = cache.get('generated_html')
    if not html_code:
        return "Error: no HTML code", 400
    pdf_data = asyncio.run(html_to_pdf(html_code))
    return send_file(pdf_data, as_attachment=True, download_name="resume.pdf", mimetype="application/pdf")



if __name__ == "__main__":
    app.run(debug=True)
