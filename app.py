import streamlit as st
import pandas as pd
import plotly_express as pt


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


st.subheader("Visualization options")

include_small = st.checkbox("Include models with less than 1000 ads", value=True)

# Contar cuántos anuncios tiene cada fabricante
model_count = car_data['model'].value_counts()


# Filtrar según el checkbox
if not include_small:
    valid_models = model_count[model_count >= 1000].index
    car_data = car_data[car_data['model'].isin(valid_models)]
    
st.subheader("Preview of filtered data")
st.dataframe(car_data)


st.header("Distribution of type of vehicles by model")
models = sorted(car_data['model'].dropna().unique())
selected_models = st.multiselect(
    'Select one or multiple models:',
    options=models,
    default=[]
)
if selected_models:
    data_filtrada = car_data[car_data['model'].isin(selected_models)]
else:
    data_filtrada = car_data
    

if st.button('Show histogram'):
    fig = pt.histogram(
        data_filtrada,
        x='model',     # eje X: modelos
        color='type',         # color: tipo de vehículo
        barmode='stack',      # barras apiladas
        title='Quantity of vehicles by model and type'
    )

    for trace in fig.data:
        trace.visible = 'legendonly'
        
    fig.update_layout(
        xaxis_title='Model',
        yaxis_title='Quantity',
        legend_title='Type of vehicle (select an option below)',
        width=900,
        height=500,
        title_font_size=22
    )

    st.plotly_chart(fig, use_container_width=True)


st.header("Relation between price and mileage")

# Botón para mostrar el gráfico
if st.button("Show scatter plot"):
    fig = pt.scatter(
        car_data,
        x='odometer',          # eje X: kilometraje
        y='price',             # eje Y: precio
        color='type',          # color por tipo de vehículo
        hover_data=['model', 'model_year'],  # info al pasar el mouse
        title='Relation between price and mileage by vehicle type'
    )

    for trace in fig.data:
        trace.visible = 'legendonly'
        
    fig.update_layout(
        xaxis_title='Mileage (odometer)',
        yaxis_title='Price (USD)',
        legend_title='Type of vehicle (select an option below)',
        width=900,
        height=500,
        title_font_size=22
    )

    st.plotly_chart(fig, use_container_width=True)