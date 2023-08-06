import asyncio
from pyppeteer import launch
import json

def coolors():
    loop = asyncio.get_event_loop()
    r = loop.run_until_complete(_main())
    result = r.split('/')[-1]
    results = result.split('-')

    return results

async def _main():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto('https://coolors.co/generate',{'waitUntil' : 'networkidle2'})
    js = "() => { return window.location.href }"
    result = await page.evaluate(js)
    await browser.close()

    return result
