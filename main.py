import os
import shutil

from stem.control import Controller
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
  return "Hello world"

if (__name__ == "__main__"):
    print(' * Connecting to tor')

    # Use ControlPort
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()

        # Create a hidden service where visitors of port 80 get redirected to local port 8080
        hidden_service_dir = "C:/tmp"
        print(" * Creating our hidden service in " + hidden_service_dir)
        result = controller.create_hidden_service(hidden_service_dir, 80, "127.0.0.1", target_port = 8080)

        #The hostname is only available when we can read the hidden service directory. This requires us to be running with the same user as tor.
        with open("C:/tmp/hostname", "r") as h:
            print(" * Running on " + h.read())
          
        try:
            app.run(port=8080)
      
        # Shut down the hidden service and clean it off disk. 
        # If you want to use same hostname in next deployment, just delete this part
        finally:
            print(" * Shutting down our hidden service")
            controller.remove_hidden_service(hidden_service_dir)
            shutil.rmtree(hidden_service_dir)
