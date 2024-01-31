from flask import Flask, request, jsonify
import openai
import json
import apiKeys
import os
import sys
# import config

app = Flask(__name__)

# import the api key
openai.api_key = apiKeys.OPENAI_API_KEY

# Define arrays for each category
ulasim_ofisi = []
catering = []
bilisim = []
otopark = []
saha = []
gruplandirilmamis = []

# Function to take user input
def get_user_input():
    return input("Enter your text: ")

# user_request = "Semihin çok yorulmuş, soğuk bir şeyler içmek istiyor."

def run_conversation(user_request):
  message = """

  Determine which of the given 6 categories the sentence entered by the user belongs to. Respond with only one of the 6 categories(Ulaşım ofisi, Catering, Bilişim, Otopark, Saha, Gruplandırılamamış/diğer).

  - Ulaşım ofisi = Any sentence related to the transportation of middle school, high school, university participants, and volunteers who arrive at the Teknofest area from outside by bus and plane falls into this category. Key words = Uçak, otobüs, ulaşım, trafik, kaza.
  - Catering = Any topic related to food, water, and snack services falls into this category. Key words = Su, Catering, eksik, geç geldi, hala yok, eksik.
  - Bilişim = Any sentence related to computers, software, hardware, network, server, internet, wifi, electricity, electronics, and electronic cards in the Teknofest area falls into this category. Key words = Bilgisayar, yazılım, donanım, ağ, sunucu, internet, wifi, elektrik, elektronik, elektronik kart, arıza.
  - Otopark = It is related to the location where vehicles are parked in the Teknofest area. Key words = Otopark, araç, park, park yeri, özel araç, ambulans, polis, jandarma.
  - Saha = Any sentence related to the field, track, hangar, booth, tent, and other areas in the Teknofest area falls into this category. Key words = Saha, pist, hangar, stant, çadır, scooter, kayıp çocuk, kavga.
  - Gruplandırılamamış/diğer = sentences that do not belong to any of the other categories.
  
  """

  messages = [{"role": "system", "content": message},
              #  Only reply with given function parameters in a dictionary. For parameter that are not specified always fill them randomly with valid type of value."},
              #  + explanations_of_predicates + "Use predicaters to vizualize the environment to take action."},
              #  You are an assistant that always replies with multiple function calls in straight JSON format ready to parsed. 
              {"role": "user", "content": user_request}]
  print("messages: " + str(messages))

  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-16k",
      messages=messages,
      # functions=functions,
      # function_call="auto",
      temperature=0.0,
  )
  response_message = response["choices"][0]["message"]["content"]

  print("Tüm kategoriler:\nUlaşım ofisi\nCatering\nBilişim\nOtopark\nSaha\nGruplandırılamamış/diğer" + "\n")
  print("Girilen Sorun= " + "\n")
  print("Sorun kategorisi: " + str(response_message) + "\n\n\n")

# Function to analyze the response and determine the category
def determine_category(response):
    if "Ulaşım Ofisi" in response:
        return ulasim_ofisi
    elif "Catering" in response:
        return catering
    elif "Bilişim" in response:
        return bilisim
    elif "Otopark" in response:
        return otopark
    elif "Saha" in response:
        return saha
    else:
        return gruplandirilmamis


from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/run_prototype', methods=['POST'])
def run_prototype():
    # user_request = get_user_input()
    user_request = request.json['userInput']
    response = run_conversation(user_request)
    category = determine_category(response)
    category.append(user_request)
    return jsonify({'category': category})

# run_prototype()
if __name__ == '__main__':
    app.run(port=5000)