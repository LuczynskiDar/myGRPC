
# Configure Flask logging
app.logger.setLevel(logging.INFO)  # Set log level to INFO
path = os.path.join(app.root_path)
root_path = Path(path)
# C:\Workspace\LLM\C04D04\api\cashman\static
handler = logging.FileHandler('app.log',encoding='utf-8')  # Log to a file
# handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s.py %(remote_addr)s requested %(url)s : %(message)s'))
handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s.py : %(message)s'))
app.logger.addHandler(handler)


import logging
import logging.config
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

logger.debug('This is a debug message')



import logging
import logging.config

logging.config.fileConfig(fname='config.ini', disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger(__name__)

logger.debug('This is a debug message')

