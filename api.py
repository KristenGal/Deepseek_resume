import requests
import json


def deepseek_api(d):
    info = ""
    for k, v in d.items():
        info = info + str(k) + ": " + str(v) + "\n"

    content = f"""Create an HTML file for a professional resume template. The resume should have the following sections. Do not provide me with any information besides Html file:

Header:

Full name at the top, bolded and large.
A smaller subtitle underneath with a short job title or profession.
Contact information below the subtitle
Summary Section:

A brief paragraph summarizing career highlights and professional experience.
Skills Section:

A list of technical and soft skills, organized into two categories.
Work Experience Section:

List of previous jobs with job titles, company names, and dates of employment.
A brief description of responsibilities and achievements in bullet points.
Education Section:

Degrees obtained with institutions
Footer:

A section for references or a "available upon request" note.
Style:

Use a clean, minimalist design.
The font should be modern and readable
Use a light background with dark text for contrast.
Please ensure the HTML structure is organized with clear semantic tags (e.g., <header>, <section>, <footer>), and include basic CSS for styling.

use this information.
{info}"""

    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
    #    "HTTP-Referer": "<YOUR_SITE_URL>", Optional. Site URL for rankings on openrouter.ai.
    #    "X-Title": "<YOUR_SITE_NAME>", Optional. Site title for rankings on openrouter.ai.
    },
    data=json.dumps({
        "model": "deepseek/deepseek-r1:free",
        # "model": "deepseek/deepseek-r1",
        "messages": [
        {
            "role": "user",
            "content": content
        }
        ],
        
    })
    )
    
    print(response)
    try:
        r = response.json()["choices"][0]["message"]["content"].split("```")
        for el in r:
            if "<!DOCTYPE html>" in el:
                return el.replace("html\n", "")
    except Exception as ex:
        print(f"Error! Your exception is {ex}")
        return None


# a = {"Name": "Alex Pyvovarov",
# "Address": "171 queen st",
# "Email": "alalalalal@gmail.com",
# "job titles": "softwere enginer, team lead",
# "skills": "Python, Java, Linux, C++, Git, SQL, HTML, teamworking, networking, hard working, social",
# "Education": "computer science in harvard",
# "Experience": "5 years in Apple, internship in Microsoft"}

# deepseek_api(a)
