"""running raw arranger by default - example"""
from pathlib import Path

from kmarotools.basics import logtools

from krawarranger import RawArranger


if __name__ == "__main__":
    this_file_path = Path(__file__).parent.resolve()
    positive_folder = this_file_path.parent.parent
    negative_folder = this_file_path.parent
    logger = logtools.get_fast_logger("RawArranger", this_file_path)
    folder_patterns = ("1.*", "2.*", "3.*", "4.*", "5.*", )
    RawArranger(positive_folder, negative_folder, logger, folder_patterns
                ).run()
