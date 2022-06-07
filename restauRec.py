import streamlit as st
import pandas as pd
import numpy as np
chefmozaccepts=pd.read_csv('chefmozaccepts.csv')
chefmozcuisine=pd.read_csv('chefmozcuisine.csv')
chefmozhours4=pd.read_csv('chefmozhours4.csv')
chefmozparking=pd.read_csv('chefmozparking.csv')
geoplaces2=pd.read_csv('geoplaces2.csv')
rating_final=pd.read_csv('rating_final.csv')
usercuisine=pd.read_csv('usercuisine.csv')
userpayment=pd.read_csv('userpayment.csv')
userprofile=pd.read_csv('userprofile.csv')
import pandas as pd
from functools import reduce

#define list of DataFrames
dfs = [chefmozaccepts, chefmozcuisine, chefmozhours4, chefmozparking,geoplaces2,rating_final]

#merge all DataFrames into one
final_df = reduce(lambda  left,right: pd.merge(left,right,on=['placeID'],
                                            how='inner'), dfs)


import base64

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return



st.set_page_config(page_title=None, page_icon='set_png_as_page_bg("img/PHOTO-Jess.png")', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("Restaurants Recommender")
from PIL import Image
image = Image.open('image_restaurant.jpg')

st.image(image)


geo_data = geoplaces2.filter(['latitude','longitude'])
st.map(data=geo_data, zoom=5, use_container_width=True)
    
st.write("""
### Best restaurants 
 
""")
final_df["city"] = final_df["city"].map(lambda x: x.lower())
final_df['city'].replace(['?'],final_df['city'].mode(), inplace=True)
final_df['url'].replace(['?'],'No Details', inplace=True)
final_df['address'].replace(['?'],'No Details', inplace=True)
final_df['days'].replace(['?'],'No Details', inplace=True)
final_df['hours'].replace(['?'],'No Details', inplace=True)
final_df['Rcuisine'].replace(['?'],final_df['Rcuisine'].mode(), inplace=True)
final_df['price'].replace(['?'],final_df['price'].mode(), inplace=True)
final_df['Rpayment'].replace(['?'],final_df['Rpayment'].mode(), inplace=True)
final_df['parking_lot'].replace(['?'],final_df['parking_lot'].mode(), inplace=True)
final_df['Restaurant_information'] ='Address: ' +final_df['address']+ ', City: ' + final_df['city']+', Cuisine: ' +final_df['Rcuisine']
final_df['Additional_information'] =' Price: ' + final_df['price']+ ', Payment Method: ' + final_df['Rpayment']+', Parking_lot :'+final_df['parking_lot']+', days_open : '+final_df['days']+' , Hours : '+final_df['hours']
new_final_df= final_df.drop_duplicates()
new_final_df1= new_final_df.drop_duplicates(subset=['Restaurant_information'])

def popularity_based_recommender(new_final_df1: pd.DataFrame, min_n_ratings: float):
    
    return (
        new_final_df1
        .groupby(['Additional_information', 'name',  'Restaurant_information'])
        .agg(
           
            rating_mean = ('rating', 'mean'),
            rating_count = ('rating', 'count')
        )
        .reset_index()
        .sort_values(['rating_count'], ascending=False)
        .query('rating_mean >= @min_n_ratings')
        .head(5)
        )
hide_table_row_index = """
       <style>
       tbody th {display:none}
       .blank {display:none}
       </style>
       """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
most_popular = popularity_based_recommender(new_final_df1.copy(),1.7)
mostPopular = most_popular.filter(['name','Restaurant_information','Additional_information'])
st.table(mostPopular)

