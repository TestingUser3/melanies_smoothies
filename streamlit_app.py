# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(f" :cup_with_straw: Customize your Smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom smoothie.
  """
)

name_on_order = st.text_input('Name on your Smoothie : ')
# st.write(name_on_order)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data = my_dataframe, use_container_width=True)

ingredients_list = st.multiselect("Choose upto 5 ingredients", my_dataframe,max_selections=5)

if ingredients_list:
    # st.write(ingredients_list)
    ingredients_string = ''
    for i in ingredients_list:
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        ingredients_string+=i + ' '

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    # st.write(my_insert_stmt)
    submit_button = st.button('Submit Order')

    if submit_button:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order+ '!', icon="✅")



