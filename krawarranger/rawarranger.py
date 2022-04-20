"""
------------------------------------------------------------------------------
Kjmaro Negatives Arranger
------------------------------------------------------------------------------
"""
# pylint: disable=too-many-instance-attributes,too-many-arguments
from typing import Tuple, List
from logging import Logger
from pathlib import Path

from kmarotools.basics import filetools, logtools

from .rawerrors import folders_error, files_error


class RawArranger:
    """
    --------------------------------------------------------------------------
    Kjmaro Negatives Arranger
    --------------------------------------------------------------------------
    The purpose of this program is to have and maintain a mirror of the folder
    structure of your pictures with all their corresponding negatives (raw).
    - pos_base_path: The photography/media positives folder
    - neg_base_path: The photography/media negatives folder
    - logger: Python logging.Logger class to attach
    - folder_patterns: Positive sub-folders to handle (based on patterns*)
    - raw_extensions: Extensions assumed to be negative files (filename.ext)
    --------------------------------------------------------------------------
    *patterns: in order to avoid the total scan of the pos/neg_base_path
               folders, only the folders matching the given patterns will be
               scanned in these paths (if provided) eg: ('1.*', '2.*', '4.*')
    --------------------------------------------------------------------------
    """
    LPHS = "[RWA] <NewModulePhase> "
    LRES = "[RWA] <NewResultsBlock> "

    def __init__(self, pos_base_path: Path, neg_base_path: Path,
                 logger: Logger, folder_patterns: Tuple[str, ...] = (),
                 raw_extensions: Tuple[str, ...] = ("RAW", "NEF")) -> None:

        # Input variables to the class
        self.pos_base_path = pos_base_path
        self.neg_base_path = neg_base_path
        self.fld_patterns = folder_patterns
        self.raw_exts = raw_extensions
        self.log = logger

        # Output and result variables
        self._folders_pos_tree: List[Path]
        self._folders_neg_tree: List[Path]
        self._abs_files2move: List[Path]

    def check_folders_tree_integrity(self) -> List[Path]:
        """
        ----------------------------------------------------------------------
        Verify that all folders in NEGATIVES already exist in POSITIVES
        > return List[Path(relative_to)] of discrepances
        ----------------------------------------------------------------------
        """
        self.log.info(f"{self.LPHS}Checking folders integrity...")
        positive_tree = filetools.get_folders_tree(self.pos_base_path,
                                                   self.fld_patterns)
        negative_tree = filetools.get_folders_tree(self.neg_base_path,
                                                   self.fld_patterns)

        self._folders_pos_tree = positive_tree
        self._folders_neg_tree = negative_tree

        rel_pos_tree = [x.relative_to(self.pos_base_path
                                      ) for x in positive_tree]
        neg_pos_tree = [x.relative_to(self.neg_base_path
                                      ) for x in negative_tree]

        discrepances = []
        for relpath in neg_pos_tree:
            if relpath not in rel_pos_tree:
                discrepances.append(relpath)

        if discrepances:
            self.log.warning(f"{self.LRES}Folder discrepances found = %s",
                             len(discrepances))
            for dscrp in discrepances:
                self.log.warning(str(dscrp))
        return discrepances

    def check_files_tree_integrity(self) -> List[Path]:
        """
        ----------------------------------------------------------------------
        Verify that all files in POSITIVES to be moved to NEGATIVES doesn't
        exist already in NEGATIVES
        > return List[Path] of discrepances (files duplicated)
        ----------------------------------------------------------------------
        """
        inf_msg = f"{self.LPHS}Checking already existing negative files..."
        self.log.info(inf_msg)
        files2move = filetools.get_files_tree(self._folders_pos_tree,
                                              self.raw_exts, True)

        files_in_neg = filetools.get_files_tree(self._folders_neg_tree,
                                                self.raw_exts, True)
        self._abs_files2move = files2move

        rel_files2move = [x.relative_to(self.pos_base_path
                                        ) for x in files2move]
        rel_files_in_neg = [x.relative_to(self.neg_base_path
                                          ) for x in files_in_neg]

        discrepances = []
        for relfile in rel_files2move:
            if relfile in rel_files_in_neg:
                discrepances.append(relfile)

        if discrepances:
            wmsg = f"{self.LRES}Files already existing in negatives %s %s"
            self.log.warning(wmsg, "found =", len(discrepances))
            for dscrp in discrepances:
                self.log.warning(str(dscrp))
        return discrepances

    def move_neg_files_to_neg_folder(self) -> None:
        """
        ----------------------------------------------------------------------
        Move all the negatives to its corresponding folder, creating it if
        needed and all the intermediate required folders
        return folders_created, files_moved, errors_found: bool
        ----------------------------------------------------------------------
        """
        imsg = f"{self.LPHS}Moving negative files to its destination %s"
        self.log.info(imsg, "folder...")
        paths2create = filetools.get_folders_from_files(self._abs_files2move)
        rel_paths2create = [x.relative_to(
            self.pos_base_path) for x in paths2create]
        rel_files2move = [x.relative_to(
            self.pos_base_path) for x in self._abs_files2move]

        rel_flds_crted = filetools.replicate_folders_in_path(
            rel_paths2create, self.neg_base_path)
        self.log.info(f"{self.LRES}Total folders created = %s",
                      len(rel_flds_crted))
        for folder in rel_flds_crted:
            self.log.info("[RWA] [FolderCreated]: %s", folder)

        rel_moved_files = filetools.move_files2destination(
            rel_files2move, self.pos_base_path, self.neg_base_path)
        self.log.info(f"{self.LRES}Total files moved = %s",
                      len(rel_moved_files))
        for filmved in rel_moved_files:
            self.log.info("[RWA] [FileMoved]: %s", filmved)

    def run(self, embedded=False) -> bool:
        """
        ----------------------------------------------------------------------
        Execute RawArranger with the defined configuration
        - log_actions: log the folders created and files moved
        - embedded: It won't stop after successful execution
        ----------------------------------------------------------------------
        return:
            - True: An error was raised during execution
            - False: No error raised during execution
        ----------------------------------------------------------------------
        """
        self.log.info("[RWA] <INIT> RawArranger initialized ...")
        self.log.info(f"[RWA] <CNFG> raw_extnsns = {self.raw_exts}")
        self.log.info(f"[RWA] <CNFG> fld_patterns = {self.fld_patterns}")
        self.log.info(f"[RWA] <CNFG> pos_base_path = {self.pos_base_path}")
        self.log.info(f"[RWA] <CNFG> neg_base_path = {self.neg_base_path}")
        self.log.info("[RWA] <TAGS> [FolderCreated] [FileMoved]")

        if self.check_folders_tree_integrity():
            input(folders_error(self.log))
            return True

        if self.check_files_tree_integrity():
            input(files_error(self.log))
            return True

        self.move_neg_files_to_neg_folder()
        if not embedded:
            input("\nPROCESS FINALIZED\n\t\tPRESS ENTER TO RESUME")
        return False


if __name__ == "__main__":
    # ========================================================================
    # For executing this example remove the '.' in the '.rawerrors' import
    # ========================================================================
    _THIS_FILE_PATH = Path(__file__).parent.resolve()
    _POSITIVE_FOLDER = _THIS_FILE_PATH.parent.parent
    _NEGATIVE_FOLDER = _THIS_FILE_PATH.parent
    _LOGGER = logtools.get_fast_logger("RawArranger", _THIS_FILE_PATH)
    _FOLDER_PATTERNS = ("1.*", "2.*", "3.*", "4.*", "5.*", )
    RawArranger(_POSITIVE_FOLDER, _NEGATIVE_FOLDER, _LOGGER, _FOLDER_PATTERNS
                ).run()
