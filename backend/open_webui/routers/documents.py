"""
Sirru Documents API Router
REST API endpoints for the Docs AI module
"""

import logging
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel

from open_webui.models.documents import (
    Documents,
    DocumentModel,
    DocumentUserModel,
    DocumentForm,
    DocumentUpdateForm,
    DocumentResponse,
)
from open_webui.utils.auth import get_current_user, get_admin_user
from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()

####################
# Document Endpoints
####################


@router.get("/", response_model=List[DocumentUserModel])
async def get_documents(
    user=Depends(get_current_user),
    include_archived: bool = Query(False, description="Include archived documents"),
):
    """
    Get all documents accessible by the current user
    """
    return Documents.get_documents_by_user_id(user.id, permission="read")


@router.post("/", response_model=DocumentModel)
async def create_document(form_data: DocumentForm, user=Depends(get_current_user)):
    """
    Create a new document
    """
    document = Documents.create_document(user.id, form_data)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create document",
        )
    return document


@router.get("/templates", response_model=List[DocumentModel])
async def get_templates(
    user=Depends(get_current_user),
    organization_id: Optional[str] = Query(None, description="Filter by organization"),
):
    """
    Get all document templates
    """
    return Documents.get_templates(organization_id)


@router.get("/search", response_model=List[DocumentModel])
async def search_documents(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(20, ge=1, le=100),
    user=Depends(get_current_user),
):
    """
    Search documents by title or content
    """
    return Documents.search_documents(q, user.id, limit)


@router.get("/{id}", response_model=DocumentResponse)
async def get_document_by_id(id: str, user=Depends(get_current_user)):
    """
    Get a specific document by ID
    """
    if not Documents.check_access_by_user_id(id, user.id, permission="read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    document = Documents.get_document_by_id(id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    # Calculate word count
    word_count = 0
    character_count = 0
    if document.content:
        character_count = len(document.content)
        word_count = len(document.content.split())

    return DocumentResponse(
        **document.model_dump(),
        word_count=word_count,
        character_count=character_count,
    )


@router.put("/{id}", response_model=DocumentModel)
async def update_document(
    id: str, form_data: DocumentUpdateForm, user=Depends(get_current_user)
):
    """
    Update a document
    """
    if not Documents.check_access_by_user_id(id, user.id, permission="write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    document = Documents.update_document_by_id(id, form_data)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update document",
        )
    return document


class ContentUpdateForm(BaseModel):
    content: str
    content_json: Optional[dict] = None


@router.put("/{id}/content", response_model=DocumentModel)
async def update_document_content(
    id: str, form_data: ContentUpdateForm, user=Depends(get_current_user)
):
    """
    Update document content (for auto-save)
    """
    if not Documents.check_access_by_user_id(id, user.id, permission="write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    document = Documents.update_document_content(
        id, form_data.content, form_data.content_json
    )
    if not document:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update document content",
        )
    return document


@router.delete("/{id}")
async def delete_document(id: str, user=Depends(get_current_user)):
    """
    Delete a document
    """
    if not Documents.check_access_by_user_id(id, user.id, permission="write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    success = Documents.delete_document_by_id(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete document",
        )
    return {"success": True}


@router.post("/{id}/archive", response_model=DocumentModel)
async def archive_document(id: str, user=Depends(get_current_user)):
    """
    Archive a document (soft delete)
    """
    if not Documents.check_access_by_user_id(id, user.id, permission="write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    document = Documents.archive_document_by_id(id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to archive document",
        )
    return document


@router.post("/{id}/duplicate", response_model=DocumentModel)
async def duplicate_document(id: str, user=Depends(get_current_user)):
    """
    Duplicate a document
    """
    if not Documents.check_access_by_user_id(id, user.id, permission="read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    original = Documents.get_document_by_id(id)
    if not original:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    # Create a copy
    new_document = Documents.create_document(
        user.id,
        DocumentForm(
            title=f"{original.title} (Copy)",
            content=original.content,
            content_json=original.content_json,
            document_type=original.document_type,
            tags=original.tags,
            folder_id=original.folder_id,
            is_template=False,  # Copies are not templates
            organization_id=original.organization_id,
        ),
    )

    if not new_document:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to duplicate document",
        )
    return new_document


@router.post("/{id}/publish", response_model=DocumentModel)
async def publish_document(id: str, user=Depends(get_current_user)):
    """
    Publish a document
    """
    if not Documents.check_access_by_user_id(id, user.id, permission="write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    document = Documents.update_document_by_id(
        id, DocumentUpdateForm(is_published=True)
    )
    if not document:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish document",
        )
    return document
