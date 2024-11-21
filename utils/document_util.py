# -*- coding = utf-8 -*-
# @time:2024/8/27 16:38
# Author:david yuan
# @File:load_data.py
# @Software:VeSync

import os
import argparse
from tqdm import tqdm
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..')))

from vagents.manager.chroma_manager import ChromaManager

class DocumentUtil:
    def __init__(self):
        self.db = ChromaManager('doc_db')

    def embed_and_store_documents(self,documents_directory): 
        documents = []
        metadatas = []
        files = os.listdir(documents_directory)
        for filename in files:
            with open(f"{documents_directory}/{filename}", "r") as file:
                for line_number, line in enumerate(
                        tqdm((file.readlines()), desc=f"Reading {filename}"), 1
                ):
                    line = line.strip()
                    if len(line) == 0:
                        continue
                    documents.append(line)
                    metadatas.append({"filename": filename, "line_number": line_number})

        collection = self.db.load_collection()

        count = collection.count()
        print(f"Collection already contains {count} documents")
        ids = [str(i) for i in range(count, count + len(documents))]

        for i in tqdm(
                range(0, len(documents), 100), desc="Adding documents", unit_scale=100
        ):
            collection.add(
                ids=ids[i: i + 100],
                documents=documents[i: i + 100],
                metadatas=metadatas[i: i + 100],  # type: ignore
            )

        new_count = collection.count()
        print(f"Added {new_count - count} documents")
