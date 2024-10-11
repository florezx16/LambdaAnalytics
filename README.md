# LambdaAnalytics technical assessment

Este proyecto consiste en dos aplicaciones para explorar multiples funcionalidades:
1. User management
2. Web scraping

# User management
Es una API con Django, DjangoRestFramework y DjangoRestFramework_simplejwt en la cual puedes crear usuarios de manera pública para luego probar la autenticación y la autorización usando JWT.

# Web scraping
una API desarrollada con Django y Django Rest Framework que realiza scraping en MercadoLibre para obtener información de productos, incluyendo nombre, precio, descuento, vendedor, calificación, URL de la imagen y URL del producto.

## Características

- Autenticación usando JWT
- Los tokens generados tienen una duración de 30m/1d respectivamente
- Las solicitudes son realizas con Fecth desde el front-end
- Web scraping de MercadoLibre usando BeautifulSoup
- Endpoint de búsqueda de productos (`/api/search/?query=`)
- Endpoint de análisis de precios, este Endpoint depende de que anteriormente ya hagas ejecutado el primero, ya que utilizara la información de este para realizar el análisis, como (precio más alto, más bajo, promedio) (`/api/get_etl/`)
- CUIDADO El Endpoint (`/get_etl`) depende del resultado de (`/search/?query=`). Asi que para obtener el resultado de la ETL debes PRIMERO ejecutar el query, de esta manera brindaras los datos suficientes para que la ETL se ejecute sin problemas ya que tendra los datos a disposición.
- Respuesta en formato JSON
- Pequeña interfaz para realizar las peticiones de manera más amigable

## Requisitos

- Python 3.8+
- Django 4.0+
- Django Rest Framework
- Django Rest simplejwt
- BeautifulSoup
- Requests

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/LambdaAnalytics.git
cd LambdaAnalytics
