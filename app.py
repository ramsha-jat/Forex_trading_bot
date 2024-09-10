import anthropic
import base64
import os.path
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

import asyncio
import os
import anthropic
import atexit
import pandas as pd



# URL to navigate to
url = 'https://www.investing.com/currencies/streaming-forex-rates-majors'

# get element by 'data-test' attribute with value 'dynamic-table'
tag = '[data-test="dynamic-table"]'

# Check if the Chrome executable path exists


if not os.getenv("ANTHROPIC_API_KEY"):
    raise Exception("ANTHROPIC_API_KEY environment variable is not set")

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

print('Anthropic client initialized')




def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def email_message(service, to, message_text):
    message = MIMEText(message_text)
    message["to"] = to
    message["subject"] = "Forex News"

    # Encode the message and send it
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message = {'raw': raw}
    service.users().messages().send(userId='me', body=message).execute()


def send_email(message_text):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """

    creds = get_credentials()

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)

        # send email
        email_message(service, 'ramsha.bscsf19@iba-suk.edu.pk', message_text)
        email_message(service, 'rajahassanali25@gmail.com', message_text)
        print("Email sent successfully")
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")




# if __name__ == '__main__':
#     asyncio.run(main())  # this will run the main function, which will run the send_data function every 30 minutes

import asyncio
from pyppeteer import launch




import asyncio
from playwright.async_api import async_playwright
#
#
# async def get_source_code(url):
#     async with async_playwright() as p:
#         # Launch a headless browser
#         browser = await p.chromium.launch()
#
#         # Open a new page
#         page = await browser.new_page()
#
#         # Go to the specified URL
#         await page.goto(url)
#
#         # Get the page content (HTML)
#         content = await page.content()
#
#         # Close the browser
#         await browser.close()
#
#         return content
#
#
# # Run the async function and print the result
# source_code = asyncio.run(get_source_code(url))
# print(source_code)
# from playwright.sync_api import sync_playwright
#
# with sync_playwright() as p:
#     for browser_type in [p.chromium, p.firefox, p.webkit]:
#         browser = browser_type.launch()
#         page = browser.new_page()
#         page.goto('http://playwright.dev')
#         page.screenshot(path=f'example-{browser_type.name}.png')
#         browser.close()
#
# import asyncio
# from playwright.async_api import async_playwright
async def get_data_with_scroll(url, selector):
    async with async_playwright() as p:
        browser = await   p.chromium.launch(args=["--disable-infobars"])
        page = await browser.new_page()
        # await page.set_java_script_enabled(False)
        await page.goto(url,wait_until="domcontentloaded")

        # Scroll down to the bottom of the page to load more content
        previous_height = await page.evaluate("document.body.scrollHeight")
        while True:
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(200000)  # Adjust the delay as needed

            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == previous_height:
                break
            previous_height = new_height

        # Extract content after scrolling
        elements = await page.query_selector_all(selector)
        data = [await element.text_content() for element in elements]

        await browser.close()
        return data

#
# # Run the async function and print the result
# selector = 'p'  # Replace with the selector of the elements you want to extract data from
# data = asyncio.run(get_data_with_scroll(url, selector))
# print(data)


websocket_url = "ws://localhost:9222/devtools/browser/b0fdbb83-a425-472f-9372-76283320953a"
import websockets

import asyncio
from playwright.async_api import async_playwright
import bs4

async def get_page_content():
    # Replace with your actual WebSocket Debugging URL

    async with async_playwright() as p:
        # Connect to the already running browser
        browser = await p.chromium.connect_over_cdp(websocket_url)

        # Get all open pages (tabs)
        print(browser.contexts)
        pages = browser.contexts[0].pages

        while True:

            # print( browser.contexts[0])
            # Iterate through each page and print the title
            print(pages)
            for page in pages:
                title = await page.title()
                print(f'Tab Title: {title}')

            # Select the first page (assuming it's the page you want)
            # Change index if needed for different tabs
            page = pages[0]
            # for i in range(len(pages)):
            #     page = pages[i]
            #     if 'https://www.investing.com/currencies/streaming-forex-rates-majors' in page.url:
            #         break

            # Get the page content (HTML)
            # content = await page.content()
            # get data-test="dynamic-table" selector
            await page.wait_for_selector('[data-test="dynamic-table"]',
                                         timeout=10000)  # Timeout after 10 seconds if not found

            # Get the content of the element with the attribute `data-test="dynamic-table"`
            table_content = await page.eval_on_selector('[data-test="dynamic-table"]', 'element => element.outerHTML')
            # print(table_content)
            # Parse the HTML content using BeautifulSoup
            soup = bs4.BeautifulSoup(table_content, 'html.parser')
            # table
            table = soup.find('table')
            # print(table)
            # print text
            print(table.text)
            csv_data = table.text

            csv_data += ("Based on the above information, predict the potential impact on the Forex market and use the "
                         "volatility.")
            # the message using the Claude model
            message = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,  # token
                temperature=0.6,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": csv_data
                            }
                        ]
                    }
                ]
            )

            send_email(message.content[0].text)
            await asyncio.sleep(1800) # 30 minutes


    # return content


# Run the async function and print the result
asyncio.run(get_page_content())
# print(content)
