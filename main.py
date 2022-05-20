import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px
import pyodbc
import plotly.graph_objects as go


st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("Data Vizualization")



conn = pyodbc.connect(driver='{SQL Server Native Client 11.0}', host='show-case-project.database.windows.net', database='sql-db-show-case',
                     user='show-case-db', password='admin123*')
def init_connection():
   return pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + st.secrets["server"] + ";DATABASE=" + st.secrets["database"] + ";UID="       
       + st.secrets["username"]
       + ";PWD="
       + st.secrets["password"]
   )

conn = init_connection()
product_orders = pd.read_sql('select  top (20) prod.ProductName, prod.ModelName, sum(orderqty) as OrderQuantity  from [dbo].products prod left join orders on prod.ProductID=orders.CustomerID group by prod.ProductName, prod.ModelName order by OrderQuantity desc', conn)

#st.write(product_orders)

chunk_test = pd.read_sql('SELECT * from products', conn)
st.markdown("Data from AdventureWorks database")

prod_sold_by_date = pd.read_sql('select  OrderDate,prod.ProductNumber, prod.ModelName,prod.ProductName, sum(orderqty) as OrderQuantity  from [dbo].products prod inner join orders on prod.ProductID=orders.CustomerID group by prod.ModelName, prod.ProductName, prod.ProductNumber, OrderDate order by prod.ProductNumber,OrderDate', conn)


df  = pd.DataFrame(chunk_test)

chunk_test2 = pd.read_sql('SELECT * from orders_USD', conn)

#-----------


filter = st.selectbox('Please select the product number?', prod_sold_by_date['ProductNumber'].unique())
filtered_data = prod_sold_by_date[prod_sold_by_date['ProductNumber'] == filter]
st.write(filtered_data)
#st.write(prod_sold_by_date)

filtered_data_line=px.line(filtered_data,title='Number of orders by date', x="OrderDate", y="OrderQuantity", height=400, width= 800, labels={"Rate":"Date"},
color_discrete_sequence=px.colors.sequential.Turbo, )

st.plotly_chart(filtered_data_line)

st.subheader('Top 20 most ordered products')
st.write(product_orders)

hist_graph = px.bar(product_orders,title='', x="ProductName", y="OrderQuantity", barmode="group" , height=400, width= 800, color_discrete_sequence=px.colors.sequential.Turbo)
st.plotly_chart(hist_graph)

nb_orders = pd.read_sql('select OrderDate,sum(orderqty)orderqty,sum(subtotal) subtotal from orders group by OrderDate order  by OrderDate', conn)

df3=px.line(nb_orders,title='Number and volume of orders', x="OrderDate", y=["orderqty","subtotal"] , height=400, width= 800, labels={"Rate":"Date"},
color_discrete_sequence=px.colors.sequential.Turbo, )

df3.update_layout(legend=dict(yanchor="top", y=.74, xanchor="right", x=.99))
st.plotly_chart(df3)



