import os
import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

switch = 0

genai.configure(api_key="**your api key here**")

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 200,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  system_instruction="**insert your chatbots personality here**",
)

history = []

driver_path = '**insert web driver path here**'
service = Service(driver_path)
driver = webdriver.Chrome(service=service) 
driver.get('https://web.whatsapp.com')
print("Please scan the QR code to log in.")
time.sleep(20)

contact_name = "**name of the person u want your chatbot to talk with**"

search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")
search_box.click()
search_box.send_keys(contact_name + Keys.ENTER)

print(f"Now reading messages from {contact_name}...")

messages = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjz._amjw span.selectable-text")
old_message = messages[-1].text
print(old_message)

try:
    while True:
        chat_session = model.start_chat(
        history = history  
        )
        messages = driver.find_elements(By.CSS_SELECTOR, "div.message-in.focusable-list-item._amjy._amjz._amjw span.selectable-text")
        for message in messages[-1:]:
            if(message.text != old_message):
              if(switch == 0):
                message_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p')
                message_box.click()
                greetings_message = "**insert a greeting message here**"
                message_box.send_keys(greetings_message + Keys.ENTER)
                time.sleep(3)
                switch = 1

              print("Message:", message.text)
              old_message = message.text
              response = chat_session.send_message(message.text)
              model_response = response.text
              print("Bot:", model_response)
              message_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p')
              message_box.click()
              message_box.send_keys(model_response + Keys.ENTER)
              time.sleep(3)
              history.append({"role": "user", "parts": [message.text]})
              history.append({"role": "model", "parts": [model_response]})
              

        if message.text.lower() in ["quit", "exit", "bye"]:
            break
        time.sleep(3)
except KeyboardInterrupt:
    print("Stopped reading messages.")

finally:
    driver.quit()
