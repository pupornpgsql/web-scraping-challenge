import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News
    url = "https://redplanetscience.com/#"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('div', class_ = 'content_title').text
    paragraph = soup.find('div', class_ = 'article_teaser_body').text

    # JPL Mars Space Images - Featured Image
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_url = soup.find('a', class_ = "showimg fancybox-thumbs")['href']
    featured_image_url = f"{url}{image_url}"

    # Mars Facts Table
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    mars_facts_table = tables[0]
    mars_facts_table.columns = mars_facts_table.iloc[0]
    mars_facts_table = mars_facts_table.iloc[1:, ]
    mars_facts_table.set_index("Mars - Earth Comparison", inplace = True)
    html_table = mars_facts_table.to_html(classes = "table table-striped")

    # Mars Hemispheres Data
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemi_list = []
    hemis = soup.find_all('h3')

    for hemi in hemis:
        hemi_name = hemi.text
        hemi_list.append(hemi_name)

    del hemi_list[len(hemi_list) - 1]

    # Hemisphere list to store dictionaries in

    hemisphere_image_urls = []

    # For loop to retrieve image URL and hemisphere name
    for hemi in hemi_list:
        
        # Retrieve html to know what I'm scraping for
        browser.links.find_by_partial_text(hemi).click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemisphere_dict = {}

        # Extract the title
        hemi_title = soup.find('div', class_ = 'cover')
        hemi_title = hemi_title.h2.text.split(' ')[:-1]
        hemi_title = " ".join(hemi_title)
        hemisphere_dict['title'] = hemi_title

        # Extract image url
        image_url = soup.find('ul').li.a['href']
        hemisphere_dict['img_url'] = f"{url}{image_url}"
        
        # Append dict to list
        hemisphere_image_urls.append(hemisphere_dict)
        
        # Go back to main page 
        browser.links.find_by_partial_text('Back').click()

    scrape_results = {
        "news_title": title,
        "news_paragraph": paragraph,
        "featured_image": featured_image_url,
        "facts_table": html_table,
        "hemi_image_urls": hemisphere_image_urls
        }

    browser.quit()

    return scrape_results