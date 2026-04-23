from app.repositories.base_repo import BaseRepository
from app.db.models.user_model import User
from sqlalchemy.orm import Session


class UserRepo(BaseRepository[User]):
    """Repository for User model operations."""
    
    def __init__(self, db: Session):
        """
        Initialize User repository.

        Args:
            db: Database session
        """
        super().__init__(User, db)
    
    def get_by_email(self, email: str):
        """
        Get user by email address.

        Args:
            email: User's email address

        Returns:
            User if found, None otherwise
        """
        return self.get_by_field("email", email)
    
    def get_by_phone(self, phone: str):
        """
        Get user by phone number.

        Args:
            phone: User's phone number

        Returns:
            User if found, None otherwise
        """
        return self.get_by_field("phone", phone)
    
    def email_exists(self, email: str) -> bool:
        """
        Check if email exists.

        Args:
            email: Email address to check

        Returns:
            True if email exists, False otherwise
        """
        return self.get_by_email(email) is not None
    
    def phone_exists(self, phone: str) -> bool:
        """
        Check if phone exists.

        Args:
            phone: Phone number to check

        Returns:
            True if phone exists, False otherwise
        """
        return self.get_by_phone(phone) is not None
    
    def create(self, data: dict):
        new_user = self.model(**data)

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user