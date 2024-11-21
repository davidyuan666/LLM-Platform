from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vagents.models.base_model import Base
from datetime import datetime

'''
pip install aiomysql
pip install sqlalchemy
'''
class DatabaseManager:
    def __init__(self, db_url='mysql+pymysql://root:123456789@127.0.0.1/agentdb'):
        """
        Initializes the DatabaseManager with a database connection.
        
        Args:
            db_url (str): The database URL. Default is set to local MySQL instance.
        """
        # self.db_url = 'mysql+pymysql://root:123456789@agent-mysql/agentdb'
        # self.db_url = 'mysql+pymysql://root:123456789@127.0.0.1/agentdb'
        # self.db_url = 'mysql+pymysql://root:123456789@10.25.34.108/agentdb'
        self.db_url = db_url
        self.engine = None
        self.db_session = None

    def connect(self):
        """
        Establishes the database connection.
        """
        self.engine = create_engine(self.db_url)
        self.db_session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """
        Creates all tables defined in the Base metadata.
        """
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """
        Returns a new database session.
        """
        if not self.db_session:
            raise ValueError("Database is not connected. Call connect() first.")
        return self.db_session()

    def close_session(self, session):
        """
        Closes the given database session.
        """
        session.close()

    def insert_records(self, records):
        """
        Inserts multiple records into the database.
        """
        with self.get_session() as session:
            session.add_all(records)
            session.commit()

    def delete_records(self, condition, Model):
        """
        Deletes records from the database based on a condition.
        """
        with self.get_session() as session:
            session.query(Model).filter(condition).delete()
            session.commit()

    def get_latest_record(self, Model):
        """
        Retrieves the latest record for a given model.
        """
        with self.get_session() as session:
            return session.query(Model).order_by(Model.timestamp.desc()).first()

    def get_all_records(self, Model):
        """
        Retrieves all records for a given model.
        """
        with self.get_session() as session:
            return session.query(Model).all()

    def execute_query(self, query):
        """
        Executes a custom SQL query.
        """
        with self.get_session() as session:
            return session.execute(query)

    def commit_transaction(self, session):
        """
        Commits the current transaction.
        """
        session.commit()

    def rollback_transaction(self, session):
        """
        Rolls back the current transaction.
        """
        session.rollback()