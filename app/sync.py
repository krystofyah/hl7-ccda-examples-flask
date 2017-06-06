#!flask/bin/python
from app.db import db
import os.path
import git
import ipdb
import git
import shutil
from parse_meta_data import parse
from db import GIT_URL, GIT_BRANCH


def sync():

    #   repo = git.Repo(folder)
    repo =  git.Repo.clone_from(GIT_URL, "./ccda_examples_repo")


    LOCAL_EXAMPLES_REPO_DIR = "./ccda_examples_repo"

    shutil.rmtree(LOCAL_EXAMPLES_REPO_DIR)
    repo = git.Repo.clone_from(GIT_URL, LOCAL_EXAMPLES_REPO_DIR)
    repo.git.pull("origin", GIT_BRANCH)
    repo.git.fetch()
    parse(repo, LOCAL_EXAMPLES_REPO_DIR)
    basedir = os.path.abspath(os.path.dirname(__file__))

    sections = db.sections.find().count()
    examples = db.examples.find().count()
    return "loaded {} sections and {} examples".format(sections, examples)
