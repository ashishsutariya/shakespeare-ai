# Run by typing python3 main.py

# **IMPORTANT:** only collaborators on the project where you run
# this can access this web server!
"""
    Bonus points if you want to have internship at AI Camp
    1. How can we save what user built? And if we can save them, like allow them to publish, can we load the saved results back on the home page? 
    2. Can you add a button for each generated item at the frontend to just allow that item to be added to the story that the user is building? 
    3. What other features you'd like to develop to help AI write better with a user? 
    4. How to speed up the model run? Quantize the model? Using a GPU to run the model? 
"""

# import basics
import os
from flask import Flask
from flask import render_template, request
import requests
global API_URL
global headers
global response
import smtplib

# import stuff for our web server
from flask import redirect, url_for, session
from utils import get_base_url
# import stuff for our models
# from aitextgen import aitextgen

# load up a model from memory. Note you may not need all of these options.
# ai = aitextgen(model_folder="model/",
#                tokenizer_file="model/aitextgen.tokenizer.json", to_gpu=False)

# ai = aitextgen(model="distilgpt2", to_gpu=False)

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
  app = Flask(__name__)
else:
  app = Flask(__name__, static_url_path=base_url + 'static')

app.secret_key = os.urandom(64)

# set up the routes and logic for the webserver

# import torch
# from transformers import GPT2Tokenizer, GPT2LMHeadModel

# tokenizer = GPT2Tokenizer.from_pretrained("/path/to/tokenizer/files")
# model = GPT2LMHeadModel.from_pretrained("/path/to/model/files")
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# def generate_text(prompt):
#     input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
#     output = model.generate(input_ids, max_length=1000, do_sample=True, top_p=0.95, top_k=60)
#     generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
#     return generated_text


# bkp
def query(text):
  payload = {"inputs": text}
  API_URL = "https://api-inference.huggingface.co/models/Ashish9879/aic_shakespeare"
  # API_URL = "https://api-inference.huggingface.co/models/Ashish9879/aic_shakespeare2"
  headers = {"Authorization": "Bearer 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"}
  response = requests.post(API_URL, headers=headers, json=payload)
  try:
    q = eval(
      str(response.content)[3:-2].replace("\\n",
                                          " ").replace("\\",
                                                       " "))["generated_text"]
    print(q)
  except Exception as e:
    q = e
    q = "I am sorry our creative expert is busy due to traffic, Please try again after some time. Thank you!"
  return q


@app.route(f'{base_url}')
def home():
  # return render_template('writer_home.html', generated=None)
  return render_template('index.html')


@app.route(f'{base_url}/model/')
def model():
  return render_template('model.html')


@app.route(f'{base_url}/model/', methods=['POST'])
def process_form():
  global prompt
  prompt = request.form['prompt']  # prompt is requesting from this form
  prompt
  # Process the prompt and return the result
  result = process_prompt(prompt)
  return result


def process_prompt(prompt):

  processed_prompt = query(prompt)

  return render_template('model.html', processed_prompt=processed_prompt)


# @app.route('/model', methods=['POST'])
# def process_form():
#   # Get the prompt from the form data
#   global prompt
#   prompt = request.form['prompt']  # prompt is requesting from this form
#   prompt
#   # Process the prompt and return the result
#   result = process_prompt(prompt)
#   return result


@app.route(f'{base_url}/results/')
def results():
  if 'data' in session:
    data = session['data']
    return render_template('Write-your-story-with-AI.html', generated=data)
  else:
    return render_template('Write-your-story-with-AI.html', generated=None)


@app.route(f'{base_url}/learn/')
def learn():
  return render_template('learnmore.html')


# @app.route(f'{base_url}/generate_text/', methods=["POST"])
# def generate_text():
#   """
#     view function that will return json response for generated text.
#     """

#   prompt = request.form['prompt']
#   if prompt is not None:
#     generated = ai.generate(n=1,
#                             batch_size=3,
#                             prompt=str(prompt),
#                             max_length=300,
#                             temperature=0.9,
#                             return_as_list=True)

#   data = {'generated_ls': generated}
#   session['data'] = generated[0]
#   return redirect(url_for('results'))

# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page

if __name__ == '__main__':
  # IMPORTANT: change url to the site where you are editing this file.
  website_url = 'coding.ai-camp.dev'

  print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
  app.run(host='0.0.0.0', port=port, debug=True)
