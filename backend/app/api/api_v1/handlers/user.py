from fastapi import APIRouter, HTTPException, status
from app.schemas.user_schema import UserAuth, UserOut, UserUpdate
from fastapi import Depends
from app.services.user_service import UserService
import pymongo
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user
import sys
import traceback


user_router = APIRouter()

@user_router.post('/create', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    """
    Create a new user in the system.

    Args:
        data (UserAuth): User authentication data including email, username, and password.

    Returns:
        UserOut: Details of the newly created user.

    Raises:
        HTTPException: If a user with the same email or username already exists.
    """
    try:
        print(f"=== Attempting to create user: {data.email} ===", file=sys.stderr)
        result = await UserService.create_user(data)
        print(f"=== User created successfully ===", file=sys.stderr)
        return result
    except pymongo.errors.DuplicateKeyError as e:
        print(f"=== Duplicate key error: {str(e)} ===", file=sys.stderr)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exist"
        )
    except Exception as e:
        print(f"=== UNEXPECTED ERROR ===", file=sys.stderr)
        print(f"Error type: {type(e).__name__}", file=sys.stderr)
        print(f"Error message: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@user_router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    """
    Retrieve the details of the currently authenticated user.

    Args:
        user (User, optional): The currently logged-in user, injected via dependency.

    Returns:
        UserOut: Details of the authenticated user.
    """
    return user


@user_router.post('/update', summary='Update User', response_model=UserOut)
async def update_user(data: UserUpdate, user: User = Depends(get_current_user)):
    """
    Update the authenticated user's information.

    Args:
        data (UserUpdate): The fields to update for the user.
        user (User, optional): The currently logged-in user, injected via dependency.

    Returns:
        UserOut: Updated details of the user.

    Raises:
        HTTPException: If the user does not exist in the database.
    """
    try:
        return await UserService.update_user(user.user_id, data)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )
