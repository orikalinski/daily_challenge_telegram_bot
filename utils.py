import logging


def get_logger(name):
    logger = logging.getLogger(name)
    hdlr = logging.FileHandler('./daily_challenge.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger
