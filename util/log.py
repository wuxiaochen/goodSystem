import os,time
from logging.handlers import RotatingFileHandler
import logging
import multiprocessing


if os.name == 'nt':
    import win32con, win32file, pywintypes
    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
    LOCK_SH = 0 # The default value
    LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
    __overlapped = pywintypes.OVERLAPPED(  )
 
    def lock(file, flags):
        hfile = win32file._get_osfhandle(file.fileno(  ))
        win32file.LockFileEx(hfile, flags, 0, 0xffff0000, __overlapped)
 
    def unlock(file):
        hfile = win32file._get_osfhandle(file.fileno(  ))
        win32file.UnlockFileEx(hfile, 0, 0xffff0000, __overlapped)
elif os.name == 'posix':
    from fcntl import LOCK_EX, LOCK_SH, LOCK_NB
 
    def lock(file, flags):
        fcntl.flock(file.fileno(  ), flags)
 
    def unlock(file):
        fcntl.flock(file.fileno(  ), fcntl.LOCK_UN)
else:
    raise RuntimeError("File Locker only support NT and Posix platforms!")

_log_f_handler = logging.handlers.RotatingFileHandler(u"assistant.trace", mode="aw",maxBytes=20971520,backupCount=1)
_loghandler = logging.getLogger("fruitSystem")
_loghandler.setLevel(logging.DEBUG)
_log_f_handler.setFormatter(logging.Formatter(u'[%(asctime)s][%(levelname)s][Process:%(process)d][Thread%(thread)d][Filename:%(filename)s][FunctionName:%(funcName)s]---------------[%(message)s]'))
_loghandler.addHandler(_log_f_handler)


def trace(tracetype, msg):
    f = open("logLock.dat", "w")
    lock(f, LOCK_EX)
    if tracetype.upper() == "DEBUG":
        _loghandler.debug(msg)
    elif tracetype.upper() == "INFO":
        _loghandler.info(msg)
    elif tracetype.upper() == "WARNING":
        _loghandler.info(msg)
    elif tracetype.upper() == "ERROR":
        _loghandler.error(msg)
    else:
        _loghandler.info(msg)
    unlock(f)
    f.close()

if __name__ == "__main__":
    trace("info", "testlog")
