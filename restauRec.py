import streamlit as st
import pandas as pd
chefmozaccepts=pd.read_csv('chefmozaccepts.csv')
chefmozcuisine=pd.read_csv('chefmozcuisine.csv')
chefmozhours4=pd.read_csv('chefmozhours4.csv')
chefmozparking=pd.read_csv('chefmozparking.csv')
geoplaces2=pd.read_csv('geoplaces2.csv')
rating_final=pd.read_csv('rating_final.csv')
usercuisine=pd.read_csv('usercuisine.csv')
userpayment=pd.read_csv('userpayment.csv')
userprofile=pd.read_csv('userprofile.csv')


st.write("""
### Best restaurants 
 
""")
matrix = pd.merge(rating_final,geoplaces2, how ="inner", on = ["placeID"])
matrix1 = pd.merge(matrix,chefmozcuisine, how ="inner", on = ["placeID"])
# modify values : Make the data in all cities to lowecase
matrix1["city"] = matrix1["city"].map(lambda x: x.lower())
# Popularity based recommender
def popularity_based_recommender(matrix1: pd.DataFrame, min_n_ratings: float):
    
    return (
        matrix1
        .groupby(['city', 'name',  'Rcuisine'])
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
most_popular = popularity_based_recommender(matrix1.copy(),1.7)
mostPopular = most_popular.filter(['name','city','Rcuisine'])
st.table(mostPopular)
