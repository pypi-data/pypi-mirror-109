__author__ = "sstober"

import logging
from logging import Handler, Formatter
import sys

# from pylearn2.utils.logger import CustomFormatter, CustomStreamHandler


class CustomFormatter(Formatter):
    """
    Conditionally displays log level names and source loggers, only if
    the log level is WARNING or greater.
    Parameters
    ----------
    prefix : WRITEME
    only_from : WRITEME
    """

    def __init__(self, prefix="", only_from=None):
        Formatter.__init__(self)
        self._info_fmt = prefix + "%(message)s"
        self._fmt = prefix + "%(levelname)s (%(name)s): %(message)s"
        self._only_from = only_from

    def format(self, record):
        """
        Format the specified record as text.
        Parameters
        ----------
        record : object
            A LogRecord object with the appropriate attributes.
        Returns
        -------
        s : str
            A string containing the formatted log message.
        Notes
        -----
        The record's attribute dictionary is used as the operand to a
        string formatting operation which yields the returned string.
        Before formatting the dictionary, a couple of preparatory
        steps are carried out. The message attribute of the record is
        computed using LogRecord.getMessage(). If the formatting
        string uses the time (as determined by a call to usesTime(),
        formatTime() is called to format the event time. If there is
        exception information, it is formatted using formatException()
        and appended to the message.
        """
        record.message = record.getMessage()
        # Python 2.6 don't have usesTime() fct.
        # So we skip that information for them.
        if hasattr(self, "usesTime") and self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        emit_special = self._only_from is None or record.name.startswith(
            self._only_from
        )
        if record.levelno == logging.INFO and emit_special:
            s = self._info_fmt % record.__dict__
        else:
            s = self._fmt % record.__dict__
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            try:
                s = s + record.exc_text
            except UnicodeError:
                # Sometimes filenames have non-ASCII chars, which can lead
                # to errors when s is Unicode and record.exc_text is str
                # See issue 8924
                s = s + record.exc_text.decode(sys.getfilesystemencoding())
        return s


class CustomStreamHandler(Handler):
    """
    A handler class which writes logging records, appropriately
    formatted, to one of two streams. DEBUG and INFO messages
    get written to the provided `stdout`, all other messages to
    `stderr`.
    If stream is not specified, sys.stderr is used.
    Parameters
    ----------
    stdout : file-like object, optional
        Stream to which DEBUG and INFO messages should be written.
        If `None`, `sys.stdout` will be used.
    stderr : file-like object, optional
        Stream to which WARNING, ERROR, CRITICAL messages will be
        written. If `None`, `sys.stderr` will be used.
    formatter : `logging.Formatter` object, optional
        Assigned to `self.formatter`, used to format outgoing log messages.
    Notes
    -----
    N.B. it is **not** recommended to pass `sys.stdout` or `sys.stderr` as
    constructor arguments explicitly, as certain things (like nosetests) can
    reassign these during code execution! Instead, simply pass `None`.
    """

    def __init__(self, stdout=None, stderr=None, formatter=None):
        Handler.__init__(self)
        self._stdout = stdout
        self._stderr = stderr
        self.formatter = formatter

    @property
    def stdout(self):
        """
        .. todo::
            WRITEME
        """
        return sys.stdout if self._stdout is None else self._stdout

    @property
    def stderr(self):
        """
        .. todo::
            WRITEME
        """
        return sys.stderr if self._stderr is None else self._stderr

    def flush(self):
        """Flushes the stream."""
        for stream in (self.stdout, self.stderr):
            stream.flush()

    def emit(self, record):
        """
        Emit a record.
        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        Parameters
        ----------
        record : WRITEME
        """
        try:
            msg = self.format(record)
            if record.levelno > logging.INFO:
                stream = self.stderr
            else:
                stream = self.stdout
            fs = "%s\n"
            # if no unicode support...
            # Python 2.6 don't have logging._unicode, so use the no unicode path
            # as stream.encoding also don't exist.
            if not getattr(logging, "_unicode", True):
                stream.write(fs % msg)
            else:
                try:
                    if isinstance(msg, str) and getattr(stream, "encoding", None):
                        try:
                            stream.write(fs % msg)
                        except UnicodeEncodeError:
                            # Printing to terminals sometimes fails. For
                            # example, with an encoding of 'cp1251', the above
                            # write will work if written to a stream opened or
                            # wrapped by the codecs module, but fail when
                            # writing to a terminal even when the codepage is
                            # set to cp1251.  An extra encoding step seems to
                            # be needed.
                            stream.write((fs % msg).encode(stream.encoding))
                    else:
                        stream.write(fs % msg)
                except (UnicodeError, TypeError):
                    stream.write((fs % msg).encode("UTF-8"))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def configure_custom(debug=False, stdout=None, stderr=None):
    """
    copied from pylearn2.utils.logger to obtain similar behavior for deepthought extensions

    Configure the logging module to output logging messages to the
    console via `stdout` and `stderr`.

    Parameters
    ----------
    debug : bool
        If `True`, display DEBUG messages on `stdout` along with
        INFO-level messages.
    stdout : file-like object, optional
        Stream to which DEBUG and INFO messages should be written.
        If `None`, `sys.stdout` will be used.
    stderr : file-like object, optional
        Stream to which WARNING, ERROR, CRITICAL messages will be
        written. If `None`, `sys.stderr` will be used.

    Notes
    -----
    This uses `CustomStreamHandler` defined in this module to
    set up a console logger. By default, messages are formatted
    as "LEVEL: message", where "LEVEL:" is omitted if the
    level is INFO.

    WARNING, ERROR and CRITICAL level messages are logged to
    `stderr` (or the provided substitute)

    N.B. it is **not** recommended to pass `sys.stdout` or
    `sys.stderr` as constructor arguments explicitly, as certain
    things (like nosetests) can reassign these during code
    execution! Instead, simply pass `None`.
    """
    top_level_logger = logging.getLogger(__name__.split(".")[0])

    # Do not propagate messages to the root logger.
    top_level_logger.propagate = False

    # Set the log level of our logger, either to DEBUG or INFO.
    top_level_logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # Get rid of any extant logging handlers that are installed.
    # This means we can call configure_custom() more than once
    # and have it be idempotent.
    while top_level_logger.handlers:
        top_level_logger.handlers.pop()

    # Install our custom-configured handler and formatter.
    fmt = CustomFormatter()
    handler = CustomStreamHandler(stdout=stdout, stderr=stderr, formatter=fmt)
    top_level_logger.addHandler(handler)
