"""
Sirru Presentations API Router
REST API endpoints for the Slides AI module
"""

import logging
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel

from open_webui.models.presentations import (
    Presentations,
    PresentationModel,
    PresentationUserModel,
    PresentationForm,
    PresentationUpdateForm,
    PresentationResponse,
    GeneratePresentationForm,
)
from open_webui.utils.auth import get_current_user, get_admin_user
from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()

####################
# Presentation Endpoints
####################


@router.get("/", response_model=List[PresentationUserModel])
async def get_presentations(
    user=Depends(get_current_user),
    include_archived: bool = Query(False, description="Include archived presentations"),
):
    """
    Get all presentations accessible by the current user
    """
    return Presentations.get_presentations_by_user_id(user.id, permission="read")


@router.post("/", response_model=PresentationModel)
async def create_presentation(
    form_data: PresentationForm, user=Depends(get_current_user)
):
    """
    Create a new presentation
    """
    presentation = Presentations.create_presentation(user.id, form_data)
    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create presentation",
        )
    return presentation


@router.get("/themes", response_model=List[dict])
async def get_themes(user=Depends(get_current_user)):
    """
    Get available presentation themes
    """
    return Presentations.get_available_themes()


@router.get("/templates", response_model=List[PresentationModel])
async def get_templates(
    user=Depends(get_current_user),
    organization_id: Optional[str] = Query(None, description="Filter by organization"),
):
    """
    Get all presentation templates
    """
    return Presentations.get_templates(organization_id)


@router.get("/{id}", response_model=PresentationResponse)
async def get_presentation_by_id(id: str, user=Depends(get_current_user)):
    """
    Get a specific presentation by ID
    """
    if not Presentations.check_access_by_user_id(id, user.id, permission="read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    presentation = Presentations.get_presentation_by_id(id)
    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Presentation not found",
        )

    return presentation


@router.put("/{id}", response_model=PresentationModel)
async def update_presentation(
    id: str, form_data: PresentationUpdateForm, user=Depends(get_current_user)
):
    """
    Update a presentation
    """
    if not Presentations.check_access_by_user_id(id, user.id, permission="write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    presentation = Presentations.update_presentation_by_id(id, form_data)
    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update presentation",
        )
    return presentation


class SlidesUpdateForm(BaseModel):
    slides: List[dict]


@router.put("/{id}/slides", response_model=PresentationModel)
async def update_slides(
    id: str, form_data: SlidesUpdateForm, user=Depends(get_current_user)
):
    """
    Update presentation slides (for auto-save)
    """
    if not Presentations.check_access_by_user_id(id, user.id, permission="write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    presentation = Presentations.update_slides(id, form_data.slides)
    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update slides",
        )
    return presentation


@router.delete("/{id}")
async def delete_presentation(id: str, user=Depends(get_current_user)):
    """
    Delete a presentation
    """
    if not Presentations.check_access_by_user_id(id, user.id, permission="write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    success = Presentations.delete_presentation_by_id(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete presentation",
        )
    return {"success": True}


@router.post("/{id}/archive", response_model=PresentationModel)
async def archive_presentation(id: str, user=Depends(get_current_user)):
    """
    Archive a presentation (soft delete)
    """
    if not Presentations.check_access_by_user_id(id, user.id, permission="write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    presentation = Presentations.archive_presentation_by_id(id)
    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to archive presentation",
        )
    return presentation


@router.post("/{id}/duplicate", response_model=PresentationModel)
async def duplicate_presentation(id: str, user=Depends(get_current_user)):
    """
    Duplicate a presentation
    """
    if not Presentations.check_access_by_user_id(id, user.id, permission="read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    original = Presentations.get_presentation_by_id(id)
    if not original:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Presentation not found",
        )

    # Create a copy
    new_presentation = Presentations.create_presentation(
        user.id,
        PresentationForm(
            title=f"{original.title} (Copy)",
            description=original.description,
            slides=original.slides,
            theme=original.theme,
            theme_config=original.theme_config,
            is_template=False,
            organization_id=original.organization_id,
        ),
    )

    if not new_presentation:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to duplicate presentation",
        )
    return new_presentation


@router.post("/{id}/publish", response_model=PresentationModel)
async def publish_presentation(id: str, user=Depends(get_current_user)):
    """
    Publish a presentation
    """
    if not Presentations.check_access_by_user_id(id, user.id, permission="write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    presentation = Presentations.update_presentation_by_id(
        id, PresentationUpdateForm(is_published=True)
    )
    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish presentation",
        )
    return presentation


@router.post("/generate", response_model=PresentationModel)
async def generate_presentation(
    form_data: GeneratePresentationForm, user=Depends(get_current_user)
):
    """
    Generate a presentation using AI from a prompt
    """
    # Create initial slides structure
    initial_slides = [
        {
            "id": "slide-1",
            "type": "title",
            "title": "Generated Presentation",
            "subtitle": form_data.prompt[:100] + "..." if len(form_data.prompt) > 100 else form_data.prompt,
            "order": 0,
        }
    ]

    # Add placeholder slides
    for i in range(1, min(form_data.slide_count, 20)):
        initial_slides.append(
            {
                "id": f"slide-{i + 1}",
                "type": "content",
                "title": f"Slide {i + 1}",
                "content": "Content will be generated...",
                "order": i,
            }
        )

    presentation = Presentations.create_presentation(
        user.id,
        PresentationForm(
            title="AI Generated Presentation",
            description=f"Generated from: {form_data.prompt[:200]}",
            slides=initial_slides,
            theme=form_data.theme,
            source_prompt=form_data.prompt,
            source_document_id=form_data.source_document_id,
            organization_id=form_data.organization_id,
        ),
    )

    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate presentation",
        )

    # TODO: Integrate with AI to actually generate slide content
    # This would involve calling the LLM to generate content for each slide

    return presentation
