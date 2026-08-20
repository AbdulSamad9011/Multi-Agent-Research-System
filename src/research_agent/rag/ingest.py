"""Document ingestion pipeline for the RAG knowledge base.

This scaffold ingests a folder of local .txt/.md files as a placeholder.
Swap `load_source_documents` for real loaders (PDF, web pages, Google
Drive, Notion, Confluence, ...) and swap `InMemoryVectorStore` for a
persistent store (Chroma, FAISS, PGVector, Pinecone) — the interface
below stays the same either way.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Union

from langchain.embeddings import init_embeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from research_agent.config import settings

_SPLITTER = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)


def load_source_documents(source_dir: Union[str, Path]) -> List[Document]:
    """TODO: replace with real loaders (PyPDFLoader, WebBaseLoader,
    GoogleDriveLoader, NotionDBLoader, etc.). This placeholder just reads
    local text/markdown files so the scaffold runs out of the box."""
    source_dir = Path(source_dir)
    docs: List[Document] = []
    for path in source_dir.glob("**/*"):
        if path.suffix.lower() not in {".txt", ".md"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        docs.append(Document(page_content=text, metadata={"source": str(path)}))
    return docs


def build_vectorstore(source_dir: Optional[Union[str, Path]] = None) -> InMemoryVectorStore:
    """Build (or rebuild) the RAG index.

    Pass `source_dir=None` to start with an empty knowledge base (the
    researcher agents will then lean on the web_search tool instead).
    """
    embeddings = init_embeddings(settings.embedding_model)
    store = InMemoryVectorStore(embeddings)

    if source_dir is not None:
        raw_docs = load_source_documents(source_dir)
        if raw_docs:
            chunks = _SPLITTER.split_documents(raw_docs)
            store.add_documents(chunks)

    return store
