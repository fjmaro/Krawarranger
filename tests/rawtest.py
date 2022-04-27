"""rawarranger test"""
from pathlib import Path
import shutil
import os

from kjmarotools.basics import logtools

from krawarranger import RawArranger


def rawtest():
    """raw test"""
    here = Path(__file__).parent.resolve()
    output_folder = here.joinpath("datasets/_temporal")
    os.makedirs(output_folder, exist_ok=True)

    logger = logtools.get_fast_logger("rawtest", output_folder)
    pos_base_path = here.joinpath("datasets/totest")
    neg_base_path = output_folder

    if pos_base_path.exists():
        shutil.rmtree(pos_base_path)
    shutil.copytree(here.joinpath("datasets/originals"), pos_base_path)

    rwr = RawArranger(pos_base_path, neg_base_path, logger,
                      ("1*", "2*", "3*", "4*", "5*"))
    errors_found = rwr.run()

    print("\nERRORS IN TEST:", errors_found, "\n")
    input("Press ENTER to delete test results")
    try:
        shutil.rmtree(output_folder)
    except PermissionError:
        pass


if __name__ == "__main__":
    rawtest()
