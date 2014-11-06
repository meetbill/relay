import logging
from colorlog import ColoredFormatter
from relay import log


def configure_logging(add_handler):
    """
    Configure log records.  If adding a handler, make the formatter print all
    passed in key:value data.
        ie log.extra('msg', extra=dict(a=1))
        generates  'msg  a=1'

    `add_handler` (True, False, None, or Handler instance)
        if True, add a logging.StreamHandler() instance
        if False, do not add any handlers.
        if given a handler instance, add that the the logger
    """
    _ignore_log_keys = set(logging.makeLogRecord({}).__dict__)

    def _json_format(record):
        extras = ' '.join(
            "%s=%s" % (k, record.__dict__[k])
            for k in set(record.__dict__).difference(_ignore_log_keys))
        if extras:
            record.msg = "%s    %s" % (record.msg, extras)
        return record

    class ColoredJsonFormatter(ColoredFormatter):
        def format(self, record):
            record = _json_format(record)
            return super(ColoredJsonFormatter, self).format(record)
    if not log.handlers:
        if add_handler is True:
            _h = logging.StreamHandler()
            _h.setFormatter(ColoredJsonFormatter(
                "%(log_color)s%(levelname)-8s %(message)s %(reset)s %(cyan)s",
                reset=True
            ))
            log.addHandler(_h)
        elif isinstance(add_handler, logging.Handler):
            log.addHandler(add_handler)
        else:
            log.addHandler(logging.NullHandler())
    log.setLevel(logging.DEBUG)
    log.propagate = False
    return log