"""Raw Arranger Tools"""
from logging import Logger


def folders_error(logger: Logger) -> str:
    """Error log message"""
    err_msg = "[RWA] Edit the Negatives folders-tree to "
    err_msg += "match the Origin ones before executing the script. "
    err_msg += "RULE: All the Negatives folders must exist in Origin."
    logger.error(err_msg)
    return_msg = "\nERROR: Mismatching folders found. See <RawArranger"
    return_msg += ".log> for more info\n\t\tPRESS ENTER TO RESUME"
    return return_msg


def files_error(logger: Logger) -> str:
    """Error log message"""
    err_msg = "[RWA] Verify if the file in Origin is the same as the one "
    err_msg += "in Negatives. Delete or rename one of the files before "
    err_msg += "executing the script."
    logger.error(err_msg)
    return_msg = "\nERROR: Duplicated files found. See <RawArranger.log> "
    return_msg += "for more info\n\t\tPRESS ENTER TO RESUME"
    return return_msg


def rawmove_error(logger: Logger) -> str:
    """Error log message"""
    err_msg = "[RWA] Errors while creating folders or moving negative files "
    err_msg += "found. This is mainly caused due to permissions error"
    logger.error(err_msg)
    return_msg = "\nERROR: Negatives movement not completed. See <RawArranger."
    return_msg += "log> for more info\n\t\tPRESS ENTER TO RESUME"
    return return_msg
