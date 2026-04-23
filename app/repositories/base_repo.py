from typing import Type, TypeVar, Generic, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, false, true
from sqlalchemy.sql.expression import select, delete, update
from sqlalchemy.ext.declarative import declarative_base

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    """Base repository providing common CRUD operations."""

    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize repository.

        Args:
            model: The SQLAlchemy model class
            db: Database session
        """
        super().__init__()
        self.model = model
        self.db = db

    def get_by_id(self, id: str) -> Optional[ModelType]:
        """
        Get a record by ID.

        Args:
            id: The record ID

        Returns:
            The record if found, None otherwise
        """
        return self.db.query(self.model).filter(
            and_(
                self.model.id == id,
                self.model.is_deleted == false(),
                self.model.is_active == true()
            )
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get all records with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of records
        """
        return self.db.query(self.model).filter(
            and_(
                self.model.is_deleted == false(),
                self.model.is_active == true()
            )
        ).offset(skip).limit(limit).all()

    def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """
        Create a new record.

        Args:
            obj_in: Dictionary containing the record data

        Returns:
            The created record
        """
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, id: str, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        """
        Update a record by ID.

        Args:
            id: The record ID
            obj_in: Dictionary containing the updated data

        Returns:
            The updated record if found, None otherwise
        """
        db_obj = self.get_by_id(id)
        if db_obj:
            for field, value in obj_in.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            self.db.commit()
            self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: str) -> bool:
        """
        Soft delete a record by ID.

        Args:
            id: The record ID

        Returns:
            True if deleted, False otherwise
        """
        db_obj = self.get_by_id(id)
        if db_obj:
            db_obj.is_deleted = True
            self.db.commit()
            return True
        return False

    def hard_delete(self, id: str) -> bool:
        """
        Hard delete a record by ID.

        Args:
            id: The record ID

        Returns:
            True if deleted, False otherwise
        """
        db_obj = self.db.query(self.model).filter(self.model.id == id).first()
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False

    def get_by_field(self, field_name: str, value: Any) -> Optional[ModelType]:
        """
        Get a record by a specific field value.

        Args:
            field_name: The field name to search
            value: The value to match

        Returns:
            The record if found, None otherwise
        """
        if hasattr(self.model, field_name):
            return self.db.query(self.model).filter(
                and_(
                    getattr(self.model, field_name) == value,
                    self.model.is_deleted == false(),
                    self.model.is_active == true()
                )
            ).first()
        return None

    def get_by_fields(self, filters: Dict[str, Any]) -> List[ModelType]:
        """
        Get records by multiple field values.

        Args:
            filters: Dictionary of field names and values to filter by

        Returns:
            List of matching records
        """
        query = self.db.query(self.model).filter(
            and_(
                self.model.is_deleted == false(),
                self.model.is_active == true()
            )
        )
        
        for field_name, value in filters.items():
            if hasattr(self.model, field_name):
                query = query.filter(getattr(self.model, field_name) == value)
        
        return query.all()

    def exists(self, id: str) -> bool:
        """
        Check if a record exists by ID.

        Args:
            id: The record ID

        Returns:
            True if exists, False otherwise
        """
        return self.db.query(self.model).filter(
            and_(
                self.model.id == id,
                self.model.is_deleted == false(),
                self.model.is_active == true()
            )
        ).first() is not None

    def count(self) -> int:
        """
        Get the total count of active records.

        Returns:
            Number of active records
        """
        return self.db.query(self.model).filter(
            and_(
                self.model.is_deleted == false(),
                self.model.is_active == true()
            )
        ).count()

    def activate(self, id: str) -> bool:
        """
        Activate a record by ID.

        Args:
            id: The record ID

        Returns:
            True if activated, False otherwise
        """
        db_obj = self.db.query(self.model).filter(self.model.id == id).first()
        if db_obj:
            db_obj.is_active = True
            self.db.commit()
            return True
        return False

    def deactivate(self, id: str) -> bool:
        """
        Deactivate a record by ID.

        Args:
            id: The record ID

        Returns:
            True if deactivated, False otherwise
        """
        db_obj = self.get_by_id(id)
        if db_obj:
            db_obj.is_active = False
            self.db.commit()
            return True
        return False