from msilib import _directories
from os import name
import os
from pickle import NONE
from turtle import end_fill
from bs4 import BeautifulSoup
import pandas as pd
import requests

from cv2 import imread
from requests import request






# This function will return List of All topics title--
def topic_title_tags(doc):

    topic_title_tag = doc.find_all('p',{'class':'f3 lh-condensed mb-0 mt-1 Link--primary'})
    all_topics = [item.text.strip() for item in topic_title_tag] # making a list of topic titles

    return all_topics


#This function will return description about all topics 
def topic_desc_tags(doc):

    desc_tag = doc.find_all('p',{'class':'f5 color-fg-muted mb-0 mt-1'})
    all_desc = [item.text.strip() for item in desc_tag]

    return all_desc


#This function will return URL of that topics --
def topic_url_tags(doc):

    topic_url_tags= doc.find_all('a', {'class':'no-underline flex-1 d-flex flex-column'})
    base_url = 'https://www.github.com/'
    topic_url=[base_url + item['href'].strip() for item in topic_url_tags]

    return topic_url



#This function will convert start of repository into Integer 
# 89.6k --> 89600 and 800-> 800
def star_to_int(strA):
    if(strA[-1] == 'k'):
        return int(float(strA[:-1])*1000)
    else:
        return int(strA)


#This is the main Function of this program that will scrap all information about 'https://github.com'
#This function will return Pandas dataframe of information that will contain Topic_title , Topic_description and URL of title
def main_scrap():
    main_url ='https://github.com/topics'
    request = requests.get(main_url)        

    #if requset status failed then program will stop   
    if request.status_code != 200:              
        raise Exception("SomeThing Went Wrong ")


    # using Beautiful Soup to parse the data into HTML
    doc = BeautifulSoup(request.text ,'html.parser') 

    #calling the topic_title_tags function , topic_desc_tags 
    # function and topic_url_tags function in dictionary to scrap data 
    topic_dic = {'Titles': topic_title_tags(doc), 'Description':topic_desc_tags(doc), 'Topics URL': topic_url_tags(doc)}


    # using pandas to convert dictionary to pandas dataframe--
    topic_df = pd.DataFrame(topic_dic)
    return topic_df


# This function is whole scraping function for titles 
# This will Take URL of topic on github and will return pandas dataframe
#  of Top user and his famous repository in that topic along with stars and links of that repository 

def scrap_topic(topic_url):
    #requsting for input URL 
    topic_request = requests.get(topic_url)
    #using Beautiful soup library to parse the html file 
    topic_doc= BeautifulSoup(topic_request.text, 'html.parser')


    #extractin tag for top user and his repository along with repository's URL
    name_repo_url_tag = topic_doc.find_all('h3',{'class':'f3 color-fg-muted text-normal lh-condensed'})
    #extraction Star of top Repositories
    star_tag = topic_doc.find_all('span',{'id':'repo-stars-counter-star'})

    #making a dictionary that will hold all the information about that website
    topic_repo_dict = {'user_name': [], 'Repo_name': [], 'star':[],'user_repo_url':[]}

    #using loop filling the dictionary with website's data
    for i in range(len(name_repo_url_tag)):
        item = name_repo_url_tag[i]
        star_item = star_tag[i]
        star_of_repo=star_to_int(star_item.text.strip())
        a_tag= item.find_all('a')
        name_tag = a_tag[0].text.strip()
        repo_tag = a_tag[1].text.strip()
        url_of_repo = a_tag[1]['href']
        topic_repo_dict['user_name'].append(name_tag)
        topic_repo_dict['Repo_name'].append(repo_tag)
        topic_repo_dict['user_repo_url'].append('https://www.github.com' + url_of_repo)
        topic_repo_dict['star'].append(star_of_repo)
    
    #convertion dictionay into pandas dataframe
    topic_repo_url_pd = pd.DataFrame(topic_repo_dict)


    return topic_repo_url_pd


#This function will scrap top repository of all titles that will be present on 'https://github.com/topics' 
# and it will create CSV file for all topics and will store it in DATA folder that will be created by this function itself


def scrap_topics_repo():
    #storing panda dataframe of 'https://github.com/topics'
    topics_pd = main_scrap()

    # Creating A folder Named DATA that will hold all scrapping information
    os.mkdir('DATA')           
    for ind in topics_pd.index:
        print('extraction data of :' , topics_pd['Titles'][ind])
        #creating path to Store all data 
        fname = 'DATA/'+topics_pd['Titles'][ind] + '.csv'
        scrap_topic(topics_pd['Topics URL'][ind]).to_csv(fname , index=None)


scrap_topics_repo()




'''

link_files = 

# print((link_files))
all_topic = [topic.text.strip() for topic in topic_title_tag]
all_desc = [item.text.strip() for item in desc_tag]
all_link = [item['href'].strip() for item in link_files]
base = 'https://github.com'
i=0
for item in all_link:
    item = base + item
    all_link[i]=item
    i += 1
    


topic_dic ={'Topics':all_topic, 'TagLine': all_desc, 'Links':all_link}


akash = pd.DataFrame(topic_dic)

akash.to_csv('topics.csv',index=None )
# print((akash))

topic_url = all_link[0]







'''

'''
for i in range(30):
    topic_url=all_link[i]
    topic_url_df=pd.DataFrame(url_scrapping(topic_url))
    url_scrapping(topic_url)
    csv_name ='page' + str(i)+'.csv'
    topic_url_df.to_csv(csv_name, index=None)

'''








'''




topic_doc = BeautifulSoup(topic_request.text , 'html.parser')

# print(len(topic_doc))

username = topic_doc.find_all('h3',{'class':'f3 color-fg-muted text-normal lh-condensed'})

star_tag = topic_doc.find_all('span',{'id':'repo-stars-counter-star'})
# print(len(star_tag))





for item in star_tag:
    topic_repo_dict['star'].append(star_to_int(item.text.strip()))

for item in username:
    a_tag = item.find_all('a')
    topic_repo_dict['user_name'].append(a_tag[0].text.strip())
    topic_repo_dict['Repo_name'].append(a_tag[1].text.strip())
    topic_repo_dict['user_repo_url'].append(base + a_tag[1]['href'])


# print(topic_repo_dict)

topic_repo_df = pd.DataFrame(topic_repo_dict)

print(topic_repo_df)

topic_repo_df.to_csv('topic_details.csv', index=None) '''