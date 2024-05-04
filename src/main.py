from database import *
import pandas as pd
import random


init_db()
print ("Hello World")
product = get_product("aaaa")

print ("The product is: ", product)
print ("Heeeeeeeeee")

#data = pd.read_csv("../products.csv", delimiter=';')
#data["stock"]= [random.randint(50,120) for _ in range(len(data))]
#records = data.to_dict('records')
#for record in records:
    #doc_id = record["id"]
    #del record["id"]
    #add_data(str(doc_id),record)
