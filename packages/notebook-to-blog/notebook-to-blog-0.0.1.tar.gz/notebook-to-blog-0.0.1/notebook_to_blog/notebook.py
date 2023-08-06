import json

from notebook_to_blog.cells import CodeCell, MarkdownCell
from notebook_to_blog.constants import PROJECT_DIR


class Notebook:
    def __init__(self, path, output_dir=None, gh_creds=None):
        self.path = path
        self.output_dir = output_dir
        self.gh_creds = gh_creds

        # load notebook and convert into dictionary
        with open(path, "r") as f:
            self.contents = json.loads(f.read())

        self._load_cells()

    def _load_cells(self):
        self.cells = []
        for i, x in enumerate(self.contents["cells"]):
            if x["cell_type"] == "markdown":
                cell = MarkdownCell(x)
            elif x["cell_type"] == "code":
                cell = CodeCell(i, x, self.output_dir, self.gh_creds)
            else:
                raise TypeError("Unknown cell type.")
            self.cells.append(cell)
        return self.cells

    def convert(self):
        return "\n\n".join([c.convert() for c in self.cells])


if __name__ == "__main__":
    notebook = Notebook(PROJECT_DIR / "tests/test_notebook.ipynb")
    result = notebook.convert()
    import pdb

    pdb.set_trace()
