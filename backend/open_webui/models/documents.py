"""
Sirru Documents Model
Document management for the Docs AI module
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
from sqlalchemy import BigInteger, Column, String, Text, JSON, Boolean, Index

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

####################
# Document DB Schema
####################


class Document(Base):
    __tablename__ = "sirru_documents"

    id = Column(Text, unique=True, primary_key=True)
    user_id = Column(Text, nullable=False, index=True)
    organization_id = Column(Text, nullable=True, index=True)  # Multi-tenant support

    title = Column(Text, nullable=False, default="Untitled Document")
    content = Column(Text, nullable=True)  # Markdown/HTML content
    content_json = Column(JSON, nullable=True)  # TipTap JSON content

    # Document metadata
    document_type = Column(Text, default="document")  # document, template, report
    tags = Column(JSON, nullable=True)  # List of tags
    folder_id = Column(Text, nullable=True, index=True)

    # Status
    is_published = Column(Boolean, default=False)
    is_template = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)

    # RAG integration
    knowledge_base_id = Column(Text, nullable=True)  # Link to knowledge base for RAG
    embedding_status = Column(Text, default="pending")  # pending, processing, completed, failed

    # Access control
    access_control = Column(JSON, nullable=True)

    # Audit fields
    meta = Column(JSON, nullable=True)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)
    published_at = Column(BigInteger, nullable=True)

    __table_args__ = (
        Index("ix_sirru_documents_user_updated", "user_id", "updated_at"),
        Index("ix_sirru_documents_org_updated", "organization_id", "updated_at"),
    )


####################
# Pydantic Models
####################


class DocumentModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    organization_id: Optional[str] = None

    title: str
    content: Optional[str] = None
    content_json: Optional[dict] = None

    document_type: str = "document"
    tags: Optional[List[str]] = None
    folder_id: Optional[str] = None

    is_published: bool = False
    is_template: bool = False
    is_archived: bool = False

    knowledge_base_id: Optional[str] = None
    embedding_status: str = "pending"

    access_control: Optional[dict] = None
    meta: Optional[dict] = None

    created_at: int
    updated_at: int
    published_at: Optional[int] = None


class DocumentUserModel(DocumentModel):
    user: Optional[UserResponse] = None


class DocumentResponse(DocumentModel):
    word_count: Optional[int] = None
    character_count: Optional[int] = None


class DocumentUserResponse(DocumentUserModel):
    word_count: Optional[int] = None
    character_count: Optional[int] = None


####################
# Forms
####################


class DocumentForm(BaseModel):
    title: str = "Untitled Document"
    content: Optional[str] = None
    content_json: Optional[dict] = None
    document_type: str = "document"
    tags: Optional[List[str]] = None
    folder_id: Optional[str] = None
    is_template: bool = False
    knowledge_base_id: Optional[str] = None
    access_control: Optional[dict] = None
    organization_id: Optional[str] = None


class DocumentUpdateForm(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    content_json: Optional[dict] = None
    tags: Optional[List[str]] = None
    folder_id: Optional[str] = None
    is_published: Optional[bool] = None
    is_template: Optional[bool] = None
    is_archived: Optional[bool] = None
    knowledge_base_id: Optional[str] = None
    access_control: Optional[dict] = None


####################
# Document Table Operations
####################


class DocumentsTable:
    def create_document(
        self, user_id: str, form_data: DocumentForm
    ) -> Optional[DocumentModel]:
        """Create a new document"""
        with get_db() as db:
            document = DocumentModel(
                **{
                    **form_data.model_dump(),
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "created_at": int(time.time()),
                    "updated_at": int(time.time()),
                }
            )

            try:
                result = Document(**document.model_dump())
                db.add(result)
                db.commit()
                db.refresh(result)
                return DocumentModel.model_validate(result) if result else None
            except Exception as e:
                log.exception(e)
                return None

    def get_documents(
        self,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        include_archived: bool = False,
    ) -> List[DocumentUserModel]:
        """Get all documents, optionally filtered by user or organization"""
        with get_db() as db:
            query = db.query(Document)

            if user_id:
                query = query.filter(Document.user_id == user_id)
            if organization_id:
                query = query.filter(Document.organization_id == organization_id)
            if not include_archived:
                query = query.filter(Document.is_archived == False)

            all_documents = query.order_by(Document.updated_at.desc()).all()

            user_ids = list(set(doc.user_id for doc in all_documents))
            users = Users.get_users_by_user_ids(user_ids) if user_ids else []
            users_dict = {user.id: user for user in users}

            documents = []
            for doc in all_documents:
                user = users_dict.get(doc.user_id)
                documents.append(
                    DocumentUserModel.model_validate(
                        {
                            **DocumentModel.model_validate(doc).model_dump(),
                            "user": user.model_dump() if user else None,
                        }
                    )
                )
            return documents

    def get_documents_by_user_id(
        self, user_id: str, permission: str = "read"
    ) -> List[DocumentUserModel]:
        """Get documents accessible by a specific user"""
        documents = self.get_documents()
        user_group_ids = {group.id for group in Groups.get_groups_by_member_id(user_id)}

        return [
            doc
            for doc in documents
            if doc.user_id == user_id
            or has_access(user_id, permission, doc.access_control, user_group_ids)
        ]

    def get_document_by_id(self, id: str) -> Optional[DocumentModel]:
        """Get a single document by ID"""
        try:
            with get_db() as db:
                document = db.query(Document).filter_by(id=id).first()
                return DocumentModel.model_validate(document) if document else None
        except Exception as e:
            log.exception(e)
            return None

    def check_access_by_user_id(
        self, id: str, user_id: str, permission: str = "read"
    ) -> bool:
        """Check if a user has access to a document"""
        document = self.get_document_by_id(id)
        if not document:
            return False
        if document.user_id == user_id:
            return True
        user_group_ids = {group.id for group in Groups.get_groups_by_member_id(user_id)}
        return has_access(user_id, permission, document.access_control, user_group_ids)

    def update_document_by_id(
        self, id: str, form_data: DocumentUpdateForm
    ) -> Optional[DocumentModel]:
        """Update a document"""
        try:
            with get_db() as db:
                update_data = {
                    k: v for k, v in form_data.model_dump().items() if v is not None
                }
                update_data["updated_at"] = int(time.time())

                # Handle publishing
                if form_data.is_published and not self.get_document_by_id(id).is_published:
                    update_data["published_at"] = int(time.time())

                db.query(Document).filter_by(id=id).update(update_data)
                db.commit()
                return self.get_document_by_id(id)
        except Exception as e:
            log.exception(e)
            return None

    def update_document_content(
        self, id: str, content: str, content_json: Optional[dict] = None
    ) -> Optional[DocumentModel]:
        """Update only document content (for auto-save)"""
        try:
            with get_db() as db:
                update_data = {
                    "content": content,
                    "updated_at": int(time.time()),
                }
                if content_json is not None:
                    update_data["content_json"] = content_json

                db.query(Document).filter_by(id=id).update(update_data)
                db.commit()
                return self.get_document_by_id(id)
        except Exception as e:
            log.exception(e)
            return None

    def delete_document_by_id(self, id: str) -> bool:
        """Delete a document"""
        try:
            with get_db() as db:
                db.query(Document).filter_by(id=id).delete()
                db.commit()
                return True
        except Exception as e:
            log.exception(e)
            return False

    def archive_document_by_id(self, id: str) -> Optional[DocumentModel]:
        """Archive a document instead of deleting"""
        return self.update_document_by_id(id, DocumentUpdateForm(is_archived=True))

    def get_templates(
        self, organization_id: Optional[str] = None
    ) -> List[DocumentModel]:
        """Get all document templates"""
        with get_db() as db:
            query = db.query(Document).filter(Document.is_template == True)
            if organization_id:
                query = query.filter(Document.organization_id == organization_id)
            templates = query.order_by(Document.title).all()
            return [DocumentModel.model_validate(t) for t in templates]

    def search_documents(
        self, query: str, user_id: str, limit: int = 20
    ) -> List[DocumentModel]:
        """Search documents by title or content"""
        with get_db() as db:
            search_pattern = f"%{query}%"
            documents = (
                db.query(Document)
                .filter(
                    Document.user_id == user_id,
                    Document.is_archived == False,
                    (
                        Document.title.ilike(search_pattern)
                        | Document.content.ilike(search_pattern)
                    ),
                )
                .order_by(Document.updated_at.desc())
                .limit(limit)
                .all()
            )
            return [DocumentModel.model_validate(d) for d in documents]


# Singleton instance
Documents = DocumentsTable()
