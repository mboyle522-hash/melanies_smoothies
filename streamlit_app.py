# Import python packages
import streamlit as st
import requests

from snowflake.snowpark.functions import col
# Write directly to the app
st.title(f"My Parents New Health Diner")
st.write(
  """Choose what fruits you want in your custom Smoothie
  """
)
name_on_order=st.text_input('Name On Smoothie:')
st.write('The Name on your smoothie will be:', name_on_order)

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
     
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select('FRUIT_NAME')
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredents_list= st.multiselect(
    'Choose up to 5 ingredents:'
    ,my_dataframe
  )
if ingredents_list:
    ingredients_string = ''

    for fruit_chosen in ingredents_list:
        ingredients_string +=fruit_chosen + ' '
    #st.write(ingredients_string)
    
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop
    time_to_insert= st.button('Submit Order')
    if time_to_insert:
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered!', icon="✅")

