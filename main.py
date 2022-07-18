import argparse

from project_initialization import (
    ProjectInitialization,
)
from git_initialization import (
    GitProjectInitialization,
)

"""
Set arguments for correctly init project
"""
parser = argparse.ArgumentParser(
    description='Process some integers.'
)

parser.add_argument(
    '--framework',
    type=str,
    help='Select framework',
)
parser.add_argument(
    '--path_project',
    type=str,
    help='Set path project',
)
parser.add_argument(
    '--project_name',
    type=str,
    help='Set project name',
)
parser.add_argument(
    '--virtualenv',
    type=str,
    help='Select virtualenv',
)
parser.add_argument(
    '--git_repository',
    type=str,
    help='Select git project specify git',
)


if __name__ == "__main__":

    ProjectInitialization().create_project()
    GitProjectInitialization().init_project()
