# -*- coding = utf-8 -*-
# @time:2024/8/26 10:44
# Author:david yuan
# @File:chrome_util.py
# @Software:VeSync
import json
import chromadb
from vagents.vagentic.config import Config
from tqdm import tqdm  # Import tqdm
import os
'''
pip install chromadb
pip install tqdm
'''
from vagents.vagentic.llms.simple_client import OpenAIChatBot
from vagents.vagentic.llms.azure_client import AzureOpenAIChatBot


class ChromaManager:
    def __init__(self, collection_name, use_azure=True):
        """
        Initializes the EmbeddingStorageManager with a specific collection for embeddings.
        Allows selection between AzureOpenAIChatBot and OpenAIChatBot based on the `use_azure` flag.

        Args:
            collection_name (str): The name of the collection to store embeddings.
            use_azure (bool): A flag to choose between AzureOpenAIChatBot (True) or OpenAIChatBot (False).
        """
        self.system_message = None  # Placeholder for system message
        self.collection_name = collection_name

        # Select the appropriate chatbot based on the use_azure flag
        self.chatbot = AzureOpenAIChatBot(system_message=self.system_message) if use_azure else OpenAIChatBot(
            system_message=self.system_message)

        self.client = self.chatbot.get_client()
        self.vector_client = None
        self.persist_directory = None
        self.collection = None
        self._initialize_storage()



    def get_persist_directory(self):
        """
        Returns the path to the persistent directory used for storing embeddings.

        Returns:
            str: The path to the persistent directory.
        """
        return self.persist_directory


    def is_collection_connected(self):
        '''
        Check if the collection is properly connected and operational.
        '''
        try:
            collections = self.vector_client.list_collections()
            if self.collection_name in collections:
                return True
        except Exception as e:
            print(f"Failed to connect to the collection: {e}")
            return False
        return False  # Default to False if other checks do not pass

    def generate_embeddings(self, texts):
        '''
        Generate embeddings for a list of texts using OpenAI's API with a progress bar.
        '''
        embeddings = []
        for text in tqdm(texts, desc="Generating embeddings"):  # tqdm wraps the iterable and displays progress
            response = self.client.embeddings.create(
                input=[text.replace("\n", " ")],
                model="text-embedding-3-small"
            )
            embeddings.append(response.data[0].embedding)
        return texts, embeddings

    def store_embeddings_to_collection(self, texts, embeddings):
        '''
        Bulk store texts along with their embeddings in ChromaDB.
        '''
        self.collection.add(
            documents=texts,  # Assuming the API can handle lists directly
            embeddings=embeddings,
            metadatas=[{"text": text[3:]} for text in texts if len(text) > 3],  # Truncate first 3 characters
            ids=[f"text_{i}" for i in range(len(texts))]  # List of unique IDs
        )

    def store_text_to_collection(self, texts):
        '''
        Bulk store texts along with their embeddings in ChromaDB.
        '''
        self.collection.add(
            documents=texts,  # Assuming the API can handle lists directly
            metadatas=[{"text": text[3:]} for text in texts if len(text) > 3],  # Truncate first 3 characters
            ids=[f"text_{i}" for i in range(len(texts))]  # List of unique IDs
        )


    def load_collection(self):
        self.collection = self.vector_client.get_collection(self.collection_name)
        return self.collection


    def query_similar_texts(self, query_text, n_results=1):
        '''
        Query the collection for similar texts using the generated embeddings.
        '''
        try:
            query_text, query_embeddings = self.generate_embeddings([query_text])
            results = self.collection.query(
                query_embeddings=query_embeddings[0],  # Assuming the first (and only) embedding
                n_results=n_results
            )
            return results['documents']
        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # Or appropriate error handling/return

    def query_similar_docs(self, query_text, n_results=1):
        '''
        Query the collection for similar texts using the generated embeddings.
        '''
        try:
            results = self.collection.query(
                query_texts=[query_text],  # Assuming the first (and only) embedding
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # Or appropriate error handling/return
        
        

    def update_the_collection(self, collection_name):
        """
        Updates the current collection to a new collection.

        Args:
            collection_name (str): The name of the new collection to switch to.
        """
        self.collection_name = collection_name
        self.persist_directory = self._get_persist_directory(collection_name)
        self.collection = self.vector_client.get_or_create_collection(name=self.collection_name)
        print(f"=====> Updated to new collection: {self.collection_name}")
        print(f"=====> Persist directory updated to: {self.persist_directory}")



    def update_the_collection(self, collection_name):
        """
        Updates the current collection to a new collection.

        Args:
            collection_name (str): The name of the new collection to switch to.
        """
        self.collection_name = collection_name
        self.persist_directory = self._get_persist_directory(collection_name)
        self.vector_client = self._initialize_client(self.persist_directory)  # Reinitialize client for new directory
        self.collection = self.vector_client.get_or_create_collection(name=self.collection_name)
        print(f"=====> Updated to new collection: {self.collection_name}")
        print(f"=====> Persist directory updated to: {self.persist_directory}")

    def _initialize_storage(self):
        """
        Initializes storage directories and vector client for managing embeddings.
        """
        self.persist_directory = os.path.join(os.getcwd(), 'knowledgebase', f'storage_{self.collection_name}')
        self.vector_client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.vector_client.get_or_create_collection(name=self.collection_name)
        print(f"=====> Persist directory set up at: {self.persist_directory}")


    def _initialize_client(self, persist_directory):
        """
        Initializes the PersistentClient for the given directory.

        Args:
            persist_directory (str): The directory to store embeddings.

        Returns:
            PersistentClient: An instance of the PersistentClient.
        """
        return chromadb.PersistentClient(path=persist_directory)
    


    def _get_persist_directory(self, collection_name):
        """
        Generates the persist directory path based on the collection name.

        Args:
            collection_name (str): The name of the collection.

        Returns:
            str: The path to the persistent directory for the collection.
        """
        return os.path.join(os.getcwd(), 'knowledgebase', f'storage_{collection_name}')
    

    
    def process_recipe_json(self, json_file_path):
        """
        Reads a JSON file containing recipe data, generates embeddings for recipe names,
        steps, and ingredients, and stores them in the collection.

        Args:
            json_file_path (str): Path to the JSON file containing recipe data.

        Returns:
            int: Number of recipes processed successfully.
        """
        processed_recipes = 0

        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                recipes = json.load(file)

            for recipe_name, recipe_data in recipes.items():
                # Generate embeddings for recipe name
                name_embedding = self.generate_embeddings([recipe_name])[1][0]

                # Generate embeddings for steps
                steps = ' '.join(recipe_data['steps'])
                steps_embedding = self.generate_embeddings([steps])[1][0]

                # Generate embeddings for ingredients
                ingredients = ' '.join(recipe_data['ingredients'])
                ingredients_embedding = self.generate_embeddings([ingredients])[1][0]

                # Store embeddings in the collection
                self.collection.add(
                    documents=[recipe_name, steps, ingredients],
                    embeddings=[name_embedding, steps_embedding, ingredients_embedding],
                    metadatas=[
                        {"type": "recipe_name", "recipe": recipe_name},
                        {"type": "steps", "recipe": recipe_name},
                        {"type": "ingredients", "recipe": recipe_name}
                    ],
                    ids=[f"{recipe_name}_name", f"{recipe_name}_steps", f"{recipe_name}_ingredients"]
                )

                processed_recipes += 1
                print(f"Processed recipe: {recipe_name}")

        except Exception as e:
            print(f"Error processing JSON file: {str(e)}")

        print(f"Total recipes processed: {processed_recipes}")
        return processed_recipes

    



