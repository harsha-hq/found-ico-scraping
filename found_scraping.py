# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 17:49:37 2021

@author: hvvel
"""

from bs4 import BeautifulSoup
from datetime import date
from selenium import webdriver
from itertools import repeat    
from pprint import pprint as pp
from lxml import etree
from found_ico_link import *
import os
import requests
import re
import copy
import time
import datetime
import pandas as pd
import js2xml

cd = pd.read_csv(r"C:\Users\hvvel\OneDrive\Documents\RA\Final Code\FoundICO\found_company_filter_link.csv",encoding='utf-8-sig')

found_links = cd["Company_Link"]

driver = webdriver.Chrome("C:/Users/hvvel/Downloads/Softwares/chromedriver_win32/chromedriver.exe")

HEADER = ['Company Name','Mark','Description','Main_info_rating','Finance_rating','Product_rating','Team_rating',
          'Marketing_rating','ICO_Score','Likes','Dislikes','Start Date','Start Time','End Date','End Time']  
FOUND_DF = pd.DataFrame(columns=HEADER)  
for link in found_links:
    print(link)
    driver.get(link)
    html_content = driver.execute_script('return document.body.innerHTML')
    soep = BeautifulSoup(html_content, 'lxml')
    #name
    POSTS = soep.body.find('div',class_='col-xs-12 col-sm-8 col-md-9 col-lg-9')
    if POSTS is not None:
        name = POSTS.find('h1').get_text()
        print(name)
        post_mark = POSTS.find('span',class_='prem-mark')
        if post_mark is not None:
            mark = POSTS.find('span',class_='prem-mark').get_text()
        else: 
            mark = ""
    #ico quality
    POST_ICO = soep.find('section', id='ico-rat-cont')
    if POST_ICO is not None:
        info_rating = POST_ICO.find('div',id='fmt-information')
        main_info = info_rating.find('div',class_="flmrk-mark").get_text()
    
    if POST_ICO is not None:
        fin_rating = POST_ICO.find('div', id ='fmt-finance')
        if fin_rating is not None:
            finance_rating = fin_rating.find('div',class_="flmrk-mark").get_text()
    #print(finance_rating)
    if POST_ICO is not None:    
        product_info = POST_ICO.find('div', id ='fmt-product')
        if product_info is not None:
            product_rating = product_info.find('div',class_="flmrk-mark").get_text()
    #print(product_rating)
    if POST_ICO is not None:    
        team_rating_info = POST_ICO.find('div', id ='fmt-team')
        if team_rating_info is not None:
            team_rating = team_rating_info.find('div',class_="flmrk-mark").get_text()
        #print(team_rating)
    
    if POST_ICO is not None:
        market_rating_info = POST_ICO.find('div', id ='fmt-marketing')
        if market_rating_info is not None:
            marketing_rating = market_rating_info.find('div',class_="flmrk-mark").get_text()
    #print(marketing_rating)
    
    if POST_ICO is not None:
        score = POST_ICO.find('div', class_ ='fl-mrk-fin')
        if score is not None:
            ico_score = score.find('span',class_= 'flmf-mark').find(text=True, recursive=False)

    #likes and dislikes
    like_info = soep.find('div', id='ic-rt-btns')
    num_likes = like_info.find(id = 'ic-rt-lk')
    project_up = num_likes.find('span',class_='ic-n-cont').get_text()
    dis_likes = like_info.find(id = 'ic-rt-ds')
    project_down = dis_likes.find('span',class_='ic-n-cont').get_text()
    #desc
    DESC_ICO = soep.find('section', id='ico-sum-cont') 
    desc = DESC_ICO.find('p').get_text()
    time_info = soep.find('section', id='ico-time-cont')
    #print(funding_info.get_text())
    if time_info is not None:
        start_date = time_info.find('div', id='ico-start')
        start_time = ''
        if start_date is not None:
            start_time = start_date.find_next_sibling(class_='ico-days')
            start_time = start_time.get_text().replace("\n","").replace("\t","")
            start_date = start_date.get_text().strip().replace("\n","").replace("\t","")
            start_date = datetime.datetime.strptime(start_date[:-2],'%Y%b %d').strftime('%m/%d/%Y')
        end_date = time_info.find('div', id='ico-end')
        end_time = ''
        if end_date is not None:
            end_time = end_date.find_next_sibling(class_='ico-days')
            end_time = end_time.get_text().strip().replace("\n","").replace("\t","")
            end_date = end_date.get_text().strip().replace("\n","").replace("\t","")
            end_date = datetime.datetime.strptime(end_date[:-2],'%Y%b %d').strftime('%m/%d/%Y')
    FOUND_DF = FOUND_DF.append({'Company Name':name,
                                'Mark':mark,
                                'Description':desc,
                                'Main_info_rating':main_info,
                                'Finance_rating':finance_rating,
                                'Product_rating':product_rating,
                                'Team_rating':team_rating,
                                'Marketing_rating':marketing_rating,
                                'ICO_Score':ico_score,
                                'Likes':project_up,
                                'Dislikes':project_down,
                                'Start Date':start_date,
                                'Start Time':start_time,
                                'End Date':end_date,
                                'End Time':end_time}, ignore_index=True)
FOUND_DF.to_csv("FOUND_DATA.csv", index=False,encoding='utf-8-sig')

##summary data
SUMMARY_HEADER = []
smry_data = {}
LISTDICT = []
for link in found_links:
    print(link)
    driver.get(link)
    html_content = driver.execute_script('return document.body.innerHTML')
    soep = BeautifulSoup(html_content, 'lxml')
    POSTS = soep.body.find('div',class_='col-xs-12 col-sm-8 col-md-9 col-lg-9')
    if POSTS is not None:
        name = POSTS.find('h1').get_text()
        print(name)
    summary = soep.find('section', id='ico-sum-cont') 
    smry_table = summary.find(class_='smry-table')
    for row in smry_table.findChildren('tr'):
        record = row.findChildren('td')
        if record[1].get_text() == 'Links:':
            links = record[2].find_all('a')
            for eachLink in links:
                key = eachLink['title']
                value = eachLink['href']
                smry_data[key] = value
        elif record[1].get_text() in smry_data:
            key = record[1].get_text() + str(1)
            value = record[2].get_text()
            smry_data[key] = value
        else:
            key = record[1].get_text()
            value = record[2].get_text()
            smry_data[key] = value
    smry_data['Company'] = name
    if len(SUMMARY_HEADER) > 0:
        SUMMARY_HEADER = list(set(SUMMARY_HEADER+list(smry_data.keys())))
    else:
        SUMMARY_HEADER = list(smry_data.keys())
    smry_data = {}
    LISTDICT.append(smry_data)
    #print(LISTDICT)
    SUMMARY_FOUND_DF = pd.DataFrame(columns=SUMMARY_HEADER)
    for dictItem in LISTDICT:
        SUMMARY_FOUND_DF = SUMMARY_FOUND_DF.append(dictItem, ignore_index=True)
SUMMARY_FOUND_DF.to_csv("SUMMARY_DATA.csv", index=False,encoding='utf-8-sig')
    #print(mark)
    

#Distribution
fncl_data = {}
FIN_HEADER = []
FIN_DICT = []        
for link in found_links:
    #print(link)
    driver.get(link)
    html_content = driver.execute_script('return document.body.innerHTML')
    soep = BeautifulSoup(html_content, 'lxml')
    POSTS = soep.body.find('div',class_='col-xs-12 col-sm-8 col-md-9 col-lg-9')
    if POSTS is not None:
        name = POSTS.find('h1').get_text()
        print(name)
    funding = soep.find('section', id='ico-time-cont') 
    fund_table = funding.find(class_='smry-table')
    if fund_table is not None:
        for row in fund_table.findChildren('tr'):
            record = row.findChildren('td')
            key = record[1].get_text()
            value = record[2].get_text()
            fncl_data[key] = value
    fncl_data['Company'] = name
    FIN_DICT.append(fncl_data)
    if len(FIN_HEADER) > 0:
        FIN_HEADER = list(set(FIN_HEADER+list(fncl_data.keys())))
    else:
        FIN_HEADER = list(fncl_data.keys())
    fncl_data = {}
    FUND_FOUND_DF = pd.DataFrame(columns=FIN_HEADER)
    for dictItem in FIN_DICT:
        FUND_FOUND_DF = FUND_FOUND_DF.append(dictItem, ignore_index=True)
FUND_FOUND_DF.to_csv("DISTRIBUTION_FUND_FOUND_DF.csv", index=False,encoding='utf-8-sig')
        
    
#bonus table
bonus_data = {}
BNS_DICT = []
BNS_HEADER = []
for link in found_links:
    #print(link)
    driver.get(link)
    html_content = driver.execute_script('return document.body.innerHTML')
    soep = BeautifulSoup(html_content, 'lxml')
    POSTS = soep.body.find('div',class_='col-xs-12 col-sm-8 col-md-9 col-lg-9')
    if POSTS is not None:
        name = POSTS.find('h1').get_text()
        print(name)
    funding = soep.find('section', id='ico-time-cont') 
    bonus_table = funding.find(id='det-bns-tbl')
    if bonus_table is not None:
        for row in bonus_table.findChildren('tr'):
            #print(row)
            record = row.findChildren('td')
            key = record[1].get_text()
            value = record[2].get_text()
            bonus_data[key] = value
    bonus_data['Company'] = name
    BNS_DICT.append(bonus_data)
    if len(BNS_HEADER) > 0:
        BNS_HEADER = list(set(BNS_HEADER+list(bonus_data.keys())))
    else:
        FIN_HEADER = list(bonus_data.keys())
    bonus_data = {}
    BONUS_FOUND_DF = pd.DataFrame(columns=BNS_HEADER)
    for dictItem in BNS_DICT:
        BONUS_FOUND_DF = BONUS_FOUND_DF.append(dictItem, ignore_index=True)
BONUS_FOUND_DF.to_csv("BONUS_FOUND_DF.csv", index=False,encoding='utf-8-sig')
        
#roadmap
ROAD_MAP_HEADER = ['Company Name','Timeline','Status']  
FOUND_ROUNDMAP_DF = pd.DataFrame(columns=ROAD_MAP_HEADER)
for link in found_links:
    #print(link)
    driver.get(link)
    html_content = driver.execute_script('return document.body.innerHTML')
    soep = BeautifulSoup(html_content, 'lxml')
    POSTS = soep.body.find('div',class_='col-xs-12 col-sm-8 col-md-9 col-lg-9')
    if POSTS is not None:
        name = POSTS.find('h1').get_text()
        print(name)
    roadmap = soep.find('section', id='ico-roadmap-cont')
    if roadmap is not None:
        road_table = roadmap.find(id='rd-map-cont')
        if road_table is not None:
            for row in road_table.findChildren('p'):
                record = row.find('span')
                timeline = record.get_text()
                data = record.next_sibling.string.strip()
                FOUND_ROUNDMAP_DF = FOUND_ROUNDMAP_DF.append({'Company Name':name,
                                                              'Timeline':timeline,
                                                              'Status':data},ignore_index = True)
FOUND_ROUNDMAP_DF.to_csv("FOUND_ROADMAP.csv", index=False,encoding='utf-8-sig')   

    
#TEAM
TEAM_HEADER = ['Company Name','Member Name','Member Role','Social Media Link','Social Media']  
FOUND_TEAM_DF = pd.DataFrame(columns=TEAM_HEADER)
for link in found_links:
    #print(link)
    driver.get(link)
    html_content = driver.execute_script('return document.body.innerHTML')
    soep = BeautifulSoup(html_content, 'lxml')
    POSTS = soep.body.find('div',class_='col-xs-12 col-sm-8 col-md-9 col-lg-9')
    if POSTS is not None:
        name = POSTS.find('h1').get_text()
        print(name)
    team = soep.find('section', id='ico-team-cont')
    #print(team)
    if team is not None:
        for t in team.find_all(class_='ico-team-unit'):
            det = t.find('h4')
            member_name = det.get_text()
            member_role = det.find_next_sibling('p').get_text()
            print(member_name)
            print(member_role)
            link = t.find('span', class_='smry-links')
            tag = link.find_all(class_=True)
            if tag:
                social_link = link.find('a')['href']
                #social_link = link.find('a')
                print(social_link)
                social_profile = link.find('a')['title']
                print(social_profile)
            else:
                social_link = ""
                social_profile = ""
            FOUND_TEAM_DF = FOUND_TEAM_DF.append({'Company Name':name,
                                            'Member Name':member_name,
                                            'Member Role':member_role,
                                            'Social Media Link':social_link,
                                            'Social Media':social_profile }, ignore_index=True)
FOUND_TEAM_DF.to_csv("FOUND_TEAM.csv", index=False,encoding='utf-8-sig') 



Twitter_Headers = ['Company','Date','Followers','Tweets']
Telegram_Headers = ['Company','Date', 'Subscribers']
Youtube_Headers = ['Company','Date', 'Subscribers', 'Videos']
Reddit_Headers = ['Company','Date', 'Link karma', 'Comment karma']
Github_Headers = ['Company','Date', 'Commits']
Facebook_Headers = ['Company','Date', 'Fans', 'Posts']
BitcoinTalk_Headers = ['Company','Date', 'Posts', 'Views']
Alexa_Headers = ['Company','Date', 'Worldwide rank']

All_Twitter_Stat = pd.DataFrame(columns=Twitter_Headers)
All_Telegram_Stat = pd.DataFrame(columns=Telegram_Headers)
All_Youtube_Stat = pd.DataFrame(columns=Youtube_Headers)
All_Reddit_Stat = pd.DataFrame(columns=Reddit_Headers)
All_Github_Stat = pd.DataFrame(columns=Github_Headers)
All_Facebook_Stat = pd.DataFrame(columns=Facebook_Headers)
All_BitcoinTalk_Stat = pd.DataFrame(columns=BitcoinTalk_Headers)
All_Alexa_Stat = pd.DataFrame(columns=Alexa_Headers)
    
for link in found_links:
#for link in ['https://foundico.com/ico/data-choice.html']:
#for link in ['https://foundico.com/ico/quifas.html']:
    #print(link)
    driver.get(link)
    html_content = driver.execute_script('return document.body.innerHTML')
    soep = BeautifulSoup(html_content, 'lxml')
    company_name = soep.body.find('div',class_='col-xs-12 col-sm-8 col-md-9 col-lg-9').find('h1').get_text()
    print(company_name)
    chart_scripts = soep.body.find_all('script', type='text/javascript', text=re.compile("Chart"))
    
    Twitter_Stat = pd.DataFrame(columns=Twitter_Headers)
    Telegram_Stat = pd.DataFrame(columns=Telegram_Headers)
    Youtube_Stat = pd.DataFrame(columns=Youtube_Headers)
    Reddit_Stat = pd.DataFrame(columns=Reddit_Headers)
    Github_Stat = pd.DataFrame(columns=Github_Headers)
    Facebook_Stat = pd.DataFrame(columns=Facebook_Headers)
    BitcoinTalk_Stat = pd.DataFrame(columns=BitcoinTalk_Headers)
    Alexa_Stat = pd.DataFrame(columns=Alexa_Headers)
    
    for chart in chart_scripts:
        chart_data = chart.text
        parsed = js2xml.parse(chart_data)
#        print(js2xml.pretty_print(parsed))
        chart_name = parsed.xpath("//var//arguments//string/text()")[0] # 'ic-twitter-stat'
#        print(chart_name)
        if chart_name == 'ic-twitter-stat': 
            for d in parsed.xpath("//property[@name='data']//property[@name='labels']"):
                Twitter_Stat['Date'] = d.xpath(".//array/string/text()")
            for d in parsed.xpath("//property[@name='datasets']//array//object"):
                variable = d.xpath(".//property[@name='label']//string/text()")[0]
                Twitter_Stat[variable] = [d.xpath(".//property[@name='data']//array/number/@value")][0]
            Twitter_Stat['Company'] = company_name
            All_Twitter_Stat = All_Twitter_Stat.append(Twitter_Stat, ignore_index = True)
        elif chart_name == 'ic-telegram-stat':
            for d in parsed.xpath("//property[@name='data']//property[@name='labels']"):
                Telegram_Stat['Date'] = d.xpath(".//array/string/text()")            
            for d in parsed.xpath("//property[@name='datasets']//array//object"):
                variable = d.xpath(".//property[@name='label']//string/text()")[0]
                Telegram_Stat[variable] = [d.xpath(".//property[@name='data']//array/number/@value")][0]
            Telegram_Stat['Company'] = company_name
            All_Telegram_Stat = All_Telegram_Stat.append(Telegram_Stat, ignore_index = True)
        elif chart_name == 'ic-youtube-stat':
            for d in parsed.xpath("//property[@name='data']//property[@name='labels']"):
                Youtube_Stat['Date'] = d.xpath(".//array/string/text()")            
            for d in parsed.xpath("//property[@name='datasets']//array//object"):
                variable = d.xpath(".//property[@name='label']//string/text()")[0]
                # To handle no subscriber data for Data Choice (DCT)
                if(len([d.xpath(".//property[@name='data']//array/number/@value")][0]) != 0):
                    Youtube_Stat[variable] = [d.xpath(".//property[@name='data']//array/number/@value")][0]
            Youtube_Stat['Company'] = company_name
            All_Youtube_Stat = All_Youtube_Stat.append(Youtube_Stat, ignore_index = True)
        elif chart_name == 'ic-reddit-stat':
            for d in parsed.xpath("//property[@name='data']//property[@name='labels']"):
                Reddit_Stat['Date'] = d.xpath(".//array/string/text()")            
            for d in parsed.xpath("//property[@name='datasets']//array//object"):
                variable = d.xpath(".//property[@name='label']//string/text()")[0]
                Reddit_Stat[variable] = [d.xpath(".//property[@name='data']//array/number/@value")][0]
            Reddit_Stat['Company'] = company_name
            All_Reddit_Stat = All_Reddit_Stat.append(Reddit_Stat, ignore_index = True)
        elif chart_name == 'ic-github-stat':
            for d in parsed.xpath("//property[@name='data']//property[@name='labels']"):
                Github_Stat['Date'] = d.xpath(".//array/string/text()")            
            for d in parsed.xpath("//property[@name='datasets']//array//object"):
                variable = d.xpath(".//property[@name='label']//string/text()")[0]
                Github_Stat[variable] = [d.xpath(".//property[@name='data']//array/number/@value")][0]
            Github_Stat['Company'] = company_name
            All_Github_Stat = All_Github_Stat.append(Github_Stat, ignore_index = True)
        elif chart_name == 'ic-facebook-stat':
            for d in parsed.xpath("//property[@name='data']//property[@name='labels']"):
                Facebook_Stat['Date'] = d.xpath(".//array/string/text()")            
            for d in parsed.xpath("//property[@name='datasets']//array//object"):
                variable = d.xpath(".//property[@name='label']//string/text()")[0]
                Facebook_Stat[variable] = [d.xpath(".//property[@name='data']//array/number/@value")][0]
            Facebook_Stat['Company'] = company_name
            All_Facebook_Stat = All_Facebook_Stat.append(Facebook_Stat, ignore_index = True)
        elif chart_name == 'ic-bitcointalk-stat':
            for d in parsed.xpath("//property[@name='data']//property[@name='labels']"):
                BitcoinTalk_Stat['Date'] = d.xpath(".//array/string/text()")            
            for d in parsed.xpath("//property[@name='datasets']//array//object"):
                variable = d.xpath(".//property[@name='label']//string/text()")[0]
                BitcoinTalk_Stat[variable] = [d.xpath(".//property[@name='data']//array/number/@value")][0]
            BitcoinTalk_Stat['Company'] = company_name
            All_BitcoinTalk_Stat = All_BitcoinTalk_Stat.append(BitcoinTalk_Stat, ignore_index = True)
        elif chart_name == 'ic-alexa-stat':
            for d in parsed.xpath("//property[@name='data']//property[@name='labels']"):
                # To handle invalid label 'Array' for quifas (QFS)
                r = re.compile("^[0-9]+\.[0-9]*$")
                Alexa_Stat['Date'] = list(filter(r.match, d.xpath(".//array/string/text()")))
               # Alexa_Stat['Date'] = d.xpath(".//array/string/text()")            
            for d in parsed.xpath("//property[@name='datasets']//array//object"):
                variable = d.xpath(".//property[@name='label']//string/text()")[0]
                Alexa_Stat[variable] = [d.xpath(".//property[@name='data']//array/number/@value")][0]
            Alexa_Stat['Company'] = company_name
            All_Alexa_Stat = All_Alexa_Stat.append(Alexa_Stat, ignore_index = True)
        else:
            print(chart_name)
                


All_BitcoinTalk_Stat.to_csv("Alexa.csv", index=False,encoding='utf-8-sig')
All_Alexa_Stat.to_csv("Alexa.csv", index=False,encoding='utf-8-sig')
All_Twitter_Stat.to_csv("Twitter.csv", index=False,encoding='utf-8-sig')
All_Telegram_Stat.to_csv("Telegram.csv", index=False,encoding='utf-8-sig')
All_Youtube_Stat.to_csv("YouTube.csv", index=False,encoding='utf-8-sig')
All_Reddit_Stat.to_csv("Reddit.csv", index=False,encoding='utf-8-sig')
All_Github_Stat.to_csv("Github.csv", index=False,encoding='utf-8-sig')
All_Facebook_Stat.to_csv("Facebook.csv", index=False,encoding='utf-8-sig')