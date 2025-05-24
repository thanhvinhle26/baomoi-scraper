class CrawlerError(Exception):
    """Base exception for crawler-related errors"""
    pass

class AnalysisError(Exception):
    """Exception for analysis failures"""
    pass

class StorageError(Exception):
    """Exception for storage operations"""
    pass