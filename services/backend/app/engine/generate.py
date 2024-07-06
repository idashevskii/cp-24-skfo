from copy import deepcopy
from typing import Any, Dict, List, Sequence, cast
from dotenv import load_dotenv
from llama_index.core.schema import BaseNode, TextNode, TransformComponent

load_dotenv()

import os
import logging
from llama_index.core.settings import Settings
from llama_index.core.ingestion import DocstoreStrategy, IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage import StorageContext
from app.settings import init_settings
from app.engine.loaders import get_documents
from app.engine.vectordb import get_vector_store


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

STORAGE_DIR = os.getenv("STORAGE_DIR", "storage")


def get_doc_store():

    # If the storage directory is there, load the document store from it.
    # If not, set up an in-memory document store since we can't load from a directory that doesn't exist.
    if os.path.exists(STORAGE_DIR):
        return SimpleDocumentStore.from_persist_dir(STORAGE_DIR)
    else:
        return SimpleDocumentStore()


class UrlMetadataExtractor(TransformComponent):

    def extract_headers(self, text: str):
        lines = text.split("\n", maxsplit=10)
        res_text = []
        res_meta = {}
        for line in lines:
            line_consumed = False
            for doc_key, meta_key in [
                ("url", "document_url"),
                ("title", "document_title"),
            ]:
                prefix = f"{doc_key}:"
                if line.startswith(prefix):
                    res_meta[meta_key] = line.removeprefix(prefix).strip()
                    line_consumed = True
                    break
            if line_consumed:
                continue
            res_text.append(line)

        return "\n".join(res_text).strip(), res_meta

    def extract_metadata(self, node: BaseNode):
        if isinstance(node, TextNode):
            node.text, headers = self.extract_headers(cast(TextNode, node).text)
            node.metadata.update(headers)
        return node

    def __call__(self, nodes: List[BaseNode], **kwargs: Any) -> List[BaseNode]:
        return [deepcopy(self.extract_metadata(node)) for node in nodes]


def run_pipeline(docstore, vector_store, documents):
    pipeline = IngestionPipeline(
        transformations=[
            UrlMetadataExtractor(),
            SentenceSplitter(
                chunk_size=Settings.chunk_size,
                chunk_overlap=Settings.chunk_overlap,
            ),
            Settings.embed_model,
        ],
        docstore=docstore,
        docstore_strategy=DocstoreStrategy.UPSERTS_AND_DELETE,
        vector_store=vector_store,
    )

    # Run the ingestion pipeline and store the results
    nodes = pipeline.run(show_progress=True, documents=documents)

    return nodes


def persist_storage(docstore, vector_store):
    storage_context = StorageContext.from_defaults(
        docstore=docstore,
        vector_store=vector_store,
    )
    storage_context.persist(STORAGE_DIR)


def generate_datasource():
    init_settings()
    logger.info("Generate index for the provided data")

    # Get the stores and documents or create new ones
    documents = get_documents()
    docstore = get_doc_store()
    vector_store = get_vector_store()

    # Run the ingestion pipeline
    _ = run_pipeline(docstore, vector_store, documents)

    # Build the index and persist storage
    persist_storage(docstore, vector_store)

    logger.info("Finished generating the index")


if __name__ == "__main__":
    generate_datasource()
