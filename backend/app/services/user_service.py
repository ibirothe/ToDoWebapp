from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from app.schemas.user_schema import UserAuth
from app.models.user_model import User
from app.core.security import get_password, verify_password

class UserService:
    """
    Service layer for managing user creation, authentication,
    and database queries.
    """

    @staticmethod
    async def create_user(user: UserAuth) -> User:
        """
        Create and save a new user with hashed password.

        Args:
            user (UserAuth): Input user data.

        Returns:
            User: The created user instance.
        """
        if await User.find_one({"email": user.email}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
        )
    
        if await User.find_one(User.username == user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        user_in = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password(user.password)
        )
        await user_in.save()
        return user_in

    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        """
        Verify user credentials.

        Args:
            email (str): User email.
            password (str): Plaintext password.

        Returns:
            Optional[User]: User if authenticated, else None.
        """
        user = await UserService.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_password=user.hashed_password):
            return None
        return user
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """
        Find a user by email.

        Args:
            email (str): Email to search.

        Returns:
            Optional[User]: User if found, else None.
        """
        user = await User.find_one(User.email == email)
        return user
    
    @staticmethod
    async def get_user_by_id(id: UUID) -> Optional[User]:
        """
        Find a user by UUID.

        Args:
            id (UUID): User ID.

        Returns:
            Optional[User]: User if found, else None.
        """
        user = await User.find_one(User.user_id == id)
        return user
