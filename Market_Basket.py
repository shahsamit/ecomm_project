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
print("Check the distribution of transactions per country")#
top10 = df["Country"].value_counts().head(10)
print(top10)
print("Create a pie chart to show distribution of transactions")#
plt.figure(figsize=[8,8])
#print(type(plt.pie(top10,labels=top10.index, autopct = '%0.0f%%',labeldistance=1.3)))
plt.title("Distribution of Transactions by Country")
plt.show()
print("configuring a pie chart to show distribution of transactions")#
#Group, sum, unstack and set index of dataframe
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

basket_encoded
#filter for only invoices with 2 or more items
basket_filtered = basket_encoded[(basket_encoded > 0).sum(axis=1) >= 2]

basket_filtered

#Generate the frequent itemsets
frequent_itemsets = apriori(basket_filtered, min_support=0.03, use_colnames=True).sort_values("support",ascending=False)
frequent_itemsets.head(10)

#Apply association rules
assoc_rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1).sort_values("lift",ascending=False).reset_index(drop=True)
assoc_rules
