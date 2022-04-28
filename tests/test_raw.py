"""rawarranger test"""
from pathlib import Path
import shutil
import os

from kjmarotools.basics import logtools, filetools

from krawarranger import RawArranger


def test_raw():
    """raw test"""
    here = Path(__file__).parent.resolve()
    output_folder = here.joinpath("datasets/negs_path")
    os.makedirs(output_folder, exist_ok=True)

    logger = logtools.get_fast_logger("rawtest", here)
    pos_base_path = here.joinpath("datasets/pos_path")
    neg_base_path = output_folder

    if pos_base_path.exists():
        shutil.rmtree(pos_base_path)
    if output_folder.exists():
        shutil.rmtree(output_folder)
    shutil.copytree(here.joinpath("datasets/_originals_"), pos_base_path)

    pattrn = ("1*", "2*", "3*", "4*", "5*")
    rwr = RawArranger(pos_base_path, neg_base_path, logger, pattrn)
    errors_found = rwr.run(embedded=True)
    assert not errors_found

    # Verify the results in negatives
    neg2comp_path = here.joinpath("datasets/_negs_path_")
    files_neg2cmp = filetools.get_files_tree(
        filetools.get_folders_tree(neg2comp_path, pattrn))
    files_neg2cmp = [x.relative_to(neg2comp_path) for x in files_neg2cmp]

    files_neg_res = filetools.get_files_tree(
        filetools.get_folders_tree(output_folder, pattrn))
    files_neg_res = [x.relative_to(output_folder) for x in files_neg_res]
    assert len(files_neg2cmp) == len(files_neg_res), "Error in Negatives"
    for file in files_neg2cmp:
        assert file in files_neg_res
    for file in files_neg_res:
        assert file in files_neg2cmp

    # Verify the results in positives
    pos2comp_path = here.joinpath("datasets/_pos_path_")
    files_pos2cmp = filetools.get_files_tree(
        filetools.get_folders_tree(pos2comp_path, pattrn))
    files_pos2cmp = [x.relative_to(pos2comp_path) for x in files_pos2cmp]

    files_pos_res = filetools.get_files_tree(
        filetools.get_folders_tree(pos_base_path, pattrn))
    files_pos_res = [x.relative_to(pos_base_path) for x in files_pos_res]
    assert len(files_pos2cmp) == len(files_pos_res), "Error in Positives"
    for file in files_pos2cmp:
        assert file in files_pos_res
    for file in files_pos_res:
        assert file in files_pos2cmp


if __name__ == "__main__":
    test_raw()
