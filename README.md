# Project 1

Web Programming with Python and API's
requirements : 1)Flask
               2) database (I used postgresql hosted on heroku)
               3) Goodreads Account for accesing goodread's api
login using your credentials.
search amongst 5000 books by their title,author or isbn
from the results choose any of the books. You will be taken to that respective book's page
feel free to post a review and rate that book out . 
on the same page average rating and total ratings of that book received by the goodreads api will also be posted.
i have also included my own  websites api to directly give u information in json format
  ex:-the url "/api/<string:isbn>"
  will query the database and will give the following response.
  {
            "title": apires.title,
            "author": apires.author,
            "year": apires.year,
            "isbn": apires.isbn
        }
