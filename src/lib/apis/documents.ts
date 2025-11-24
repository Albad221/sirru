/**
 * Sirru Documents API Client
 * API client for the Docs AI module
 */

import { WEBUI_API_BASE_URL } from '$lib/constants';

export interface Document {
	id: string;
	user_id: string;
	organization_id?: string;
	title: string;
	content?: string;
	content_json?: Record<string, unknown>;
	document_type: string;
	tags?: string[];
	folder_id?: string;
	is_published: boolean;
	is_template: boolean;
	is_archived: boolean;
	knowledge_base_id?: string;
	embedding_status: string;
	access_control?: Record<string, unknown>;
	meta?: Record<string, unknown>;
	created_at: number;
	updated_at: number;
	published_at?: number;
	user?: {
		id: string;
		name: string;
		email: string;
		profile_image_url: string;
	};
	word_count?: number;
	character_count?: number;
}

export interface DocumentForm {
	title?: string;
	content?: string;
	content_json?: Record<string, unknown>;
	document_type?: string;
	tags?: string[];
	folder_id?: string;
	is_template?: boolean;
	knowledge_base_id?: string;
	access_control?: Record<string, unknown>;
	organization_id?: string;
}

export interface DocumentUpdateForm {
	title?: string;
	content?: string;
	content_json?: Record<string, unknown>;
	tags?: string[];
	folder_id?: string;
	is_published?: boolean;
	is_template?: boolean;
	is_archived?: boolean;
	knowledge_base_id?: string;
	access_control?: Record<string, unknown>;
}

/**
 * Get all documents accessible by the current user
 */
export const getDocuments = async (
	token: string,
	includeArchived = false
): Promise<Document[]> => {
	const res = await fetch(
		`${WEBUI_API_BASE_URL}/documents?include_archived=${includeArchived}`,
		{
			method: 'GET',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
				authorization: `Bearer ${token}`
			}
		}
	);

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to fetch documents');
	}

	return res.json();
};

/**
 * Create a new document
 */
export const createDocument = async (
	token: string,
	formData: DocumentForm
): Promise<Document> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/documents`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify(formData)
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to create document');
	}

	return res.json();
};

/**
 * Get a document by ID
 */
export const getDocumentById = async (token: string, id: string): Promise<Document> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/documents/${id}`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to fetch document');
	}

	return res.json();
};

/**
 * Update a document
 */
export const updateDocument = async (
	token: string,
	id: string,
	formData: DocumentUpdateForm
): Promise<Document> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/documents/${id}`, {
		method: 'PUT',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify(formData)
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to update document');
	}

	return res.json();
};

/**
 * Update document content (for auto-save)
 */
export const updateDocumentContent = async (
	token: string,
	id: string,
	content: string,
	contentJson?: Record<string, unknown>
): Promise<Document> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/documents/${id}/content`, {
		method: 'PUT',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ content, content_json: contentJson })
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to update document content');
	}

	return res.json();
};

/**
 * Delete a document
 */
export const deleteDocument = async (token: string, id: string): Promise<boolean> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/documents/${id}`, {
		method: 'DELETE',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to delete document');
	}

	return true;
};

/**
 * Archive a document
 */
export const archiveDocument = async (token: string, id: string): Promise<Document> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/documents/${id}/archive`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to archive document');
	}

	return res.json();
};

/**
 * Duplicate a document
 */
export const duplicateDocument = async (token: string, id: string): Promise<Document> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/documents/${id}/duplicate`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to duplicate document');
	}

	return res.json();
};

/**
 * Publish a document
 */
export const publishDocument = async (token: string, id: string): Promise<Document> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/documents/${id}/publish`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to publish document');
	}

	return res.json();
};

/**
 * Get document templates
 */
export const getTemplates = async (
	token: string,
	organizationId?: string
): Promise<Document[]> => {
	const url = organizationId
		? `${WEBUI_API_BASE_URL}/documents/templates?organization_id=${organizationId}`
		: `${WEBUI_API_BASE_URL}/documents/templates`;

	const res = await fetch(url, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to fetch templates');
	}

	return res.json();
};

/**
 * Search documents
 */
export const searchDocuments = async (
	token: string,
	query: string,
	limit = 20
): Promise<Document[]> => {
	const res = await fetch(
		`${WEBUI_API_BASE_URL}/documents/search?q=${encodeURIComponent(query)}&limit=${limit}`,
		{
			method: 'GET',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
				authorization: `Bearer ${token}`
			}
		}
	);

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to search documents');
	}

	return res.json();
};
