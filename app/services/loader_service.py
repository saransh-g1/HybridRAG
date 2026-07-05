from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)

SUPPORTED_LOADERS = {
    ".pdf": PyPDFLoader,
    ".txt": TextLoader,
    ".md": UnstructuredMarkdownLoader,
}


class LoaderService:

    def load_directory(self, directory: str = "data"):

        documents = {}

        for file in Path(directory).iterdir():

            if file.suffix not in SUPPORTED_LOADERS:
                continue

            loader = SUPPORTED_LOADERS[file.suffix](str(file))

            documents[str(file)] = loader.load()

        return documents