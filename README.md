# Practica 4 - Practica 8 - DAI

[![Heroku Deploy](https://www.herokucdn.com/deploy/button.svg)](https://practica8.herokuapp.com/)

###Integración continua:

Para la integración continua se ha usado Travis-CI para realizar los tests. Para llevarlo a cabo se ha necesitado crear un fichero [.travis.yml](https://github.com/rubenjo7/Practica4-DAI/blob/master/.travis.yml).

El makefile que he creado para hacer las instalaciones automáticamente y los test es:

    install:
    	pip install -r requirements.txt

    test:
    	python test.py

    ejecutar:
    	python p4.py

Tras esto, Travis comienza a instalar los paquetes necesarios y a ejecutar el test.

Test en ordenador personal:

<img src="http://i67.tinypic.com/2aihiro.png" border="0" alt="Image and video hosting by TinyPic">

Test TRAVIS-CI:

Si nos vamos a [TRAVIS-CI]() vemos que esta todo correcto porque esta de color verde.

###Despliegue en Heroku:

Para este despliegue, me he tenido que dar de alta en la web, vincular mi cuenta de github a esta nueva y a partir de ahí crear una aplicación.

Ahora nos vamos a Heroku y seleccionamos la casilla de despliegue automático, para que una vez se haga push en git, este actualice automáticamente. Además, seleccionamos la opción de esperar a que los test de integración continua estén pasados, lo cual es bastante conveniente tenerlo activo:

<img src="http://i68.tinypic.com/iegkme.png" border="0" alt="Image and video hosting by TinyPic">

Otra manera de hacerlo es de forma manual, porque a veces tarde más de lo esperado:

<img src="http://i66.tinypic.com/95pyk9.png" border="0" alt="Image and video hosting by TinyPic">

Para el despliegue necesitamos un fichero Procfile, cuyo contenido esta en el siguiente [enlace](https://github.com/rubenjo7/Practica4-DAI/blob/master/Procfile).

Este fichero es el que Heroku ejecuta, por tanto, debemos decirle que ejecute la web.

A parte, he creado un archivo llamado [runtime.txt](https://github.com/rubenjo7/Practica4-DAI/blob/master/runtime.txt) que contiene la versión de Python que estamos usando.

Una vez que se evaluen los test unitarios de nuestra aplicación en TravisCI en mi caso veremos como nuestra aplicación se despliega en Heroku:

<img src="http://i66.tinypic.com/e9t91y.png" border="0" alt="Image and video hosting by TinyPic">


En este momento nuestra web esta desplegado. Podemos ver los logs en la siguiente imagen:

<img src="http://i67.tinypic.com/raan36.png" border="0" alt="Image and video hosting by TinyPic">

Con esto ya tendremos configurado nuestro despliegue atomático y podremos probarlo desde cualquier plataforma.

<img src="http://i66.tinypic.com/1e9i00.png" border="0" alt="Image and video hosting by TinyPic">
