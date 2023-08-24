# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 12:19:38 2022

@author: Siyabonga
"""
import re
import requests
from bs4 import BeautifulSoup

class linkedin_Extraction:
    CLEANR = re.compile('<.*?>')

    def func(value):
        return ''.join(value.splitlines())

    def cleanhtml(raw_html):
        cleantext = re.sub(linkedin_Extraction.CLEANR, '', raw_html)
        return cleantext
#___________________________________________________________________________________________________________________________________________

    def Get_Page(link):

        # The Logging in and extraction of data will be done here
        client = requests.Session() 
        # 
        # --- Logging Into Linked in
        HomepageURL = "https://www.linkedin.com"
        LoginURL = "https://www.linkedin.com/checkpoint/lg/login-submit"
        try:
            html = client.get(HomepageURL).content
        except requests.ConnectionError:
            return 3

        soup = BeautifulSoup(html,"html.parser")
        # --- username & password
        csrf = soup.find(id = "loginCsrfParam-login")
        login_info = {'session_key':'sibiyalerato894@gmail.com','session_password':'10111kA^^','loginCsrfParam':csrf,}
        # --- Logging in and extracting
        
        try:
            client.post(LoginURL,data = login_info)
        except requests.ConnectionError:
            return 3
        
        try:
            web_info = client.get(link)
        except requests.exceptions.RequestException as e:
                return 4
        
        html_web = web_info.text
        return html_web

        
        

#_____________________________________________________________________________________________________________________________________________-

    def Get_Description(page): 
        soup = BeautifulSoup(page,"html.parser") 
        for data in soup.find_all("div", class_="description__text description__text--rich"):
            job_desc_info = data.get_text()
            #
            job_info = linkedin_Extraction.func(job_desc_info)
            description = re.sub(' +', ' ', job_info)
            return description
    
    def Get_title(page):
        soup = BeautifulSoup(page,"html.parser")  
        titleH = soup.h1
        title = linkedin_Extraction.cleanhtml(str(titleH))
        return title

# ``````````````````````````````````````````````````````````````~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~````````````````````````````````````````````````````````````````
class Career24_Extraction:
    def func(value):
        return ''.join(value.splitlines())

    def Get_Page(link):
        client = requests.Session()
        login_PAGE = 'https://www.careers24.com/Login'
        login_info = {'Email':'Drsiya36@gmail.com','Password':'Drntswembu36@','CheckIfHuman':'False','__RequestVerificationToken':'CfDJ8PrA7ETzixFIirXXHuY5vJvg6IOi1ayclU8HnP371up5hRjaeCztujgoy9MMfJKiBW-ZSxO3jL3DyQ4Eu46mqH7oPRl0jqNJLUcBCscyXFWy-8td6u3KTCbdIopGfSWmALt9pSnSI-RyvdA6nU1YUxo','IsPersistent':'false',}
        
        try:
            client.post(login_PAGE,data = login_info)
        except requests.ConnectionError:
            return 3
             
        
        try:
            cont = client.get(link)
        except requests.exceptions.RequestException as e:
                return 4
                
        html_web = cont.text
        return html_web

    def get_title(page):
        soup = BeautifulSoup(page,"html.parser")
        html_title = soup.find('title')
        title_as_whole = html_title.string
        Comma_pos = title_as_whole.rfind(',')
        title = title_as_whole[0:Comma_pos:1]
        return title

    def get_location(page):
        soup = BeautifulSoup(page,"html.parser")
        html_title = soup.find('title')
        title_as_whole = html_title.string
        Comma_pos = title_as_whole.rfind(',')
        desh_pos = title_as_whole.rfind('-')
        location = title_as_whole[Comma_pos+2:desh_pos-1:1] 
        return location

    def Get_Description(page): 
        soup = BeautifulSoup(page,"html.parser") 
        for data in soup.find_all("div", class_="v-descrip"):
            job_desc_info = data.get_text()
        job_desc = Career24_Extraction.func(job_desc_info)
        final_text = re.sub(' +', ' ', job_desc)
        return final_text