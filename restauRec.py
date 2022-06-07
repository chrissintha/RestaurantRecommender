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
    

