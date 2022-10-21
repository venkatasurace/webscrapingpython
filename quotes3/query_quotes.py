import sqlite3


def connect_and_fetch_from_db(query,data = None):
  connection = sqlite3.connect("quotes.db")
  cursor = connection.cursor()

  if data != None:
    cursor.execute(query,data)
  else:
    cursor.execute(query)
    
  query_response = cursor.fetchall()
  connection.close()
  return query_response

def get_total_quotes_in_website():

  query = ("""
      SELECT 
          COUNT(id) as tota_quotes 
      FROM 
          quotes;
    """)
  total_quotes = connect_and_fetch_from_db(query)
  print(" ")
  print(f'Total Number of quotations in the website: {total_quotes[0][0]}')
  
def total_quotes_by_author(author_name):

  query = ("""
      SELECT 
          COUNT(id) as total_quotes
      FROM 
          quotes
      WHERE author_id = (
              SELECT id
              FROM authors
              WHERE name = ?
            )
      GROUP BY author_id;
     """)
  total_quotes = connect_and_fetch_from_db(query,[author_name])
  print(" ")
  print(f'Total No of Quotes by {author_name}: {total_quotes[0][0]}')

def authors_with_maximum_no_of_quotes(number):
  
  query = ("""
      SELECT 
          authors.name,count(quotes.id) AS total_quotes
      FROM 
        quotes INNER JOIN authors on quotes.author_id = authors.id
      GROUP BY authors.name 
      ORDER BY total_quotes DESC, authors.name ASC
      LIMIT ?;
  """)
  total_quotes_by_author = connect_and_fetch_from_db(query,[number])
  for author_name,no_of_quotes in total_quotes_by_author:
    print("")
    print(f'{author_name.strip(" ")}\t|  {no_of_quotes}')

def max_min_avg_no_of_tags():
 
  query = ("""
    SELECT 
      MAX(no_of_tags),
      MIN(no_of_tags),
      round(AVG(no_of_tags),2)
    FROM (
      SELECT count(tag_id) as no_of_tags
      FROM quotes LEFT JOIN quote_tag on quotes.id = quote_tag.quote_id
      GROUP BY quote_id
    );
  """)
  max_min_avg_of_tags = connect_and_fetch_from_db(query)
  print(" ")
  print(f'MAX No_of_Tags : {max_min_avg_of_tags[0][0]}')
  print(f'MIN No_of_Tags : {max_min_avg_of_tags[0][1]}')
  print(f'AVG No_of_Tags : {max_min_avg_of_tags[0][2]}')


get_total_quotes_in_website()

total_quotes_by_author("Albert Einstein")

authors_with_maximum_no_of_quotes(5)

max_min_avg_no_of_tags()