import logging
import time
import datetime


class Logger(object):
    logging.basicConfig(
        format='%(message)s',
        level=logging.INFO
    )

    def log(self, *args):
        logging.info(args[0])
        return args


class PerformanceLoggerDateTime(Logger):
    @classmethod
    def reset_timer(cls):
        cls.__start_time = datetime.datetime.now()

    def log(self, func_name, msg):
        message = f"{func_name} : {(datetime.datetime.now() - self.__start_time)} {msg}"
        super().log(message)


class PerformanceLoggerNanoSec(Logger):
    @classmethod
    def reset_timer(cls):
        cls.__start_time = time.perf_counter_ns()

    def log(self, func_name, msg):
        message = f"{func_name} : {(time.perf_counter_ns() - self.__start_time)} {msg}"
        super().log(message)

