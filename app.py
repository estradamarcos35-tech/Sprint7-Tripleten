import streamlit as st
import pandas as pd
import plotly_express as pt

st.header('US vehicles car sale')
hist_button = st.button('Construir histograma')

car_data = pd.read_csv(r'C:\Users\marko\ProyectosPython\Sprint7-Tripleten\vehicles_us.csv')


#Revisamos cómo están nuestros datos.
car_data.info(10)
car_data.isnull().sum()


#Convertimos de tipo algunas de las columnas, ya que no tienen sentido que estuvieran en tipo float.
car_data = car_data.astype({
    'model_year': 'object',
    'cylinders': 'object',
    'odometer': 'object',
    'paint_color': 'object',
    'is_4wd': 'object',
})

#Hacemos conversión de la columna "date_posted" para acceder a ella como fecha, en caso de necesitar acceder a ella en un futuro.
car_data['date_posted'] = pd.to_datetime(car_data['date_posted'])

#Rellenamos valores ausentes con "unknown" ya que desconocemos muchos detalles que no queremos descartar sin conocerlos.
car_data = car_data.fillna({
    'model_year': 'unknown',
    'cylinders': 'unknown',
    'odometer': 'unknown',
    'paint_color': 'unknown',
    'is_4wd': 'unknown'
})

#Reemplazamos 1.0 por yes.
car_data['is_4wd'] = car_data['is_4wd'].replace(1.0, 'yes')

#Comprobamos los cambios
car_data.info()
print('Cantidad total de duplicados:', car_data.duplicated().sum())
print(car_data.sample(10))



if hist_button:
    st.write('Creación de un histograma para el conjunto de datos de anuncios de venta de coches')
    fig = pt.histogram(car_data, x="odometer")
    st.plotly_chart(fig, use_container_width=True)
    
scatter_button = st.button('Mostrar gráfico de dispersión')

if scatter_button:
    st.write('Relación entre el odómetro y el precio')
    fig2 = pt.scatter(car_data, x='odometer', y='price')
    st.plotly_chart(fig2, use_container_width=True)