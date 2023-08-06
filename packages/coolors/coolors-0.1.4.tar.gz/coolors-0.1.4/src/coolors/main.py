import asyncio
from pyppeteer import launch
import json

def generate():
    loop = asyncio.get_event_loop()
    r = loop.run_until_complete(async_generate())
    return r

async def async_generate():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto('https://coolors.co/generate',{'waitUntil' : 'networkidle2'})
    js = "() => { return window.location.href }"
    url = await page.evaluate(js)
    await browser.close()
    colors = url.split('/')[-1]
    results = colors.split('-')
    return results
