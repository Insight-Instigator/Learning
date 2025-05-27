from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import get_session
from app.services.book_service import BookService
from app.core.auth import api_key_dependency
import logging
from typing import Any

logger = logging.getLogger(__name__)

router = APIRouter()


@router.delete("/{book_id}", status_code=204, summary="Delete a book by ID")
async def delete_book(
    book_id: int,
    session: AsyncSession = Depends(get_session),
    _: Any = Depends(api_key_dependency)
) -> None:
    """
    Deletes a book record from the database by its ID.

    Args:
        book_id (int): The ID of the book to delete.
        session (AsyncSession): Database session.
        _: Any: Dependency for API key authentication.

    Raises:
        HTTPException: If the book is not found or a database error occurs.
    """
    if book_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid book ID.")

    book_service = BookService(session)

    try:
        deleted = await book_service.delete_book(book_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Book not found.")
    except SQLAlchemyError as e:
        logger.error("Database error in delete_book", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error.")
    except Exception as e:
        logger.error("Unexpected error in delete_book", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error.")
