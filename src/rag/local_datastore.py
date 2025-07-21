import os
import json
from uuid import uuid4
from typing import List

from .retriever import Retriever, Resource, Document, Chunk


class LocalDataStoreProvider(Retriever):
    """Simple local file-based datastore provider"""

    def __init__(self):
        self.data_dir = os.getenv("LOCAL_DATASTORE_DIR", "datasets")
        os.makedirs(self.data_dir, exist_ok=True)
        self.meta_path = os.path.join(self.data_dir, "datasets.json")
        if os.path.exists(self.meta_path):
            with open(self.meta_path, "r", encoding="utf-8") as f:
                self.datasets = json.load(f)
        else:
            self.datasets = []

    def _save_meta(self):
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.datasets, f)

    def create_dataset(self, name: str, files: List[str]):
        dataset_id = str(uuid4())
        ds_path = os.path.join(self.data_dir, dataset_id)
        os.makedirs(ds_path, exist_ok=True)
        for fp in files:
            dest = os.path.join(ds_path, os.path.basename(fp))
            with open(fp, "rb") as src, open(dest, "wb") as dst:
                dst.write(src.read())
        self.datasets.append({"id": dataset_id, "name": name})
        self._save_meta()
        return dataset_id

    def list_resources(self, query: str | None = None) -> List[Resource]:
        resources = []
        for ds in self.datasets:
            if query and query.lower() not in ds["name"].lower():
                continue
            resources.append(Resource(uri=f"rag://dataset/{ds['id']}", title=ds["name"]))
        return resources

    def query_relevant_documents(self, query: str, resources: List[Resource] = []):
        query = query.lower()
        docs = []
        for resource in resources:
            ds_id = resource.uri.split("/")[1]
            ds_path = os.path.join(self.data_dir, ds_id)
            if not os.path.exists(ds_path):
                continue
            for fname in os.listdir(ds_path):
                fpath = os.path.join(ds_path, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        text = f.read()
                except Exception:
                    continue
                if query in text.lower():
                    chunk = Chunk(content=text[:200], similarity=1.0)
                    docs.append(Document(id=fname, title=fname, chunks=[chunk]))
        return docs
