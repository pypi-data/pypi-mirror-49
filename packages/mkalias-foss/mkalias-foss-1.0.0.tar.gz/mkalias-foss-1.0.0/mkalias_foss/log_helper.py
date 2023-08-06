import logging


class LogHelper:

    @staticmethod
    def init_logging(debug: bool, name):
        """
        Logging initializer
        :param debug: True/False used to set DEBUG default INFO
        :param name: Class/module name to pass to logger usually __name__
        :return: Logger object from logging
        """
        # Setup logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # setup Logging Handlers
        log_console_handler = logging.StreamHandler()
        if debug:
            log_console_handler.setLevel(logging.DEBUG)  # Verbose/Debug output
        else:
            log_console_handler.setLevel(logging.INFO)  # Normal Output

        # setup Logging Formatters
        log_console_format = logging.Formatter('%(name)s - %(levelname)s: \n %(message)s')
        log_console_handler.setFormatter(log_console_format)
        # add handler to the logger
        logger.addHandler(log_console_handler)

        return logger

    @staticmethod
    def shutdown():
        logging.shutdown()
