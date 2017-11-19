'''
Module - logger.py

Description - Module for logging information to the console or txt file

Items -

    Class Logger:
        -Logger Description-
            This class is used for writing text to either the console or txt file.
            You do not instantiate any Logger objects for use but rather call each function
            statically.

        -Logger  static variables-
            TYPE : NAME - DESC
            string : directory - directory the log files will be written to
            string : fileName - The name of the log file
            file object : f - File object for the logger to write to

        -Logger functions-
            RETURNTYPE : NAME - DESC
            void : console_i - prints information to the console
            void : console_e - prints error information to the console
            void : console_d - prints debug information to the console
            void : log_info - writes information to a txt file
            void : log_error - writes error information to a txt file
            void : log_debug - writes debug information to a txt file
            void : close_log - Closes the file object

'''

from inspect import getframeinfo, stack
from time import strftime
from os.path import join

class Logger(object):
    '''

       Logger, a static based class that provides functions to log information
       to the console or to a file

       If the console is only being called explicitly, the only
       argument that needs to be passed is a string containing the
       information you're trying to print or output to a file

       arg[0] = message - output to the console
       arg[1] = file name - what file the logger instance was called from
       arg[2] = line number - what linea logger instance was called from

    '''
    DEBUGMODE = True
    directory = "logs/"
    file_name = "{}.txt".format(strftime("%m-%d-%Y"))
    file_object = open(join(directory, file_name), "a+")

    @staticmethod
    def load_file_object(directory=None, file_name=None):
        """
        Reload the file object used for appending data to

        Params:
            (str) directory = directory path 
            (str) file_name = file_name 
        """
        if directory is None and file_name is None:
            Logger.file_object = open(join(Logger.directory, Logger.file_name), 'a+')
        elif directory is not None and file_name is None:
            Logger.file_object = open(join(directory, Logger.file_name), 'a+')
        elif directory is None and file_name is not None:
            Logger.file_object = open(join(Logger.directory, file_name), 'a+')
        else:
            Logger.file_object = open(join(directory, file_name), 'a+')

    @staticmethod
    def console_i(message=None,*args):
        """
        Output information to the console

        user must always supply the message string when explicitly calling console_i.
        args is meant for other functions to pass the frame info to the console from
        their call when DEBUGMODE is True

        Params:
            message = Information to be printed to the console
            *args = frame info Information passed from other Logger functions

        """
        if message is not None:
            caller = getframeinfo(stack()[1][0])
            print("[INFO][{}][{}]:{}".format(caller.filename, caller.lineno, message))
        else:
            print("[INFO][{}][{}]:{}".format(args[2], args[1], args[0]))

    @staticmethod
    def console_e(message=None, *args):
        """
        Output errors to the console

        user must always supply the info string when explicitly calling console_i.
        args is meant for other functions to pass the frame info to the console from
        their call when DEBUGMODE is True

        Params:
            message = Information to be printed to the console
            *args = frame info Information passed from other Logger functions

        """
        if message is not None:
            caller = getframeinfo(stack()[1][0])
            print("[ERROR][{}][{}]:{}".format(caller.filename, caller.lineno, message))
        else:
            print("[ERROR][{}][{}]:{}".format(args[2], args[1], args[0]))

    @staticmethod
    def console_d(message=None, *args):
        """
         Output debug information to the console, DEBUGMODE must be true in order for this
         function to do anything

         user must always supply the info string when explicitly calling console_i.
         args is meant for other functions to pass the frame info to the console from
         their call when DEBUGMODE is True

         Params:
            message = Information to be printed to the console
            *args = frame info Information passed from other Logger functions

        """
        if Logger.DEBUGMODE:
            
            if message is not None:
                caller = getframeinfo(stack()[1][0])
                print("[DEBUG][{}][{}]:{}".format(caller.filename, caller.lineno, message))
            else:
                print("[DEBUG][{}][{}]:{}".format(args[2], args[1], args[0]))

    @staticmethod
    def log_info(message):
        """
         Log information into a text file

         when DEBUGMODE is set to true the function will also implicitly call 
         console_i with the correct frame info

         Params:
            message = Information to be logged as a string

        """
        caller = getframeinfo(stack()[1][0])
        
        if Logger.DEBUGMODE:
            Logger.console_i(message, caller.filename, caller.lineno)
        
        Logger.file_object.write("[INFO][{}][{}][{}][{}]:{}\n".format(strftime("%m-%d-%Y"),
                       strftime("%H:%M:%S"), caller.filename, caller.lineno, message))

    #append error information to a log file
    @staticmethod
    def log_error(message):
        """
         Log errors into a text file

         when DEBUGMODE is set to true the function will also implicitly call 
         console_i with the correct frame info

         Params:
            message = message to be logged as a string

        """
        
        caller = getframeinfo(stack()[1][0])
        
        if Logger.DEBUGMODE:
            Logger.console_e(message, caller.filename, caller.lineno)
        
        Logger.file_object.write("[ERROR][{}][{}][{}][{}]:{}\n".format(strftime("%m-%d-%Y"),
                       strftime("%H:%M:%S"), caller.filename, caller.lineno, message))

    @staticmethod
    def log_debug(message):
        """
         Log debug information into a text file

        DEBUG_MODE needs to be activated in order for debug information to be logged 

         Params:
            message = information to be logged as a string

        """
        caller = getframeinfo(stack()[1][0])
        
        if Logger.DEBUGMODE:
            Logger.console_d(message, caller.filename, caller.lineno)
        
            Logger.file_object.write("[DEBUG][{}][{}][{}][{}]:{}\n".format(strftime("%m-%d-%Y"),
                            strftime("%H:%M:%S"), caller.filename, caller.lineno, message))

    @staticmethod
    def close_log():
        """
        close out the file being used to append information to 
        """
        Logger.file_object.close()