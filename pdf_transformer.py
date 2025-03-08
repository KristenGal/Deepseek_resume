import io
from playwright.async_api import async_playwright


async def html_to_pdf(html_content):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html_content)
        pdf_bytes = await page.pdf(format='A4', margin={'top': '20px', 'bottom': '20px'})
        await browser.close()
        return io.BytesIO(pdf_bytes)