import github
from github import Github
from loguru import logger


def create_gist(code, gh_creds):
    g = Github(gh_creds["username"], gh_creds["password"])
    user = g.get_user()
    gist = user.create_gist(
        public=False, files={"notebook_gist.py": github.InputFileContent(code)}
    )
    logger.info(f"creating new gist with id={gist.id}")
    return gist.id
