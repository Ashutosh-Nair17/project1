import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
		f=open("books.csv")
		reader = csv.reader(f)
		for isbn, title, author,year in reader:
			db.execute("INSERT INTO books(isbn, title, author,year) VALUES (:x,:y,:z,:a)",
                    {"x": isbn, "y": title, "z": author,"a":year})
			print(f"Added {title}")
		try :	
			db.commit()
		except:
			print("something went wrong")

if __name__ == "__main__":
    main()
