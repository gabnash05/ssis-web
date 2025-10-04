"""
Base model class providing common database operations and error handling.
"""
from typing import Dict, Any, List, Optional, TypeVar, Generic
from abc import ABC, abstractmethod
from ..db.database import execute_sql
import logging

T = TypeVar('T')

logger = logging.getLogger(__name__)


class ModelError(Exception):
    """Base exception for model-related errors."""
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(ModelError):
    """Raised when data validation fails."""
    pass


class DatabaseError(ModelError):
    """Raised when database operations fail."""
    pass


class NotFoundError(ModelError):
    """Raised when a record is not found."""
    pass


class BaseModel(ABC, Generic[T]):
    """Base model class with common database operations."""
    
    @property
    @abstractmethod
    def table_name(self) -> str:
        """Return the database table name for this model."""
        pass
    
    @property
    @abstractmethod
    def primary_key(self) -> str:
        """Return the primary key column name."""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary."""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """Create model instance from dictionary."""
        pass
    
    def _execute_query(self, query: str, params: Dict[str, Any] = None) -> Any:
        """Execute a database query with error handling."""
        try:
            result = execute_sql(query, params or {})
            return result
        except Exception as e:
            logger.error(f"Database query failed: {query}, params: {params}, error: {str(e)}")
            raise DatabaseError(
                f"Database operation failed: {str(e)}",
                error_code="DATABASE_ERROR",
                details={"query": query, "params": params}
            )
    
    def _validate_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> None:
        """Validate that all required fields are present and not empty."""
        missing_fields = []
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == "":
                missing_fields.append(field)
        
        if missing_fields:
            raise ValidationError(
                f"Missing required fields: {', '.join(missing_fields)}",
                error_code="MISSING_REQUIRED_FIELDS",
                details={"missing_fields": missing_fields}
            )
    
    def _build_search_filter(self, search_by: str, search_term: str, searchable_fields: List[str]) -> tuple:
        """Build search filter clause and parameters, with casting for numeric fields."""
        if not search_term:
            return "", {}
        
        params = {"search_term": f"%{search_term}%"}

        numeric_fields = {"year_level"}  

        if search_by and search_by in searchable_fields:
            if search_by in numeric_fields:
                filters = f"WHERE CAST({search_by} AS TEXT) ILIKE :search_term"
            else:
                filters = f"WHERE {search_by} ILIKE :search_term"
        else:
            conditions = []
            for field in searchable_fields:
                if field in numeric_fields:
                    conditions.append(f"CAST({field} AS TEXT) ILIKE :search_term")
                else:
                    conditions.append(f"{field} ILIKE :search_term")
            filters = f"WHERE {' OR '.join(conditions)}"
        
        return filters, params
    
    def _build_sort_clause(self, sort_by: str, sort_order: str, allowed_sort_fields: List[str]) -> str:
        """Build ORDER BY clause with validation."""
        if sort_by not in allowed_sort_fields:
            sort_by = allowed_sort_fields[0]  # Default to first allowed field
        
        if sort_order.upper() not in ["ASC", "DESC"]:
            sort_order = "ASC"
        
        return f"ORDER BY {sort_by} {sort_order.upper()}"
    
    def _build_pagination_clause(self, limit: int, offset: int) -> str:
        """Build LIMIT and OFFSET clause."""
        return f"LIMIT {limit} OFFSET {offset}"

