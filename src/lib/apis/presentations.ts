/**
 * Sirru Presentations API Client
 * API client for the Slides AI module
 */

import { WEBUI_API_BASE_URL } from '$lib/constants';

export interface Slide {
	id: string;
	type: 'title' | 'content' | 'two-column' | 'image' | 'quote' | 'blank';
	title?: string;
	subtitle?: string;
	content?: string;
	bullets?: string[];
	image_url?: string;
	image_caption?: string;
	notes?: string;
	layout?: Record<string, unknown>;
	order: number;
}

export interface Presentation {
	id: string;
	user_id: string;
	organization_id?: string;
	title: string;
	description?: string;
	slides: Slide[];
	slide_count: number;
	theme: string;
	theme_config?: Record<string, unknown>;
	source_document_id?: string;
	source_prompt?: string;
	is_published: boolean;
	is_template: boolean;
	is_archived: boolean;
	export_settings?: Record<string, unknown>;
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
}

export interface Theme {
	id: string;
	name: string;
	description: string;
	colors: {
		primary: string;
		secondary: string;
		background: string;
		text: string;
	};
}

export interface PresentationForm {
	title?: string;
	description?: string;
	slides?: Slide[];
	theme?: string;
	theme_config?: Record<string, unknown>;
	source_document_id?: string;
	source_prompt?: string;
	is_template?: boolean;
	access_control?: Record<string, unknown>;
	organization_id?: string;
}

export interface PresentationUpdateForm {
	title?: string;
	description?: string;
	slides?: Slide[];
	theme?: string;
	theme_config?: Record<string, unknown>;
	is_published?: boolean;
	is_template?: boolean;
	is_archived?: boolean;
	export_settings?: Record<string, unknown>;
	access_control?: Record<string, unknown>;
}

export interface GeneratePresentationForm {
	prompt: string;
	slide_count?: number;
	theme?: string;
	source_document_id?: string;
	organization_id?: string;
}

/**
 * Get all presentations accessible by the current user
 */
export const getPresentations = async (
	token: string,
	includeArchived = false
): Promise<Presentation[]> => {
	const res = await fetch(
		`${WEBUI_API_BASE_URL}/presentations?include_archived=${includeArchived}`,
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
		throw new Error(error.detail || 'Failed to fetch presentations');
	}

	return res.json();
};

/**
 * Create a new presentation
 */
export const createPresentation = async (
	token: string,
	formData: PresentationForm
): Promise<Presentation> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/presentations`, {
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
		throw new Error(error.detail || 'Failed to create presentation');
	}

	return res.json();
};

/**
 * Get a presentation by ID
 */
export const getPresentationById = async (
	token: string,
	id: string
): Promise<Presentation> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/presentations/${id}`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to fetch presentation');
	}

	return res.json();
};

/**
 * Update a presentation
 */
export const updatePresentation = async (
	token: string,
	id: string,
	formData: PresentationUpdateForm
): Promise<Presentation> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/presentations/${id}`, {
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
		throw new Error(error.detail || 'Failed to update presentation');
	}

	return res.json();
};

/**
 * Update presentation slides
 */
export const updateSlides = async (
	token: string,
	id: string,
	slides: Slide[]
): Promise<Presentation> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/presentations/${id}/slides`, {
		method: 'PUT',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ slides })
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to update slides');
	}

	return res.json();
};

/**
 * Delete a presentation
 */
export const deletePresentation = async (token: string, id: string): Promise<boolean> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/presentations/${id}`, {
		method: 'DELETE',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to delete presentation');
	}

	return true;
};

/**
 * Archive a presentation
 */
export const archivePresentation = async (
	token: string,
	id: string
): Promise<Presentation> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/presentations/${id}/archive`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to archive presentation');
	}

	return res.json();
};

/**
 * Duplicate a presentation
 */
export const duplicatePresentation = async (
	token: string,
	id: string
): Promise<Presentation> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/presentations/${id}/duplicate`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to duplicate presentation');
	}

	return res.json();
};

/**
 * Publish a presentation
 */
export const publishPresentation = async (
	token: string,
	id: string
): Promise<Presentation> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/presentations/${id}/publish`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to publish presentation');
	}

	return res.json();
};

/**
 * Get available themes
 */
export const getThemes = async (token: string): Promise<Theme[]> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/presentations/themes`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		const error = await res.json();
		throw new Error(error.detail || 'Failed to fetch themes');
	}

	return res.json();
};

/**
 * Get presentation templates
 */
export const getTemplates = async (
	token: string,
	organizationId?: string
): Promise<Presentation[]> => {
	const url = organizationId
		? `${WEBUI_API_BASE_URL}/presentations/templates?organization_id=${organizationId}`
		: `${WEBUI_API_BASE_URL}/presentations/templates`;

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
 * Generate a presentation using AI
 */
export const generatePresentation = async (
	token: string,
	formData: GeneratePresentationForm
): Promise<Presentation> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/presentations/generate`, {
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
		throw new Error(error.detail || 'Failed to generate presentation');
	}

	return res.json();
};

/**
 * Create a new blank slide
 */
export function createBlankSlide(order: number, type: Slide['type'] = 'content'): Slide {
	return {
		id: `slide-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
		type,
		title: '',
		content: '',
		order
	};
}

/**
 * Default title slide
 */
export function createTitleSlide(title = 'Untitled Presentation', subtitle = ''): Slide {
	return {
		id: 'slide-title',
		type: 'title',
		title,
		subtitle,
		order: 0
	};
}
