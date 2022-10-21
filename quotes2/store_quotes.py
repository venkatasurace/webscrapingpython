import sqlite3
import json


def get_quotes_json_file():
  with open("quotes.json","r") as f:
    quotes_file = f.read()
    quotes_file = json.loads(quotes_file)
  print("Quotes File Fetched")
  return quotes_file

def create_tags_dict_from_quotes_json_file(quotes_file):
  tags_dict = {}
  tags_set = set()
  
  for each_quote in quotes_file["quotes"]:
    for each_tag in each_quote["tags"]:
      tags_set.add(each_tag)
  
  tags= sorted(list(tags_set))
  tag_id = 101
  for tag in tags:
    tags_dict[tag_id] = tag
    tag_id += 1

  return tags_dict

def create_quotes_dict_from_quotes_json_file(quotes_file):
  quotes_dict = {}
  quote_id = 201
  for each_quote in quotes_file["quotes"]:
    quotes_dict[quote_id] = each_quote
    quote_id += 1
  return quotes_dict

def create_authors_dict_from_quotes_json_file(quotes_file):
  authors_dict = {}
  author_id = 301
  for author in quotes_file["authors"]:
    authors_dict[author_id] = author
    author_id += 1
  return authors_dict

def create_tag_ids_list(quote_dict,tags_dict):
    tag_ids_list = []
     
    for tag_in_quote in quote_dict["tags"]: 
      for tag_id,tag_in_tags_dict in tags_dict.items():
        if tag_in_quote == tag_in_tags_dict:
          tag_ids_list.append(tag_id)
    return tag_ids_list
         
def create_quote_tag_id_dict(quotes_dict,tags_dict):
  quote_tag_ids_dict = {}
  for quote_id,quote in quotes_dict.items():
    if len(quote["tags"]) !=0: 
      tag_ids_list =create_tag_ids_list(quote,tags_dict)
      quote_tag_ids_dict[quote_id] = tag_ids_list

  return quote_tag_ids_dict

def enable_foriegn_key_constraints_in_db():
  connection = sqlite3.connect("quotes.db")
  print("Connected to db")
  cursor = connection.cursor()
  cursor.execute("PRAGMA foreign_keys = ON;")
  connection.commit()
  connection.close()

  print("Foreign Constraints Enabled")

def create_table_and_commit_to_db(sql_query):
  connection = sqlite3.connect("quotes.db")
  cursor = connection.cursor()
  cursor.execute(sql_query)
  connection.commit()
  connection.close()

def insert_data_and_commit_to_db(sql_query,data):
  connection = sqlite3.connect("quotes.db")
  cursor = connection.cursor()
  cursor.execute(sql_query,data)
  connection.commit()
  connection.close()
  
def create_authors_table():

  sql_query = ("""
      CREATE TABLE authors (
          id INTEGER NOT NULL PRIMARY KEY,
          name VARCHAR(250),
          born TEXT,
          reference TEXT
      );
  """)

  create_table_and_commit_to_db(sql_query)
  print("Author Table Created")

def create_tags_table():
  
  sql_query = ("""
      CREATE TABLE tags (
          id INTEGER NOT NULL PRIMARY KEY,
          tag TEXT
      );
  """)  

  create_table_and_commit_to_db(sql_query)
  print("Tags_table Created")

def create_quotes_table():

  sql_query = ("""
        CREATE TABLE quotes(
            id INTEGER NOT NULL PRIMARY KEY,
            quote TEXT,
            author_id INT); 
    """)

  create_table_and_commit_to_db(sql_query)
  print("quotes Table Created")

def create_quote_tag_table():

  sql_query=("""
          CREATE TABLE quote_tag (
              id INTEGER NOT NULL PRIMARY KEY,
              quote_id INTEGER,
              tag_id INTEGER,
              FOREIGN KEY (quote_id) REFERENCES quotes(id) ON DELETE CASCADE,
              FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE);
        """)
  create_table_and_commit_to_db(sql_query)
  print("Quote_tag Table Created")

def create_author_quote_table():

  sql_query = ("""
      CREATE TABLE author_quote(
          id INTEGER NOT NULL PRIMARY KEY,
          author_id INTEGER,
          quote_id INTEGER,
          FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE,
          FOREIGN KEY (quote_id) REFERENCES quote(id) ON DELETE CASCADE
      );
  """)
  create_table_and_commit_to_db(sql_query)
  print("Author_Quote Table created")

def insert_data_into_authors_table(authors_dict):

  for author_id,author_details in authors_dict.items():

    authors_data = [author_id,author_details["name"],author_details["born"],author_details["reference"]]
    
    sql_query = ("""
              INSERT INTO 
                  authors('id','name','born','reference') 
              VALUES
                  (?,?,?,?);
            """)
    insert_data_and_commit_to_db(sql_query,authors_data)

  print("Data Inserted Into Authors Table")

def insert_data_into_tags_tables(tags_dict):
  
  for tag_id,tag in tags_dict.items():
    tag_data = [tag_id,tag]

    sql_query =("""
            INSERT INTO 
                tags(id,'tag') 
            VALUES
                (?,?);
          """)

    insert_data_and_commit_to_db(sql_query,tag_data)

  print("Data Inserted Into Tags Table")

def insert_data_into_quotes_table(quotes_dict,authors_dict):
  for quote_id,each_quote in quotes_dict.items():
    quote = each_quote["quote"]
    for author_id,author_details in authors_dict.items():
      if each_quote["author"] == author_details["name"]:
        authors_id = author_id
    sql_query = ("""
              INSERT INTO 
                  quotes('id','quote','author_id')
              VALUES
                  (?,?,?);
            """)
    insert_data_and_commit_to_db(sql_query,[quote_id,quote,authors_id])
    author_id += 1
  print("Data Inserted Into Quotes Table")

def insert_data_into_quote_tag_table(quote_tag_ids_dict):
  
  for quote_id,tag_ids_list in quote_tag_ids_dict.items():
    for tag_id in tag_ids_list:

      sql_query = ("""
              INSERT INTO 
                  quote_tag('quote_id','tag_id') 
              VALUES
              (?,?);
          """)
      insert_data_and_commit_to_db(sql_query,[quote_id,tag_id])

  print("Data Inserted Into Quote_Tag Table")
      

def get_quotes_json_file_and_create_respective_dicts():
  quotes_file = get_quotes_json_file()
  tags_dict= create_tags_dict_from_quotes_json_file(quotes_file)
  quotes_dict = create_quotes_dict_from_quotes_json_file(quotes_file)
  authors_dict = create_authors_dict_from_quotes_json_file(quotes_file)
  quote_tag_ids_dict = create_quote_tag_id_dict(quotes_dict,tags_dict)

  return (tags_dict,quotes_dict,authors_dict,quote_tag_ids_dict)

def create_tables_in_db():
  enable_foriegn_key_constraints_in_db()
  create_tags_table()
  create_authors_table()
  create_quotes_table()
  create_quote_tag_table()

def insert_data_into_tables_in_db(extracted_data_from_quote_json):
  tags_dict,quotes_dict,authors_dict,quote_tag_ids_dict = extracted_data_from_quote_json
  insert_data_into_tags_tables(tags_dict)
  insert_data_into_authors_table(authors_dict)
  insert_data_into_quotes_table(quotes_dict,authors_dict)
  insert_data_into_quote_tag_table(quote_tag_ids_dict)

def extract_data_and_store_in_db():
  extracted_data_from_quote_json =  get_quotes_json_file_and_create_respective_dicts()
  create_tables_in_db()
  insert_data_into_tables_in_db(extracted_data_from_quote_json)
  
extract_data_and_store_in_db()