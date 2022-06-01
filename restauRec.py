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


st.write("""
### Select City of Choice : 
 
""")
#City based Recommendation
city = st.selectbox(
    ' ',
     (matrix1['city'].unique()))


def city_based_recommender(matrix1: pd.DataFrame, city: str):
    
    return (
        matrix1
        .groupby(['city', 'name'])
        .agg(
           
            rating_mean = ('rating', 'mean'),
            rating_count = ('rating', 'count')
        )
        .reset_index()
        .sort_values(['rating_count'], ascending=False)
        .query('city == @city & rating_mean >= 0')
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
most_popular1 = city_based_recommender(matrix1.copy(),city)
mostPopular1 = most_popular1.filter(['name','city','Rcuisine'])
st.table(mostPopular1)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Rating Based : ")
    #select Rating for city
    rating = st.selectbox(
        ' ',
         (matrix1['rating'].unique()))
    def cityRating_based_recommender(matrix1: pd.DataFrame, city: str, rating: int):
    
        return (
            matrix1
        
            .query('city == @city')
            .query('rating == @rating')
            .groupby(['city', 'name','rating'])
            .agg(
           
                rating_mean = ('rating', 'mean'),
                rating_count = ('rating', 'count')
            )
            .sort_values(['rating_count'], ascending=False)
            .reset_index()
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
    most_popular1 = cityRating_based_recommender(matrix1.copy(),city,rating)
    mostPopular1 = most_popular1.filter(['name','city','Rcuisine','rating'])
    st.table(mostPopular1)

with col2:
    st.subheader("Price Range Based :")
    #City and Price based recommendation
    price = st.selectbox(
        ' ',
         (matrix1['price'].unique()))
    def cityPrice_based_recommender(matrix1: pd.DataFrame, city: str, price: str):
    
        return (
            matrix1
            .query('city == @city')
            .query('price == @price')
            .groupby(['city', 'name','price'])
            .agg(
           
                rating = ('rating', 'count')
            )
            .sort_values(['rating'], ascending=False)
            .reset_index()
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
    most_popular1 = cityPrice_based_recommender(matrix1.copy(),city,price)
    mostPopular1 = most_popular1.filter(['name','city','price'])
    st.table(mostPopular1)

with col3:
    st.subheader("Cuisine based :")
#City and Cuisine based recommender
    Rcuisine = st.selectbox(
        ' ',
         (matrix1['Rcuisine'].unique()))

    def cityCuisine_based_recommender(matrix1: pd.DataFrame, city: str, Rcuisine: str):
    
        return (
            matrix1
            .query('city == @city')
            .query('Rcuisine == @Rcuisine')
            .groupby(['city', 'name','Rcuisine'])
            .agg(
           
                rating = ('rating', 'count')
            )
            .sort_values(['rating'], ascending=False)
            .reset_index()
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
    most_popular1 = cityCuisine_based_recommender(matrix1.copy(),city,Rcuisine)
    mostPopular1 = most_popular1.filter(['name','city','price'])
    st.table(mostPopular1)
