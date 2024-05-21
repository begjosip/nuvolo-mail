from flask import Flask
from dotenv import load_dotenv
import threading

from rabbitmq.rabbitmq_listener import *

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

if __name__ == '__main__':
    rabbit_listener = RabbitMQListener()
    listener_thread = threading.Thread(target=rabbit_listener.start_listening)
    listener_thread.start()
    app.run(port=os.getenv("PORT"), debug=True, use_reloader=False)
