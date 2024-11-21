from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
import redis
from typing import Any, Optional, Type, List
import json
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create base class for SQLAlchemy models
Base = declarative_base()

'''
mysql -h 10.37.34.236 -P 3306 -u ecdbuser -p
'''
class DatabaseUtil:
    def __init__(self, use_root=False):
        """
        Initialize database connections.
        Args:
            use_root: Boolean to determine whether to use root or ecdbuser credentials
        """
        # MySQL configuration using SQLAlchemy
        if use_root:
            self.mysql_url = "mysql+mysqlconnector://root:vesync#ai#2024@10.37.34.236/your_database"
        else:
            self.mysql_url = "mysql+mysqlconnector://ecdbuser:Fe98321$3@10.37.34.236/your_database"
        
        # Redis configuration
        self.redis_config = {
            'host': '98.83.141.1721',
            'port': 6379,
            'password': 'Tc@258',
            'db': 0,
            'decode_responses': True  # Automatically decode responses to Python strings
        }
        
        # Initialize connections
        self._init_mysql()
        self._init_redis()
        
    def _init_mysql(self):
        """Initialize MySQL connection with SQLAlchemy."""
        try:
            self.engine = create_engine(
                self.mysql_url,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=3600,
                # Add special handling for the # character in password
                connect_args={
                    'auth_plugin': 'mysql_native_password'
                }
            )
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            Base.metadata.create_all(bind=self.engine)
            logger.info("MySQL connection initialized successfully")
        except Exception as e:
            logger.error(f"MySQL initialization error: {str(e)}")
            raise

    def _init_redis(self):
        """Initialize Redis connection."""
        try:
            self.redis_conn = redis.Redis(**self.redis_config)
            self.redis_conn.ping()  # Test connection
            logger.info("Redis connection initialized successfully")
        except Exception as e:
            logger.error(f"Redis initialization error: {str(e)}")
            raise

    @contextmanager
    def get_db_session(self):
        """Provide a transactional scope around a series of operations."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Session error: {str(e)}")
            raise
        finally:
            session.close()

    # ... (rest of the methods remain the same)