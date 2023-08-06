
import json
from pathlib import Path
from notebook.utils import url_path_join
from ._version import __version__
from .doc import DocumentHandler

HERE = Path(__file__).parent.resolve()

with (HERE / "labextension" / "package.json").open() as fid:
    data = json.load(fid)

def _jupyter_server_extension_paths():
    return [{
        "module": "jupyter-rightbar-doc"
    }]

def _load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.
    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    # Prepend the base_url so that it works in a jupyterhub setting
    base_url = web_app.settings['base_url']
    handlers = [(url_path_join(base_url, 'codelab_doc'),  DocumentHandler)]
    web_app.add_handlers('.*$', handlers)

load_jupyter_server_extension = _load_jupyter_server_extension