#!/usr/bin/env python
# coding: utf-8

# In[30]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


data=pd.read_csv("zomato.csv")


# In[3]:


data.head()


# In[4]:


data.shape


# In[5]:


data.isnull().sum()


# In[6]:


strings_to_remove = ['NEW', '-']

# Loop to remove strings
for i in range(len(data['rate'])):
    if isinstance(data['rate'][i], str) and data['rate'][i] in strings_to_remove:
        data.at[i, 'rate'] = np.nan


# In[7]:


mode_value = data['rate'].mode()[0] 
data['rate'].fillna(mode_value, inplace=True)


# In[8]:


mode_rest = data['rest_type'].mode()[0]
data['rest_type'].fillna(mode_rest, inplace=True)


# In[9]:


mode_dish = data['dish_liked'].mode()[0]
data['dish_liked'].fillna(mode_dish, inplace=True)


# In[10]:


mode_cost = data['approx_cost(for two people)'].mode()[0]
data['approx_cost(for two people)'].fillna(mode_cost, inplace=True)


# In[11]:


column_to_drop = 'url'
data = data.drop(columns=[column_to_drop])


# In[12]:


columns_to_drop = ['address', 'phone','menu_item','listed_in(city)']
data = data.drop(columns=columns_to_drop)


# In[99]:


column_to_drop = 'reviews_list'
data = data.drop(columns=[column_to_drop])


# In[105]:


column_to_drop = 'dish_liked'
data = data.drop(columns=[column_to_drop])


# In[13]:


data['rate'] = data['rate'].str.replace('/5', '')


# In[16]:


data['rate'] = data['rate'].astype(float)


# In[19]:


data['rate'] = data['rate'].round(1)


# In[23]:


data['rate'] = data['rate'].astype(int)


# In[24]:


data['name'] = data['name'].str.lower()


# In[25]:


data['online_order'] = data['online_order'].str.lower()
data['book_table'] = data['book_table'].str.lower()
data['location'] = data['location'].str.lower()
data['rest_type'] = data['rest_type'].str.lower()
data['dish_liked'] = data['dish_liked'].str.lower()
data['cuisines'] = data['cuisines'].str.lower()
data['listed_in(type)']=data['listed_in(type)'].str.lower()


# In[28]:


print(data.dtypes)


# In[34]:


data['approx_cost(for two people)'] = data['approx_cost(for two people)'].str.replace(',', '')
data['approx_cost(for two people)'] = data['approx_cost(for two people)'].astype(int)


# In[104]:


data['name'] = data['name'].str.split('-', n=1).str[0]


# In[95]:


# Calculate quartiles
Q1 = data['rate'].quantile(0.25)
Q3 = data['rate'].quantile(0.75)

# Calculate IQR (Interquartile Range)
IQR = Q3 - Q1

# Define lower and upper bounds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter the data to remove outliers
rate = data[(data['rate'] >= lower_bound) & (data['rate'] <= upper_bound)]

# Now df_filtered contains your data with outliers removed


# In[96]:


Q1 = data['votes'].quantile(0.25)
Q3 = data['votes'].quantile(0.25)

# Calculate IQR (Interquartile Range)
IQR = Q3 - Q1

# Define lower and upper bounds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter the data to remove outliers
votes = data[(data['votes'] >= lower_bound) & (data['votes'] <= upper_bound)]


# In[97]:


column_name = 'approx_cost(for two people)'
Q1 = data[column_name].quantile(0.25)
Q3 = data[column_name].quantile(0.75)

# Calculate IQR (Interquartile Range)
IQR = Q3 - Q1

# Define lower and upper bounds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter the data to remove outliers
column_name= data[(data[column_name] >= lower_bound) & (data[column_name] <= upper_bound)]


# In[88]:


correlation_matrix = data.corr()


# In[89]:


plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix Heatmap')
plt.show()


# In[90]:


# Group by 'name' and calculate the mean price for each hotel
avg_price_by_hotel = data.groupby('name')['approx_cost(for two people)'].mean().reset_index()

# Sort by average price in descending order
top_10_hotels = avg_price_by_hotel.sort_values(by='approx_cost(for two people)', ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.bar(top_10_hotels['name'], top_10_hotels['approx_cost(for two people)'], color='skyblue')
plt.title('Top 10 Hotels by Average Price')
plt.xlabel('Hotel Name')
plt.ylabel('Average Price for two')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[111]:


# Assuming you have a DataFrame named 'df' containing hotel names, number of votes, and locations

# Step 1: Sort the DataFrame by number of votes in descending order
sorted_data = data.sort_values(by='votes', ascending=False)

# Step 2: Select the top 10 hotels
top_10_hotels = sorted_data.head(10)

# Step 3: Find the location of each hotel
top_10_hotels_with_location = top_10_hotels[['cuisines', 'location']]

plt.figure(figsize=(10, 6))
plt.bar(top_10_hotels_with_location['location'], top_10_hotels_with_location['cuisines'], color='purple')
plt.title('Top 10 Hotels by Number of Votes')
plt.xlabel('Location')
plt.ylabel('Cuisines')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()




# In[92]:


sorted_hotels = data.sort_values(by='votes', ascending=False)

# Select the most visited hostel
most_visited_hotel = sorted_hotels.head(100)

# Plot the most visited hostel in a scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(most_visited_hotel['location'], most_visited_hotel['votes'], color='red')
plt.title('Most Visited Hotel')
plt.xlabel('Location')
plt.ylabel('Number of Votes')
plt.grid(True)
plt.show()


# In[93]:


top_locations = data['location'].value_counts().head(5).index

# Filter the dataframe for top 5 locations
df_top_locations = data[data['location'].isin(top_locations)]

# Group the data by location and order type, and count occurrences
grouped_data = df_top_locations.groupby(['location', 'online_order']).size().unstack(fill_value=0)

# Plotting the grouped bar chart
grouped_data.plot(kind='bar', stacked=False, figsize=(10, 6))
plt.title('Online Order by Location (Top 5)')
plt.xlabel('Location')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Order Type')
plt.tight_layout()
plt.show()


# In[94]:


delivery_counts = data['listed_in(type)'].value_counts()

# Plotting the pie chart
plt.figure(figsize=(8, 8))
plt.pie(delivery_counts, labels=delivery_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Sum of Hotels Based on Delivery Type')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()


# In[107]:


data.to_csv('zomato_project.csv', index=False)

