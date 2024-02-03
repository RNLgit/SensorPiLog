import argparse
import os
import time
from pilogger.db_connector import SQLLogger
from pilogger.sensor import PiSensor
import logging


def setup_logging(log_level="DEBUG"):
    logger = logging.getLogger("pilogger_scheduler")
    logger.setLevel(log_level)
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler("pilogger_scheduler.log")
    c_handler.setLevel(log_level)
    f_handler.setLevel(logging.DEBUG)
    c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    return logger


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scheduler for SensorPiLog that logs data from sensors and sense hat")
    parser.add_argument("database_ip", type=str, help="database ip address")
    parser.add_argument(
        "-s", "--seconds", type=int, default=60, help="interval in seconds to log data, default is 60 seconds"
    )
    parser.add_argument("-l", "--log_level", type=str, default="DEBUG", help="log level, default is DEBUG")
    args = parser.parse_args()
    log_level = getattr(logging, args.log_level.upper())
    logger = setup_logging(log_level)

    if not all(
        os.environ.get(key)
        for key in ["PI_SERVER_DB_USER", "PI_SERVER_DB_PASSWORD", "PI_SERVER_DATABASE", "PI_SERVER_TABLE_NAME"]
    ):
        raise ValueError(
            "Environment variables not set. Please set PI_SERVER_DB_USER, PI_SERVER_DB_PASSWORD, "
            "PI_SERVER_DATABASE and PI_SERVER_TABLE_NAME for scheduler service"
        )
    while True:
        with SQLLogger(host=args.database_ip) as db:
            logger.DEBUG("start reading data and log to database")
            sensor = PiSensor()
            db.write_pi_data(sensor.read_all)
            logger.DEBUG(f"data logged to database, wait for {args.seconds} seconds before next logging.")
        time.sleep(args.seconds)
