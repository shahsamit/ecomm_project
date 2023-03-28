#Import all relevant libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


    #Load the file into pandas
df = pd.read_excel("Online_Retail.xlsx")

    #check first 5 rows
df.head()

df.replace(to_replace='United Kingdom', value='India', inplace=True)
df.head()
df.info()
    #Check for null values
df.isna().sum()
    #Drop all rows with a null value
df.dropna(inplace=True)
len(df)
    #Convert the InvoiceNo column to string
df["InvoiceNo"] = df["InvoiceNo"].astype('str')

    #Remove rows with invoices that contain a "C"
df = df[~df["InvoiceNo"].str.contains("C")]

len(df)

top10 = df["Country"].value_counts().head(10)

def getdata():
    return(top10)


basket = df[df['Country'] =="India"]\
        .groupby(['InvoiceNo', 'Description'])["Quantity"]\
        .sum().unstack()\
        .reset_index().fillna(0)\
        .set_index("InvoiceNo")

basket.head()
#Create function to hot encode the values
def encode_values(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

#Apply function to data
basket_encoded = basket.applymap(encode_values)

#filter for only invoices with 2 or more items
basket_filtered = basket_encoded[(basket_encoded > 0).sum(axis=1) >= 2]

#Generate the frequent itemsets
frequent_itemsets = apriori(basket_filtered, min_support=0.03, use_colnames=True).sort_values("support",ascending=False)

def frequentproducts():
    return frequent_itemsets.head(10)
#Apply association rules
assoc_rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1).sort_values("lift",ascending=False).reset_index(drop=True)

def getassoc_rules():
    return assoc_rules
