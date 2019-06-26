import logging

import rasa
from rasa.nlu.train import train
from rasa.nlu.training_data import load_data

logging.getLogger(__name__).addHandler(logging.NullHandler())

__version__ = rasa.__version__
