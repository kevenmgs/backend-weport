# backend-weport

Instalación y Configuración

- Acceder a la ruta donde vamos a clonar el proyecto
- Clonar el proyecto ejecutar el comando: "git clone https://github.com/kevenmgs/backend-weport.git"
- Abrir una terminal de windows y acceder a la carpeta donde se clono el proyecto "Ejemplo: cd documents/backend-weport"
- Crear un entorno virtual, ejecutar el siguiente comando:
  "python -m venv venv"
. Activar el entorno virtual, ejecuta el comando:
  ".\venv\Scripts\activate"
- Instala sqlalchemy, ejecuta el comando: "pip install sqlalchemy"
- Instala pymysql, ejecuta el comando: "pip install pymysql"
- Instala pyjwt, ejecuta el comando: "pip install pyjwt"
- En el archivo database.py, buscar la linea: DATABASE_URL = "mysql+pymysql://root:""@localhost/weport"
- "Modificar @localhost/weport reemplazándolo por el servidor y el nombre de la base de datos utilizados. En este caso, el servidor es @localhost y el nombre de la base de datos es weport."
- Iniciar el servidor FastAPI , ejecuta el comando: uvicorn app.main:app --reload
