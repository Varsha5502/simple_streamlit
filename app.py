import os
import json

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from utils.b2 import B2


# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
REMOTE_DATA = 'seattle_home_prices.csv'


# ------------------------------------------------------
#                        CONFIG
# ------------------------------------------------------
load_dotenv()

# load Backblaze connection
b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
        key_id=os.environ['B2_KEYID'],
        secret_key=os.environ['B2_APPKEY'])


# ------------------------------------------------------
#                         APP
# ------------------------------------------------------
st.write(
'''
## Seattle Home Prices
We can import data into our streamlit app using pandas read_csv then display the resulting dataframe with st.dataframe()
''')

b2.set_bucket(os.environ['B2_BUCKETNAME'])

df_prices = b2.to_df(REMOTE_DATA)
st.dataframe(df_prices)

# ------------------------------
# PART 1 : Train Model
# ------------------------------

features = ['SQUARE FEET', 'BEDS', 'LATITUDE', 'LONGITUDE']
target = 'PRICE'

df_prices = df_prices[features + [target]]
df_prices.dropna(inplace=True)


# ------------------------------
# PART 1 : Plot
# ------------------------------

st.write(
'''
### Graphing and Buttons
Lets graph some of our data with matplotlib. We can also add buttons to add interactivity to our app.
'''
)

fig, ax = plt.subplots()

ax.hist(df_prices['PRICE'])
ax.set_title('Distribution of House Prices in $100,000s')

show_graph = st.checkbox('Show Graph', value=True)

if show_graph:
    st.pyplot(fig)

# PART 5
    
st.write(
'''
### Mapping and Filtering Our Data
We can also use Streamlit's built in mapping functionality.
We can use a slider to filter for houses within a particular price range as well.
'''
)

price_input = st.slider('House Price Filter', 
                        int(df_prices['PRICE'].min()), 
                        int(df_prices['PRICE'].max()), 
                        100000)

price_filter = df_prices['PRICE'] < price_input
st.map(df_prices.loc[price_filter, ['LATITUDE', 'LONGITUDE']])

# PART 6

st.write(
'''
## Train a linear Regression Model
Create a model to predict house price from sqft and number of beds
'''
)

# There is a better way to do this ...
from sklearn.linear_model import LinearRegression

features = ['SQUARE FEET', 'BEDS']
target = 'PRICE'

df = df_prices[features + [target]]
df.dropna(inplace=True)

X = df[features]
y = df[target]

lm = LinearRegression()

lm.fit(X, y)


# PART 7

st.write(
'''
## Make predictions with the trained model from user input
'''
)

sqrft = st.number_input('Square Footage of House', value=2000)
beds = st.number_input('Number of Bedrooms', value=3)

input_data = pd.DataFrame({'SQUARE FEET': [sqrft], 'BEDS': [beds]})
pred = lm.predict(input_data)[0]
st.write(
f'Predicted Sale Price of House: ${int(pred):,}'
)