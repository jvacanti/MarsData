
# coding: utf-8

# In[79]:


#Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd


# In[18]:

def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    return browser

def scrape():
    browser = init_browser()


    results = {}


# ##### NASA Mars News

# In[19]:


    news_url = "https://mars.nasa.gov/news/"


# In[20]:



    browser.visit(news_url)


# In[21]:


    soup = BeautifulSoup(browser.html, 'html.parser')


    # In[22]:


    news_title = soup.find('div', class_='content_title').string
    news_title


    # In[23]:


    news_p = soup.find('div', class_='article_teaser_body').string
    news_p
    
    results["news_title"] = news_title
    results["news_p"] = news_p


# ##### Mars Space Images

# In[54]:


    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"


    # In[55]:


    browser.visit(image_url)
    soup = BeautifulSoup(browser.html, 'html.parser')


    # In[57]:


    for link in soup.find_all('a', class_="button fancybox"):
        link_text = link.get('data-fancybox-href')

    print(link_text)


    # In[58]:


    featured_image_url = "https://www.jpl.nasa.gov" + link_text
    featured_image_url
    
    results["featured_image_url"] = featured_image_url


# ##### Mars Weather

# In[59]:


    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    soup = BeautifulSoup(browser.html, 'html.parser')


    # In[63]:


    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    mars_weather

    results["mars_weather"] = mars_weather


    # ##### Mars Facts

    # In[70]:


    fact_url = "http://space-facts.com/mars/"
    browser.visit(fact_url)
    soup = BeautifulSoup(browser.html, 'html.parser')


    # In[73]:


    categories = []

    for cat in soup.find_all('td', class_='column-1'):
        categories.append(cat.find('strong').text)

    categories


# In[75]:


    facts = []

    for fact in soup.find_all('td', class_="column-2"):
        facts.append(fact.text)

    facts


    # In[87]:


    mars_factoids = pd.DataFrame({"Category":categories, "Value":facts})
    #mars_factoids.set_index("Category", inplace=True)
    mars_factoids

    table=mars_factoids.to_html()
    table=table.replace("\n","")

    results["facts"] = table

# ##### Mars Hemisperes

# In[77]:


    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    soup = BeautifulSoup(browser.html, 'html.parser')


    # In[89]:


    hemisphere_image_urls = []

    for hemi in soup.find_all("div", class_="item"):
        for href in hemi.find_all('img', class_='thumb'):
            link_text = href.get('src')
            
        hemisphere_image_urls.append({'title': hemi.find('h3').text, 
                                    'image':hemi_url.split('/search')[0] + link_text
                                    })
        
    hemisphere_image_urls
    
    results["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()

    return results

