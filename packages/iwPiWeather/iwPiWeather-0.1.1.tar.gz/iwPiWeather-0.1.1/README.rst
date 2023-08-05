Installation:
-------------

You can either get the source code and include it in your application
manlually, or use can use pip instead.

``pip install iwPiWeather``

Or depending on your raspberry config for python3 you might need to run

``pip3 install iwPiWeather``

Use example:
------------

Include your package, define the pins and initialize the thread

::

    import iwPiWeather

    displayPinout = { "rs": 22, "en": 17, "d7": 18, "d6": 23, "d5": 24, "d4": 25 }
    weather = iwPiWeather.weatherDisplay(apiKey='passyouroowmapikey', poolRate=120, dispPins=displayPinout, autoStart=True)

You can pass the following arguments in the constructor:

-  *apiKey* - Required field, you need to provide the OpenWeatherMap API
   key.

-  *poolRate* - Time to wait between each call to the OpenWeatherMap
   API.

-  *dispPins* - Layout of the display pins connection

-  *autoStart* - If this is toggled off, the thread will start in sleep
   mode, and no calls will be made until the thread is manually started.

The created weather object will be actually a thread that runs in the
background. So you can integrate this functionality in your application,
this will run as a background process in a separate thread.

You can temporarily pause the display update thread by calling
``weather.stopWatch()`` which will allow you for example to stop pooling
and displaying the weather data on the display and use the display for
something else in your integration.

To restart the thread and keep reprinting the weather data you can use
``weather.startWatch()``

To stop the thread and cleanup the object you can call
``weather.stopThread()``. This will kill the thread and you can safely
stop the application.
