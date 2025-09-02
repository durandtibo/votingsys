# votingsys

<p align="center">
    <a href="https://github.com/durandtibo/votingsys/actions">
        <img alt="CI" src="https://github.com/durandtibo/votingsys/workflows/CI/badge.svg">
    </a>
    <a href="https://github.com/durandtibo/votingsys/actions">
        <img alt="Nightly Tests" src="https://github.com/durandtibo/votingsys/workflows/Nightly%20Tests/badge.svg">
    </a>
    <a href="https://github.com/durandtibo/votingsys/actions">
        <img alt="Nightly Package Tests" src="https://github.com/durandtibo/votingsys/workflows/Nightly%20Package%20Tests/badge.svg">
    </a>
    <a href="https://codecov.io/gh/durandtibo/votingsys">
        <img alt="Codecov" src="https://codecov.io/gh/durandtibo/votingsys/branch/main/graph/badge.svg">
    </a>
    <br/>
    <a href="https://durandtibo.github.io/votingsys/">
        <img alt="Documentation" src="https://github.com/durandtibo/votingsys/workflows/Documentation%20(stable)/badge.svg">
    </a>
    <a href="https://durandtibo.github.io/votingsys/">
        <img alt="Documentation" src="https://github.com/durandtibo/votingsys/workflows/Documentation%20(unstable)/badge.svg">
    </a>
    <br/>
    <a href="https://github.com/psf/black">
        <img  alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
    <a href="https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings">
        <img  alt="Doc style: google" src="https://img.shields.io/badge/%20style-google-3666d6.svg">
    </a>
    <a href="https://github.com/astral-sh/ruff">
        <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;">
    </a>
    <a href="https://github.com/guilatrova/tryceratops">
        <img  alt="Doc style: google" src="https://img.shields.io/badge/try%2Fexcept%20style-tryceratops%20%F0%9F%A6%96%E2%9C%A8-black">
    </a>
    <br/>
    <a href="https://pypi.org/project/votingsys/">
        <img alt="PYPI version" src="https://img.shields.io/pypi/v/votingsys">
    </a>
    <a href="https://pypi.org/project/votingsys/">
        <img alt="Python" src="https://img.shields.io/pypi/pyversions/votingsys.svg">
    </a>
    <a href="https://opensource.org/licenses/BSD-3-Clause">
        <img alt="BSD-3-Clause" src="https://img.shields.io/pypi/l/votingsys">
    </a>
    <br/>
    <a href="https://pepy.tech/project/votingsys">
        <img  alt="Downloads" src="https://static.pepy.tech/badge/votingsys">
    </a>
    <a href="https://pepy.tech/project/votingsys">
        <img  alt="Monthly downloads" src="https://static.pepy.tech/badge/votingsys/month">
    </a>
    <br/>
</p>

A python library implementing some voting systems.

## Data representation

- anonymous
- can have null values
- can have the same ranking

- Test with a lot of candidates

### DataFrame with the rank for each candidate

### DataFrame with the score for each candidate

- descending vs ascending

## Rule

- voter ranks candidates
- single vs multiple winners: https://en.wikipedia.org/wiki/Comparison_of_voting_rules
- Ballot type:
  - single mark
  - ranking
  - truncated ranking
  - ranking with ties
  - rating
- approval and score voting: https://en.wikipedia.org/wiki/Approval_voting
- approve or disapprove of candidates, or decide to express no opinion
- Score each candidate by filling in a number (0 is worst; 9 is best)
- Majority Rule: This concept means that the candidate (choice) receiving more than 50%
of the vote is the winner.
