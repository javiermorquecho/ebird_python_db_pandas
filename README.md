# Análisis de aves.

## Directorios del proyecto

### Directorio principal

/CONABIO/ETL

En este directorio se adjuntan los proyectos, el que tenemos presente es el único: eBird. Creando nuevs directorios, se pueden crear más proyectos.

#### Directorio del proyecto de aves

/CONABIO/ETL/eBird

En este directorio se encuentran los archivos inciales para el funcionamiento de la plataforma. Estos archivo tienen la extensión .txt, que están formados en tipo CSV, separados por tabludar. Adicional, se visualizan los directorios de los 2 proyectos.

#### Directorio de prueba

/CONABIO/ETL/eBird/carga de datos

Este directorio sirvió como ejercicio para conocer las generalidades del proyecto. En él se hace pruebas de la carga y manipulación del archivo txt. De aquí podemos rescatar las generalidades del proyecto, ciertas funciolidades para generar escenarios, pero lo más importante, ayuda a entenderlo desde un inicio.

#### Directorio del proyecto

/CONABIO/ETL/eBird/carga datos v2

Este directorio ya contiene una versión estructurada de una solución basada en resolver el problema, desde el punto de vista de la BD, como primer alcance. La idea es dejar completo el proceso para ver la posibilidad de sustituir uno de esos procesos, pero desde el punto de vista de la manipulación de datos, con los pandas. Dicho proceso, contaría con la manipulación de datos y como resultado, un CSV que al final se cargaría en la ó las tablas de la base de datos.

El enfoque de la solución, es generar los pasos de manera más sencilla, a manera que se definan variables y con ello, ir procesando cada uno de los pasos del proceso.

Dentro de este directorio contamos con las siguientes clases: 
- **Db_operations**, que realiza todas las operaciones a BD.
- **Manager**, que centraliza las operaciones repetitivas de las demás clases.
- **TXT_data**, que tiene las operaciones con el CSV. Dentro de este archivo se incorporará la funcionalidad de los pandas.
- **base_stuff** y el directorio **lib**. Aún no tienen uso. La idea es que todas las clases estén en el directorio **lib** y que todo se inluya por medio del **base_stuff**.

## Archivo de pruebas
Los volúmenes de información son muy amplios, por lo que se generó un archivo de prueba para simular la carga de datos, aunque en las pruebas locales se han realizado también con archivos completos (hasta 9Gb).

# Documentación del entorno de desarrollo

A continuación se detalla la información para el levantamiento del entorno de desarrollo.

## Instalación del servidor

La documentación se refiere a la instalación de Uv y posteriormente a correr la plataforma. En relación a correr la plataforma de Jupyter Lab, se realiza de manera diferente, debido a que tenemos un servidor.

Lo normal es instalar el gestor de paquetes de Python, UV:

https://docs.astral.sh/uv/getting-started/installation/

Después hacer el clone del repo:

git clone https://github.com/javiermorquecho/ebird_python_db_pandas.git

Desde el directorio:

cd ebird_python_db_pandas/ 

Sincronizamos:

uv sync

Instalamos jupyter-lab para tener comandos de la consola:

uv tool install jupyterlab --with pip 

Corremos Jupyter Lab para que se visualice desde el servidor:

jupyter-lab --no-browser --ip=0.0.0.0

Del resultado de la ejecución obtenermos el token y con ese accedemos al proyecto. Usaríamos una URL como la siguiente:

http://172.16.1.248:8888/lab?token=7b002ffa75b15e448d4985d00194c7b4be57010fcdca5c94 

# Data Analysis with Pandas and Python

This repo contains the datasets and Jupyter Notebooks for the
**Data Analysis with Pandas and Python** course.

## Setup Instructions

1. Install the `uv` command-line program for managing Python projects.
   - Follow the instructions at https://docs.astral.sh/uv/getting-started/installation/.
2. Download or clone this repository locally.

If you have Git installed, execute `git clone git@github.com:paskhaver/data-analysis-with-pandas-and-python.git`

If you do not have Git installed, click the green `Code` button, then click `Download ZIP`.

If downloading directly from GitHub, you'll receive a compressed `.zip` file. You'll need to unzip it to access its contents.

- On macOS, double-click the `data-analysis-with-pandas-and-python` zip folder to unzip it.
- On Windows, right-click the zipped `data-analysis-with-pandas-and-python` folder, select `Extract All...`, and choose your destination folder.

3. Open your command-line application (i.e., Terminal, PowerShell) and navigate to the `data-analysis-wth-pandas-and-python` folder.
4. Execute `uv sync`. This command will:
   - Download Python (the base language)
   - Download Pandas (the data analysis library)
   - Download Jupyter Lab (the development environment)

The exact version of Python, Pandas, and all other libraries can be found in the `pyproject.toml` file.

## Two Folders

The `Incomplete` and `Complete` folders contain the exact same files.

The Jupyter Notebooks in the `Incomplete` folder have empty code cells. Watch along with the videos and practice writing the code inside the Notebook. You'll complete them as you progress through the course. Feel free to experiment!

The `Complete` folder contains my _completed_ Jupyter Notebooks from the recording of the
course. I recommend using these as a backup resource if a code sample does not work or if you want to compare our results.

## Startup and Shutdown

1. Execute `uv run jupyter-lab` to launch Jupyter Lab. Jupyter Lab should launch in your
   default web browser (i.e., Chrome). If it doesn't open, navigate to the link `localhost:8888`
   in your browser.
2. In Jupyter Lab, use the left-hand file explorer to navigate into the `incomplete` folder.
3. Open the Jupyter Notebook for your current course section.
4. Locate the section of the Notebook corresponding to the current lesson video. There is a Table of Contents icon on the left-hand side of Jupyter Lab if you'd like to navigate to any of the headings in the Notebook. The lessons appear in the same order as they do in the video course.
5. When you're done learning, save your work (`Cmd + S` on macOS, `Ctrl + S` on Windows, or press `File > Save All`).
6. Close the tabs corresponding to your open Jupyter Notebooks.
7. Click the Stop icon on the left-hand navigation bar (second button from the top).
8. In the **Kernels** section, click `Shut Down All`. Confirm your choice in the modal that appears.
9. Close the browser.
10. In your terminal, shut down your Jupyter Lab server with the shortcut `Ctrl + C`. Close your Terminal.
