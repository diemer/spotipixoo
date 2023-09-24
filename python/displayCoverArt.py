import time
import sys
import logging
from logging.handlers import RotatingFileHandler
from getSongInfo import getSongInfo
import requests
from io import BytesIO
from PIL import Image
import sys,os
import configparser
from pixoo import Pixoo

if len(sys.argv) > 2:
    username = sys.argv[1]
    token_path = sys.argv[2]
    pixoo_ip_address = sys.argv[3]

    # Configuration file    
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../config/rgb_options.ini')

    # Configures logger for storing song data    
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='spotipy.log',level=logging.INFO)
    logger = logging.getLogger('spotipy_logger')

    # automatically deletes logs more than 2000 bytes
    handler = RotatingFileHandler('spotipy.log', maxBytes=2000,  backupCount=3)
    logger.addHandler(handler)

    # Configuration for the matrix
    config = configparser.ConfigParser()
    config.read(filename)

    default_image = os.path.join(dir, config['DEFAULT']['default_image'])
    print(default_image)
    pixoo = Pixoo(pixoo_ip_address)
    prevSong    = ""
    currentSong = ""

    try:
      while True:
        try:
          imageURL = getSongInfo(username, token_path)[1]
          currentSong = imageURL

          if ( prevSong != currentSong ):
            response = requests.get(imageURL)
            image = Image.open(BytesIO(response.content))
            image.thumbnail((matrix.width, matrix.height), Image.Resampling.LANCZOS)
            # save image
            image.save("current_track.png")

            # call pixoo push
            pixoo.draw_image("current_track.png")
            pixoo.push()
            # matrix.SetImage(image.convert('RGB'))
            prevSong = currentSong

          time.sleep(1)
        except Exception as e:
          image = Image.open(default_image)
          image.thumbnail((matrix.width, matrix.height), Image.Resampling.LANCZOS)
          image.save("default_image.png")
          pixoo.draw_image("default_image.png")
          pixoo.push()
          print(e)
          time.sleep(1)
    except KeyboardInterrupt:
      sys.exit(0)

else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()
