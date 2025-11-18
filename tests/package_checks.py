from __future__ import annotations

import importlib
import logging

logger = logging.getLogger(__name__)


def check_imports() -> None:
    logger.info("Checking imports...")
    objects_to_import = [
        "votingsys.vote.BaseVote",
        "votingsys.vote.MultipleWinnersFoundError",
        "votingsys.vote.RankedVote",
        "votingsys.vote.SingleMarkVote",
    ]
    for a in objects_to_import:
        module_path, name = a.rsplit(".", maxsplit=1)
        module = importlib.import_module(module_path)
        obj = getattr(module, name)
        assert obj is not None


def main() -> None:
    check_imports()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
