# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

order_name = st.text_input('Order name')
st.write('Order name is: ', order_name)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    'Please select up to 5 fruit for your smoothie',
    my_dataframe,
    max_selections=5
)
time_to_submit = st.button('Submit Order')

if ingredients_list:
    ingredients_string = ''
    for fruit in ingredients_list:
        st.write('Selected fruit is ' + fruit)

        ingredients_string += fruit + ' '
        //search_on = pd_df.loc[pd_df['fruit_name']==fruit, 'search_on'].iloc[0]
        st.subheader(fruit + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit)
        fv_df=st.dataframe(fruityvice_response.json(),use_container_width=True)
    st.write('You have chosen: ' + ingredients_string)
    my_insert_stmt = """insert into smoothies.public.orders 
                             (name_on_order, ingredients)
                             values ('""" + order_name + """', '""" + ingredients_string + """')"""
    st.write(my_insert_stmt)

    if time_to_submit:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie has been ordered, ' + order_name + ' !!!', icon="✅")
