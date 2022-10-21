import requests
from bs4 import BeautifulSoup
import json



def request_and_soup_page(page_url):

    html_page = requests.get(page_url).content
    soup = BeautifulSoup(html_page,'html.parser')
    return soup

def create_authors_dict(each_author_details):
  
  authors_name  =each_author_details[0]
  authors_born_details = each_author_details[1]
  authors_reference_link = each_author_details[2]
  authors_temp_dict={
                      'name':authors_name,
                      "born":authors_born_details,
                      "reference":authors_reference_link
                    }
  return authors_temp_dict

def create_authors_dict_list(authors_details):
  print("creating of authors dict list is started")
  authors_list = []
  authors_dict = {}
  for each_author_details in authors_details:
      authors_name  =each_author_details[0]
      authors_dict[authors_name] = create_authors_dict(each_author_details)

  for author_name,each_authors_dict in authors_dict.items():
    authors_list.append(each_authors_dict)
  print("authors_dict_list is created")
  return authors_list

def get_authors_dob_details(author_page_link):
  authors_deatils = request_and_soup_page(author_page_link)
  dob_of_author = authors_deatils.find("span",class_="author-born-date").text 
  birth_place_of_author = authors_deatils.find("span",class_="author-born-location").text
  author_born_details = f'{dob_of_author} {birth_place_of_author}'
  return author_born_details

def get_authors_details(quotes_container):
  print("getting authors details")
  authors_details_list = []
  for each_author_details in quotes_container:
    scraped_author_page_url = each_author_details.find("a")["href"]
    author_name = each_author_details.find("small",class_="author").text
    author_page_link = f'http://quotes.toscrape.com{scraped_author_page_url}'
    authors_born_details = get_authors_dob_details(author_page_link)
    authors_details_list.append((author_name,authors_born_details,author_page_link))
  print("Getting authors detailes is completed")
  return authors_details_list

def scrape_authors_page(quotes_containers):
  print("scraping of authors page is started")
  authors_details = get_authors_details(quotes_containers)
  authors_dict_list = create_authors_dict_list(authors_details)
  print("scraping authors page is completed")
  return authors_dict_list

def create_quotes_dict_list(quotes_conatiners ):
  print("creating of quotes_dict_list is started")
  quotes_in_all_pages= []
  for each_quote in quotes_conatiners:
    quotes_dict = {}
    quotes_dict["quote"] = each_quote.find("span",class_="text").text.strip(" ,”,“")
    quotes_dict["author"] = each_quote.find("small",class_="author").text.strip(" ")
    tags = []
    for each_tag in each_quote.find_all("a",class_="tag"):
      tags.append(each_tag.text.strip(" "))
    quotes_dict["tags"] = tags
    quotes_in_all_pages.append(quotes_dict)
  print("quotes_dict_list is created")
  return quotes_in_all_pages

def get_all_quotes_containers(urls_list):

  quotes_containers = []
  for page_url in urls_list:
    soup = request_and_soup_page(page_url)
    quotes_in_each_page = soup.find_all("div",class_="quote")
    quotes_containers.extend(quotes_in_each_page)
  print("All quotes containers are fetched")
  return quotes_containers
    
def generate_quotes_page_urls():
  quotes_page_urls_list = []
  page_no = "/page/1/"
  while True:
    url = f'http://quotes.toscrape.com/{page_no}'
    html_page = requests.get(url).content
    soup = BeautifulSoup(html_page,'html.parser')
    li_tag = soup.find("li",class_="next")
    quotes_page_urls_list.append(url)
    if li_tag == None:
      break
    else:
      
      page_no = li_tag.find('a')['href']
  print("Quotes_urls are generated")
  return quotes_page_urls_list

def scrape_quotes_page():
  print("scraping of quotes_page started ")
  quotes_page_urls_list = generate_quotes_page_urls()
  quotes_containers = get_all_quotes_containers(quotes_page_urls_list)
  quotes_in_all_pages = create_quotes_dict_list(quotes_containers )
  print("scraping of quotes page completed")
  
  return quotes_containers,quotes_in_all_pages

def scrape_pages():
  print("scraping of pages is started ")
  quotes_containers,quotes_in_all_pages = scrape_quotes_page()
  authors_dict = scrape_authors_page(quotes_containers)
  print("Scraping of pages is completed")
  return quotes_in_all_pages,authors_dict

def create_quotes_json():
  quotes_dict_list,authors_dict_list = scrape_pages()

  quotes_and_authors_dict = {"quotes":quotes_dict_list,"authors":authors_dict_list}
  quotes_json = json.dumps(quotes_and_authors_dict,indent=2)

  
  with open("quotes.json","w") as f:
    f.write(quotes_json)

create_quotes_json()