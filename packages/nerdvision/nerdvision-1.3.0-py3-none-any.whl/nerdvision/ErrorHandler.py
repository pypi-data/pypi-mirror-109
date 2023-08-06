import hashlib
import logging
import os
import sys

from nerdvision.Utils import Utils
from nerdvision.models.NVError import NVError, NVErrorFrame

our_logger = logging.getLogger("nerdvision")


class ErrorHandler(object):
    roots = None

    def __init__(self, context_service):
        self.context_service = context_service

    @staticmethod
    def load_roots(main=sys.modules['__main__']):
        if ErrorHandler.roots is None:
            try:
                ErrorHandler.roots = set([
                                             # the path to the python executable
                                             os.path.abspath(
                                                 os.path.join(os.path.dirname(os.path.realpath(sys.executable)), '..')),
                                             # append python path (which can be not set) + then add the sys path as well
                                         ] + os.environ.get('PYTHONPATH', '').split(os.pathsep) + sys.path)
                # the path to the main module
                if hasattr(main, '__file__'):
                    ErrorHandler.roots.add(os.path.dirname(main.__file__))
                ErrorHandler.roots = set([s for s in ErrorHandler.roots if s.strip()])
            except:
                our_logger.exception("Cannot load roots set defaulting to none.")
                ErrorHandler.roots = {}
        return ErrorHandler.roots

    def capture_exception(self, exception_type_or_tuple=None, value=None, tb=None):
        """
        Captures an exception and extracts it into a NVError.
        If an exception is not provided, ask the system for the last error.

        :param exception_type_or_tuple: the exception to capture (as a tuple or value) or None
        :param value: the exception value
        :param tb: the traceback to process
        """

        if isinstance(exception_type_or_tuple, BaseException):
            exc_info = Utils.exc_info_from_exception(exception_type_or_tuple)
        elif isinstance(exception_type_or_tuple, tuple):
            exc_info = Utils.exc_info_from_exception(exception_type_or_tuple)
        elif isinstance(exception_type_or_tuple, type):
            exc_info = exception_type_or_tuple, value, tb
        else:
            exc_info = sys.exc_info()

        if exc_info[0] is None:
            our_logger.debug("No exception info found")
            return

        exc_type, exc_value, tb = exc_info

        nv_error = ErrorHandler.create_nv_error(exc_type, exc_value, tb)

        self.context_service.send_nv_error(nv_error)

    @staticmethod
    def trim_paths(path, roots):
        for root in roots:
            if path.startswith(root):
                return path[len(root):]
        return path

    @staticmethod
    def create_nv_error(exception_type, exception, tb, roots=None):
        """
        Create an NV Error from the exception details

        :param exception_type: the type of the exception
        :param exception: the actual exception value
        :param tb: the traceback for the exception
        :param roots: the system roots to trim from the file names
        :return: the NVError representation of the error
        """

        if roots is None:
            roots = ErrorHandler.load_roots()

        if tb is None:
            return None

        # python exception are made of 2 parts the traceback, which is the path from where we are to the
        # tracepoint and the stack, which is the path to here. So we need to combine them to get the real trace

        nv_error = NVError(exception_type.__name__, ', '.join(exception.args))
        frame = tb.tb_frame
        while frame is not None:
            line_no = frame.f_lineno
            source_file = frame.f_code.co_filename
            func_name = frame.f_code.co_name
            _self = frame.f_locals.get('self', None)
            class_name = None
            if _self is not None:
                class_name = _self.__class__.__name__

            nv_error.add_frame(NVErrorFrame(class_name, func_name, line_no, ErrorHandler.trim_paths(source_file, roots)))
            frame = frame.f_back

        frame = tb
        while frame is not None:
            line_no = frame.tb_lineno
            source_file = frame.tb_frame.f_code.co_filename
            func_name = frame.tb_frame.f_code.co_name
            _self = frame.tb_frame.f_locals.get('self', None)
            class_name = None
            if _self is not None:
                class_name = _self.__class__.__name__

            nv_error.push_frame(NVErrorFrame(class_name, func_name, line_no, ErrorHandler.trim_paths(source_file, roots)))
            frame = frame.tb_next

        nv_error.id = ErrorHandler.create_id(exception_type.__name__, nv_error.trace[0].source_file, nv_error.trace[0].line_no)
        return nv_error

    @staticmethod
    def create_id(type_name, source_file, line_no):
        return hashlib.md5((type_name + source_file + str(line_no)).encode('utf-8')).hexdigest()
