from abc import ABC, abstractmethod


@abstractmethod
def connect(self):
    """Establish connection to the database."""
    pass

@abstractmethod
def disconnect(self):
    """Close the database connection."""
    pass

@abstractmethod
def execute_query(self, query, params=None):
    """Execute a single query (INSERT, UPDATE, DELETE)."""
    pass

@abstractmethod
def fetch_all(self, query, params=None):
    """Fetch all results for a SELECT query."""
    pass

@abstractmethod
def fetch_one(self, query, params=None):
    """Fetch one result for a SELECT query."""
    pass
