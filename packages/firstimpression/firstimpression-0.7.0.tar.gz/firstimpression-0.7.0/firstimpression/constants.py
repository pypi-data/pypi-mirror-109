from tempfile import gettempdir

PICTURE_FORMATS = {
    'fullscreen': "http://narrowcasting.fimpweb.nl/imageresize.php?width=1920&url=",
    'square':     "http://narrowcasting.fimpweb.nl/imageresize.php?width=512&url=",
}

TEMP_FOLDER = gettempdir()
LOCAL_INTEGRATED_FOLDER = 'C:/Users/Public/Documents/Scala/LocalIntegratedContent'

APIS = ['', 'BBC', 'NS', 'NU', 'TRAFFIC', 'INSTAGRAM', 'WEATHER']
