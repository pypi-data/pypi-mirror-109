from performance_logger.logger import PerformanceLoggerDateTime, PerformanceLoggerNanoSec


def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


@parametrized
def perf_logger(func, time_format):
    def decorated_func(*args, **kwargs):
        if time_format == "datetime":
            log = PerformanceLoggerDateTime()
            log.reset_timer()
            fun = func(*args, **kwargs)
            name = func.__name__
            log.log(f"Run Func \'{name}\'", "time logged")
            return fun
        elif time_format == "ns":
            log = PerformanceLoggerNanoSec()
            log.reset_timer()
            fun = func(*args, **kwargs)
            name = func.__name__
            log.log(f"Run Func \'{name}\'", "time logged")
            return fun
    return decorated_func
