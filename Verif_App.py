# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 09:34:40 2022

@author: Siyabonga
"""

import Verifying_Code
from flask import Flask, render_template, request, jsonify
from spellchecker import SpellChecker
import re
import DataExtraction

from rob import get_response 
#import validators

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

# ================================================================================

@app.route('/box')
def linkPage():
    return render_template('box.html', prediction=-1)

@app.route('/textBox')
def TextPage():
    return render_template('textBox.html', prediction=-1)

# ================================================================================

@app.route('/Load1', methods=['POST'])
def Load1():
    if request.method == 'POST':
        URL = request.form['URL_Link']
        urlType = request.form['website'] 
    return render_template('progressBar.html', type = urlType, link = URL,box = 0)

@app.route('/Load2', methods=['POST'])
def Load2():
    if request.method == 'POST':
        desc = request.form['message']
        title = request.form['pasteLink'] 
        location = request.form['Location']
    return render_template('progressBar.html', job_title = title, job_desc = desc, job_location = location,box = 1)

# ================================================================================

#Verifies for link
@app.route('/Link_predict', methods=['POST'])
def Link_predict():
    if request.method == 'POST':
        urlType = request.form['urlType']

        if (urlType == 'LinkedIn'):
            extractingObj = DataExtraction.linkedin_Extraction
            URL = request.form['URL_Link']
            html_page = extractingObj.Get_Page(URL)
            if (html_page == 3):
                return render_template('disconnected.html')
            elif(html_page == 4):
                return render_template('errorText.html')
            else:
                title = extractingObj.Get_title(html_page) 
                desc = extractingObj.Get_Description(html_page)
                location = "Pretoria"
                feedBack = Verifying_Code.Verify(title,location,desc)
                return render_template('box.html', prediction=feedBack, job_title = title,link = URL, job_desc = desc, job_location = location)
        
        elif(urlType == 'Careers24'):
            extractingObj = DataExtraction.Career24_Extraction
            URL = request.form['URL_Link']
            html_page = extractingObj.Get_Page(URL)
            if (html_page == 3):
                return render_template('disconnected.html')
            elif(html_page == 4):
                return render_template('errorText.html')
            else:
                title = extractingObj.get_title(html_page) 
                desc = extractingObj.Get_Description(html_page)
                location = extractingObj.get_location(html_page)
                feedBack = Verifying_Code.Verify(title,location,desc)
            return render_template('box.html', prediction=feedBack, job_title = title,link = URL, job_desc = desc, job_location = location)
        else:
            return render_template('box.html', prediction=2)
        

#Verifies for text
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        spell = SpellChecker()

        desc = request.form['message']
        titl = request.form['pasteLink']
        titl_msg = re.sub(r"\s+|[`~!#%,/;?*'()-•.&:â€¢Â$]\s*", ' ',titl)
        msg = re.sub(r"\s+|[`~!#%,/;?*'-()•.&:â€¢Â$]\s*", ' ',desc)
        misspelled_title = spell.unknown(titl_msg.split()) 
        misspelled = spell.unknown(msg.split())
        bogus = False
        
# COUNT WORDS HERE
        count = len(msg.split())

        for word in misspelled_title:
            bogus = True

        for word in misspelled:
            bogus = True
        
        
        
        if count < 9:
            return render_template('textBox.html', prediction=4)
        else:
            if bogus:
                return render_template('textBox.html', prediction=2)
            else:
                location = request.form['Location']
                feedBack = Verifying_Code.Verify(titl,location,desc)
                return render_template('textbox.html', prediction=feedBack, job_title = titl, job_desc = desc, job_location = location)  
    else:
        return render_template('textBox.html', prediction=2)

# ================================================================================



@app.route("/respond", methods=['POST'])
def respond():
    text = request.get_json().get("message") 
    # Check if text is valid
    reply = get_response(text)
    response = {"answer": reply}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
    
