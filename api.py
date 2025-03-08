import os
import requests
import json


def deepseek_api(d):
    try:
        info = "\n".join([f"{k}: {v}" for k, v in d.items()])

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
            "Authorization": f"Bearer {os.getenv("API_KEY")}",
            "Content-Type": "application/json",
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
        response.raise_for_status()
        r = response.json()["choices"][0]["message"]["content"].split("```")
        for el in r:
            if "<!DOCTYPE html>" in el and "</html>" in el:
                print(el)
                return el.replace("html\n", "")
            
    except requests.exceptions.RequestException as ex:
        print(f"Request error: {ex}")
    except KeyError:
        print("Unexpected API response format")
    except Exception as ex:
        print(f"Error! Your exception is {ex}")
    
    return "error"

