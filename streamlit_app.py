# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie")
st.write(
    """
    Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your smoothie will be:', name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect(
    'Choose upto 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)

    ingredient_string = ''

    for fruit_chosen in ingredient_list:
        ingredient_string += fruit_chosen

    #st.write(ingredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS,Name_on_order)
            values ('""" + ingredient_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')

    st.write(my_insert_stmt)

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered:' +name_on_order, icon="✅")

    


