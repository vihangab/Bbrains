# run.py

# Author  : Vihanga Bare #

import socket
import os
import threading
import sys
import select
from signal import SIGINT

port = 8888


import os

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(debug=True)
    
