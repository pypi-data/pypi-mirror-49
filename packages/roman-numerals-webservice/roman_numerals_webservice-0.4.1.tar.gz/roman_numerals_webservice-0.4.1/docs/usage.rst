=====
Usage
=====

After installing the python package :code:`roman_numerals_webservice`
the webserver can be started with the following command

.. code-block:: shell

    roman_numerals_webservice

Alternatively we provide a prebuild docker container to start the web-service

.. code-block:: shell
    
    sudo docker run -p 8080:8080 derthorsten/roman_numerals_webservice:latest

Once the server is running requests can be send to the web-service.
On a Unix system this can be done with :code:`curl`

.. code-block:: shell

    $ curl -d '{"roman" : "XL"}' -H "Content-Type: application/json" -X POST http://localhost:8080/roman_to_arabic
    "{\"arabic\": 40}"

.. code-block:: shell

    $ curl -d '{"arabic" : 1987}' -H "Content-Type: application/json" -X POST http://localhost:8080/arabic_to_roman
    "{\"roman\": \"MCMLXXXVII\"}"


To roman_numerals_webservice can also be started from python

.. code-block:: python

    import cherrypy
    from roman_numerals_webservice import RomanNumeralsWebservice



    if __name__ == "__main__":
        config = {
            'server.socket_port': 8080,
            'server.socket_host': '0.0.0.0',
            'environment': 'production',
        }
  
        cherrypy.config.update(config)
        cherrypy.quickstart(RomanNumeralsWebservice()) 
