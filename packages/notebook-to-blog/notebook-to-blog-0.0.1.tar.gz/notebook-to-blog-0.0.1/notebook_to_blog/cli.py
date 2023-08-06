import os
import click
from pathlib import Path
from dotenv import load_dotenv

from notebook_to_blog.notebook import Notebook


def create_filename(notebook_path):
    return notebook_path.name.split(".")[0] + ".txt"


@click.command()
@click.argument("notebook_path")
@click.argument("output_dir")
@click.argument("gh_cred_filepath")
def main(notebook_path, output_dir, gh_cred_filepath):
    # setup output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # load github credentials into environment
    load_dotenv(dotenv_path=gh_cred_filepath)
    gh_user = os.getenv("GITHUB_USER")
    gh_pw = os.getenv("GITHUB_PASSWORD")

    # create notebook
    notebook_path = Path(notebook_path)
    notebook = Notebook(
        notebook_path, output_dir, {"username": gh_user, "password": gh_pw}
    )

    # convert notebook and save to desired location
    output_filename = create_filename(notebook_path)
    with open(output_dir / output_filename, "w") as f:
        f.write(notebook.convert())
