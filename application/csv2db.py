import pandas as pd
from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker, scoped_session

df = pd.read_csv("application/static/items.csv")
df["id"] = df.index
df["done"] = 0

db_name = "momo.db"

engine = create_engine("sqlite:///" + db_name, echo=False)
df.to_sql("items", engine, if_exists='replace')
