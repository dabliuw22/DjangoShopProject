# Django Paypal Shop Project 

En este proyecto se desarrollara una tienda en línea, la cual permitira el pago mediante Paypal y el uso de tareas asincronas con *Celery*. Se utilizara el interprete de python3, por lo que debemos verificar si tenemos instalada la versión, ingresando en la terminal o consola de comandos. Se utilizara como gestor de bases de datos a *MySQL*. Además se brindara la implementación de un carro de compre mediante el uso de sessiones el cual se agregara al context_processors.

Los pasos a tener en cuenta son los siguientes:
 1. Crear una cuenta en [Registro PayPal](URL "https://www.paypal.com/us/webapps/mpp/account-selection").
 2. Crear un base de datos con el nombre de **shop_db**:
 ```[sql]
    create database shop_db;
 ```
 3. Instalar broker RabbitMQ:
 * Para Ubuntu:
 ```
    sudo apt-get install rabbitmq-server
 ```
 * Para Windows:
    [Descargar instalador](URL "https://www.rabbitmq.com/install-windows.html")
 4. Crear un entorno virtual y activarlo:
 ```
    python3 -m venv entorno
 ```
 5. Instalar las apps requeridas:
 ```
    pip3 install -r requirements.txt
 ```
 6. Clonar el proyecto o descargarlo:
 ```
    git clone https://github.com/dabliuw22/DjangoShopProject.git
 ```
 7. Crear un archivo en la carpeta del proyecto, con nombre y extensión *secret.json*, donde agregaremos las key's y credenciales del proyecto:
 ```[json]
    {
        "FILENAME": "secret.json",
        "SECRET_KEY": "9+0&mdex!j@vzy_*ey7%pxjbwjy#mc$yd10v3+x-mpp)*h5!&0",
        "PASSWORD": "db_user_password",
        "CARRITO_SESSION_ID": "cart",
        "PAYPAL_RECEIVER_EMAIL": "your_email_receiver_paypal",
        "EMAIL_HOST_USER": "your_email_admin",
        "EMAIL_HOST_PASSWORD": "your_email_admin_password"
    }
 ```
 8. Correr la app en el servidor local:
 ```
    python3 manage.py runserver
 ```
 9. Correr el broker RabbitMQ en el entorno virtual:
 ```
    celery -A ShopProject worker -l info
 ```
 10. Probar sin funcionan los pagos mediante PayPal IPN Simulator, lo cual no se puede hacer con el localhost,
 por lo que instalaremos [ngrok](URL "https://ngrok.com/") y luego lo iniciaremor desde la terminal con el 
 siguiente comando:  
 ```
 ngrok http 8000
 ```
 Donde se desplegaran unas url's dinamicas virtuales para el proyecto actual que se encuentra corriendo, ejemplo:
 ```
    Session Status                online                                            
    Version                       2.2.8                                             
    Region                        United States (us)                                
    Web Interface                 http://127.0.0.1:4040                             
    Forwarding                    http://ffb56f6f.ngrok.io -> localhost:8000        
    Forwarding                    https://ffb56f6f.ngrok.io -> localhost:8000 
 ```
 **Nota:** Cada vez que lo inicien se generara una url nueva, recuerden que es dinamica, por tanto debemos configurar
 ALLOWED_HOSTS de nuestro *settings.py* según el host que generemos: 
 ```ALLOWED_HOSTS = ['ffb56f6f.ngrok.io']```
 Ahora debemos logearnos en PayPayl y dirigirnos a la [IPN Simulator](URL "https://developer.paypal.com/developer/ipnSimulator/")
 y en el campo IPN handler URL agregamos `http://ffb56f6f.ngrok.io/payment/done` y seleccionamos la Transaction Type `eCheck - complete`, 
 luego enviamos el formulario y nos dará la respuesta de la verificación.