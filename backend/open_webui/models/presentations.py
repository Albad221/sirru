"""
Sirru Presentations Model
Presentation management for the Slides AI module
"""

import json
import logging
import time
from typing import Optional, List
import uuid

from open_webui.internal.db import Base, get_db
from open_webui.env import SRC_LOG_LEVELS
from open_webui.models.users import Users, UserResponse
from open_webui.models.groups import Groups
from open_webui.utils.access_control import has_access

from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Column, String, Text, JSON, Boolean, Integer, Index

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

####################
# Presentation DB Schema
####################


class Presentation(Base):
    __tablename__ = "sirru_presentations"

    id = Column(Text, unique=True, primary_key=True)
    user_id = Column(Text, nullable=False, index=True)
    organization_id = Column(Text, nullable=True, index=True)

    title = Column(Text, nullable=False, default="Untitled Presentation")
    description = Column(Text, nullable=True)

    # Slides data (JSON array of slide objects)
    slides = Column(JSON, nullable=False, default=[])
    slide_count = Column(Integer, default=0)

    # Theme and styling
    theme = Column(Text, default="default")
    theme_config = Column(JSON, nullable=True)  # Custom theme overrides

    # Source document (if generated from a document)
    source_document_id = Column(Text, nullable=True)
    source_prompt = Column(Text, nullable=True)

    # Status
    is_published = Column(Boolean, default=False)
    is_template = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)

    # Export settings
    export_settings = Column(JSON, nullable=True)

    # Access control
    access_control = Column(JSON, nullable=True)

    # Audit fields
    meta = Column(JSON, nullable=True)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)
    published_at = Column(BigInteger, nullable=True)

    __table_args__ = (
        Index("ix_sirru_presentations_user_updated", "user_id", "updated_at"),
        Index("ix_sirru_presentations_org_updated", "organization_id", "updated_at"),
    )


####################
# Slide Schema
####################


class SlideModel(BaseModel):
    """Individual slide structure"""

    id: str
    type: str = "title"  # title, content, two-column, image, quote, blank
    title: Optional[str] = None
    subtitle: Optional[str] = None
    content: Optional[str] = None  # Markdown content
    bullets: Optional[List[str]] = None
    image_url: Optional[str] = None
    image_caption: Optional[str] = None
    notes: Optional[str] = None  # Speaker notes
    layout: Optional[dict] = None  # Custom layout config
    order: int = 0


####################
# Pydantic Models
####################


class PresentationModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    organization_id: Optional[str] = None

    title: str
    description: Optional[str] = None

    slides: List[dict] = []
    slide_count: int = 0

    theme: str = "default"
    theme_config: Optional[dict] = None

    source_document_id: Optional[str] = None
    source_prompt: Optional[str] = None

    is_published: bool = False
    is_template: bool = False
    is_archived: bool = False

    export_settings: Optional[dict] = None
    access_control: Optional[dict] = None
    meta: Optional[dict] = None

    created_at: int
    updated_at: int
    published_at: Optional[int] = None


class PresentationUserModel(PresentationModel):
    user: Optional[UserResponse] = None


class PresentationResponse(PresentationModel):
    pass


####################
# Forms
####################


class PresentationForm(BaseModel):
    title: str = "Untitled Presentation"
    description: Optional[str] = None
    slides: List[dict] = []
    theme: str = "default"
    theme_config: Optional[dict] = None
    source_document_id: Optional[str] = None
    source_prompt: Optional[str] = None
    is_template: bool = False
    access_control: Optional[dict] = None
    organization_id: Optional[str] = None


class PresentationUpdateForm(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    slides: Optional[List[dict]] = None
    theme: Optional[str] = None
    theme_config: Optional[dict] = None
    is_published: Optional[bool] = None
    is_template: Optional[bool] = None
    is_archived: Optional[bool] = None
    export_settings: Optional[dict] = None
    access_control: Optional[dict] = None


class SlideUpdateForm(BaseModel):
    """Form for updating a single slide"""

    slide_id: str
    type: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    content: Optional[str] = None
    bullets: Optional[List[str]] = None
    image_url: Optional[str] = None
    image_caption: Optional[str] = None
    notes: Optional[str] = None
    layout: Optional[dict] = None
    order: Optional[int] = None


class GeneratePresentationForm(BaseModel):
    """Form for AI-generated presentations"""

    prompt: str
    slide_count: int = 10
    theme: str = "default"
    source_document_id: Optional[str] = None
    organization_id: Optional[str] = None


####################
# Presentation Table Operations
####################


class PresentationsTable:
    def create_presentation(
        self, user_id: str, form_data: PresentationForm
    ) -> Optional[PresentationModel]:
        """Create a new presentation"""
        with get_db() as db:
            presentation = PresentationModel(
                **{
                    **form_data.model_dump(),
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "slide_count": len(form_data.slides),
                    "created_at": int(time.time()),
                    "updated_at": int(time.time()),
                }
            )

            try:
                result = Presentation(**presentation.model_dump())
                db.add(result)
                db.commit()
                db.refresh(result)
                return PresentationModel.model_validate(result) if result else None
            except Exception as e:
                log.exception(e)
                return None

    def get_presentations(
        self,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        include_archived: bool = False,
    ) -> List[PresentationUserModel]:
        """Get all presentations, optionally filtered"""
        with get_db() as db:
            query = db.query(Presentation)

            if user_id:
                query = query.filter(Presentation.user_id == user_id)
            if organization_id:
                query = query.filter(Presentation.organization_id == organization_id)
            if not include_archived:
                query = query.filter(Presentation.is_archived == False)

            all_presentations = query.order_by(Presentation.updated_at.desc()).all()

            user_ids = list(set(p.user_id for p in all_presentations))
            users = Users.get_users_by_user_ids(user_ids) if user_ids else []
            users_dict = {user.id: user for user in users}

            presentations = []
            for pres in all_presentations:
                user = users_dict.get(pres.user_id)
                presentations.append(
                    PresentationUserModel.model_validate(
                        {
                            **PresentationModel.model_validate(pres).model_dump(),
                            "user": user.model_dump() if user else None,
                        }
                    )
                )
            return presentations

    def get_presentations_by_user_id(
        self, user_id: str, permission: str = "read"
    ) -> List[PresentationUserModel]:
        """Get presentations accessible by a specific user"""
        presentations = self.get_presentations()
        user_group_ids = {group.id for group in Groups.get_groups_by_member_id(user_id)}

        return [
            pres
            for pres in presentations
            if pres.user_id == user_id
            or has_access(user_id, permission, pres.access_control, user_group_ids)
        ]

    def get_presentation_by_id(self, id: str) -> Optional[PresentationModel]:
        """Get a single presentation by ID"""
        try:
            with get_db() as db:
                presentation = db.query(Presentation).filter_by(id=id).first()
                return (
                    PresentationModel.model_validate(presentation)
                    if presentation
                    else None
                )
        except Exception as e:
            log.exception(e)
            return None

    def check_access_by_user_id(
        self, id: str, user_id: str, permission: str = "read"
    ) -> bool:
        """Check if a user has access to a presentation"""
        presentation = self.get_presentation_by_id(id)
        if not presentation:
            return False
        if presentation.user_id == user_id:
            return True
        user_group_ids = {group.id for group in Groups.get_groups_by_member_id(user_id)}
        return has_access(
            user_id, permission, presentation.access_control, user_group_ids
        )

    def update_presentation_by_id(
        self, id: str, form_data: PresentationUpdateForm
    ) -> Optional[PresentationModel]:
        """Update a presentation"""
        try:
            with get_db() as db:
                update_data = {
                    k: v for k, v in form_data.model_dump().items() if v is not None
                }
                update_data["updated_at"] = int(time.time())

                # Update slide count if slides are updated
                if form_data.slides is not None:
                    update_data["slide_count"] = len(form_data.slides)

                # Handle publishing
                if form_data.is_published:
                    existing = self.get_presentation_by_id(id)
                    if existing and not existing.is_published:
                        update_data["published_at"] = int(time.time())

                db.query(Presentation).filter_by(id=id).update(update_data)
                db.commit()
                return self.get_presentation_by_id(id)
        except Exception as e:
            log.exception(e)
            return None

    def update_slides(
        self, id: str, slides: List[dict]
    ) -> Optional[PresentationModel]:
        """Update only slides (for quick save)"""
        try:
            with get_db() as db:
                db.query(Presentation).filter_by(id=id).update(
                    {
                        "slides": slides,
                        "slide_count": len(slides),
                        "updated_at": int(time.time()),
                    }
                )
                db.commit()
                return self.get_presentation_by_id(id)
        except Exception as e:
            log.exception(e)
            return None

    def delete_presentation_by_id(self, id: str) -> bool:
        """Delete a presentation"""
        try:
            with get_db() as db:
                db.query(Presentation).filter_by(id=id).delete()
                db.commit()
                return True
        except Exception as e:
            log.exception(e)
            return False

    def archive_presentation_by_id(self, id: str) -> Optional[PresentationModel]:
        """Archive a presentation"""
        return self.update_presentation_by_id(
            id, PresentationUpdateForm(is_archived=True)
        )

    def get_templates(
        self, organization_id: Optional[str] = None
    ) -> List[PresentationModel]:
        """Get all presentation templates"""
        with get_db() as db:
            query = db.query(Presentation).filter(Presentation.is_template == True)
            if organization_id:
                query = query.filter(Presentation.organization_id == organization_id)
            templates = query.order_by(Presentation.title).all()
            return [PresentationModel.model_validate(t) for t in templates]

    def get_available_themes(self) -> List[dict]:
        """Get available presentation themes"""
        return [
            {
                "id": "default",
                "name": "Default",
                "description": "Clean, professional theme",
                "colors": {
                    "primary": "#166534",
                    "secondary": "#eab308",
                    "background": "#ffffff",
                    "text": "#1e293b",
                },
            },
            {
                "id": "dark",
                "name": "Dark",
                "description": "Modern dark theme",
                "colors": {
                    "primary": "#22c55e",
                    "secondary": "#fde047",
                    "background": "#0f172a",
                    "text": "#f8fafc",
                },
            },
            {
                "id": "corporate",
                "name": "Corporate",
                "description": "Professional business theme",
                "colors": {
                    "primary": "#1e40af",
                    "secondary": "#dc2626",
                    "background": "#ffffff",
                    "text": "#1e293b",
                },
            },
            {
                "id": "creative",
                "name": "Creative",
                "description": "Bold and colorful",
                "colors": {
                    "primary": "#7c3aed",
                    "secondary": "#f97316",
                    "background": "#faf5ff",
                    "text": "#1e293b",
                },
            },
            {
                "id": "minimal",
                "name": "Minimal",
                "description": "Simple and clean",
                "colors": {
                    "primary": "#000000",
                    "secondary": "#6b7280",
                    "background": "#ffffff",
                    "text": "#111827",
                },
            },
        ]


# Singleton instance
Presentations = PresentationsTable()
