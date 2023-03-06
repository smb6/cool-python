"""
https://towardsdatascience.com/how-to-do-logging-in-python-37fee87b718c
"""

import logging
import typing as t
import sys

# import pandas as pd  # type: ignore
from datetime import datetime
from time import sleep

# from fraud_detection_model import __version__ as _version
# from fraud_detection_model.config.core import config
# from fraud_detection_model.processing.data_manager import load_pipeline
# from fraud_detection_model.processing.validation import validate_inputs

_logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('tmp.log')
sh = logging.StreamHandler(sys.stdout)
fh.setLevel(logging.NOTSET)
sh.setLevel(logging.NOTSET)
# ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
formatter = logging.Formatter('%(asctime)s - %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(sh)

elastic_host = "http://localhost:9200"
index = 'test-index'
content = 'test exception'

from cmreslogging.handlers import CMRESHandler
handler = CMRESHandler(hosts=[{'host': 'localhost', 'port': 9200}],
                           auth_type=CMRESHandler.AuthType.NO_AUTH,
                           es_index_name="my_python_index")
log = logging.getLogger("PythonTest")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

from elasticsearch_logging_handler import ElasticHandler

handler = ElasticHandler(elastic_host, index,
                         level=logging.DEBUG,
                         # timezone='Turkey',
                         flush_period=0.5)
logger.addHandler(handler)


# pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
# _fraud_detection_pipe = load_pipeline(file_name=pipeline_file_name)
#
#
# def make_prediction(*, inputs: t.Union[pd.DataFrame, dict]) -> dict:
#     """Make a prediction using a saved model pipeline."""
#
#     input_df = pd.DataFrame(inputs)
#
#     validated_data, errors = validate_inputs(inputs=input_df)
#     results = {"predictions": None, "version": _version, "errors": errors}
#
#     if not errors:
#         predictions = _fraud_detection_pipe.predict(
#             X=validated_data[config.model_config.all_features]
#         )
#         _logger.info(
#             f"Making predictions with model version: {_version} "
#             f"Predictions: {predictions}"
#         )
#         results = {
#             "predictions": predictions.tolist(),
#             "version": _version,
#             "errors": errors,
#         }
#
#     return results


def logging_example():
    sleep(5)
    logger.debug(f"This is a debug message at {datetime.utcnow()}")
    logger.info(f"This is a info message at {datetime.utcnow()}")
    logger.warning(f"This is a warning message at {datetime.utcnow()}")
    logger.error(f"This is a error message at {datetime.utcnow()}")
    logger.critical(f"This is a critical message at {datetime.utcnow()}")


if __name__ == '__main__':
    logging_example()
    pass
