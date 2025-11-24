<script lang="ts">
	import { onMount, onDestroy, getContext } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { toast } from 'svelte-sonner';
	import { fade } from 'svelte/transition';

	import { user, models } from '$lib/stores';
	import {
		getDocumentById,
		updateDocument,
		updateDocumentContent,
		deleteDocument,
		duplicateDocument,
		publishDocument,
		type Document,
		type DocumentUpdateForm
	} from '$lib/apis/documents';

	import RichTextInput from '$lib/components/common/RichTextInput.svelte';
	import SirruGlobalSearch from '$lib/components/sirru/SirruGlobalSearch.svelte';

	const i18n = getContext('i18n');

	let document: Document | null = null;
	let loading = true;
	let saving = false;
	let lastSaved: Date | null = null;

	let title = '';
	let content = '';
	let contentJson: Record<string, unknown> | null = null;

	let editor: any = null;
	let autoSaveTimer: ReturnType<typeof setTimeout> | null = null;
	let hasUnsavedChanges = false;

	// AI Assistant state
	let showAIPanel = false;
	let aiPrompt = '';
	let aiLoading = false;

	$: documentId = $page.params.id;

	async function loadDocument() {
		if (!documentId || documentId === 'new') {
			document = null;
			title = 'Untitled Document';
			content = '';
			loading = false;
			return;
		}

		try {
			loading = true;
			document = await getDocumentById(localStorage.token, documentId);
			title = document.title;
			content = document.content || '';
			contentJson = document.content_json || null;
		} catch (error) {
			toast.error('Failed to load document');
			console.error(error);
			goto('/docs');
		} finally {
			loading = false;
		}
	}

	async function handleSave() {
		if (!document && documentId !== 'new') return;

		try {
			saving = true;

			if (documentId === 'new') {
				// Create new document
				const { createDocument } = await import('$lib/apis/documents');
				const newDoc = await createDocument(localStorage.token, {
					title,
					content,
					content_json: contentJson || undefined
				});
				document = newDoc;
				goto(`/docs/${newDoc.id}`, { replaceState: true });
			} else {
				// Update existing document
				await updateDocumentContent(localStorage.token, documentId, content, contentJson || undefined);
				await updateDocument(localStorage.token, documentId, { title });
			}

			lastSaved = new Date();
			hasUnsavedChanges = false;
			toast.success('Document saved');
		} catch (error) {
			toast.error('Failed to save document');
			console.error(error);
		} finally {
			saving = false;
		}
	}

	function scheduleAutoSave() {
		if (autoSaveTimer) {
			clearTimeout(autoSaveTimer);
		}
		hasUnsavedChanges = true;
		autoSaveTimer = setTimeout(handleSave, 3000); // Auto-save after 3 seconds of inactivity
	}

	function handleContentChange(e: { html: string; json: unknown; md: string }) {
		content = e.md;
		contentJson = e.json as Record<string, unknown>;
		scheduleAutoSave();
	}

	function handleTitleChange() {
		scheduleAutoSave();
	}

	async function handleDelete() {
		if (!document) return;
		if (!confirm('Are you sure you want to delete this document?')) return;

		try {
			await deleteDocument(localStorage.token, document.id);
			toast.success('Document deleted');
			goto('/docs');
		} catch (error) {
			toast.error('Failed to delete document');
			console.error(error);
		}
	}

	async function handleDuplicate() {
		if (!document) return;

		try {
			const newDoc = await duplicateDocument(localStorage.token, document.id);
			toast.success('Document duplicated');
			goto(`/docs/${newDoc.id}`);
		} catch (error) {
			toast.error('Failed to duplicate document');
			console.error(error);
		}
	}

	async function handlePublish() {
		if (!document) return;

		try {
			await publishDocument(localStorage.token, document.id);
			document.is_published = true;
			toast.success('Document published');
		} catch (error) {
			toast.error('Failed to publish document');
			console.error(error);
		}
	}

	async function handleAIAssist() {
		if (!aiPrompt.trim()) return;

		try {
			aiLoading = true;
			// TODO: Integrate with AI chat completion API
			toast.info('AI assistance coming soon!');
		} catch (error) {
			toast.error('AI request failed');
			console.error(error);
		} finally {
			aiLoading = false;
		}
	}

	function formatLastSaved(): string {
		if (!lastSaved) return '';
		const now = new Date();
		const diff = now.getTime() - lastSaved.getTime();
		const seconds = Math.floor(diff / 1000);
		const minutes = Math.floor(diff / 60000);

		if (seconds < 60) return 'Saved just now';
		if (minutes < 60) return `Saved ${minutes}m ago`;
		return `Saved at ${lastSaved.toLocaleTimeString()}`;
	}

	// Keyboard shortcuts
	function handleKeydown(e: KeyboardEvent) {
		// Ctrl/Cmd + S to save
		if ((e.ctrlKey || e.metaKey) && e.key === 's') {
			e.preventDefault();
			handleSave();
		}
	}

	onMount(() => {
		if (!$user) {
			goto('/auth');
			return;
		}
		loadDocument();
		window.addEventListener('keydown', handleKeydown);
	});

	onDestroy(() => {
		if (autoSaveTimer) {
			clearTimeout(autoSaveTimer);
		}
		window.removeEventListener('keydown', handleKeydown);
	});
</script>

<svelte:head>
	<title>{title || 'New Document'} - Docs AI - Sirru</title>
</svelte:head>

<div class="h-screen flex flex-col bg-white dark:bg-gray-950">
	<!-- Header -->
	<header class="sirru-header flex-shrink-0">
		<div class="max-w-full px-4">
			<div class="flex items-center justify-between h-14">
				<!-- Left: Back & Title -->
				<div class="flex items-center gap-3 flex-1 min-w-0">
					<a
						href="/docs"
						class="p-2 rounded-lg text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
					>
						<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
						</svg>
					</a>

					<div class="flex items-center gap-2 flex-1 min-w-0">
						<div class="w-6 h-6 rounded bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center flex-shrink-0">
							<svg class="w-3 h-3 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
							</svg>
						</div>
						<input
							bind:value={title}
							on:input={handleTitleChange}
							placeholder="Untitled Document"
							class="flex-1 min-w-0 bg-transparent border-0 text-lg font-medium text-gray-900 dark:text-white placeholder:text-gray-400 focus:outline-none focus:ring-0"
						/>
					</div>
				</div>

				<!-- Center: Save Status -->
				<div class="hidden sm:flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
					{#if saving}
						<div class="flex items-center gap-2">
							<div class="animate-spin rounded-full h-4 w-4 border-2 border-blue-600 border-t-transparent"></div>
							<span>Saving...</span>
						</div>
					{:else if hasUnsavedChanges}
						<span class="text-amber-600 dark:text-amber-400">Unsaved changes</span>
					{:else if lastSaved}
						<span>{formatLastSaved()}</span>
					{/if}
				</div>

				<!-- Right: Actions -->
				<div class="flex items-center gap-2">
					<!-- AI Assist Toggle -->
					<button
						on:click={() => (showAIPanel = !showAIPanel)}
						class="p-2 rounded-lg transition-colors {showAIPanel ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800'}"
						title="AI Assistant"
					>
						<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
						</svg>
					</button>

					<!-- More Actions Dropdown -->
					<div class="relative group">
						<button
							class="p-2 rounded-lg text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
						>
							<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
							</svg>
						</button>

						<div class="absolute right-0 top-full mt-1 w-48 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 py-1 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
							<button
								on:click={handleDuplicate}
								class="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2"
							>
								<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
								</svg>
								Duplicate
							</button>
							{#if document && !document.is_published}
								<button
									on:click={handlePublish}
									class="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2"
								>
									<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
										<path stroke-linecap="round" stroke-linejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
									</svg>
									Publish
								</button>
							{/if}
							<hr class="my-1 border-gray-200 dark:border-gray-700" />
							<button
								on:click={handleDelete}
								class="w-full px-4 py-2 text-left text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 flex items-center gap-2"
							>
								<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
								</svg>
								Delete
							</button>
						</div>
					</div>

					<!-- Save Button -->
					<button
						on:click={handleSave}
						disabled={saving}
						class="sirru-btn sirru-btn-primary sirru-btn-sm"
					>
						{#if saving}
							<div class="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
						{:else}
							Save
						{/if}
					</button>
				</div>
			</div>
		</div>
	</header>

	<!-- Main Content -->
	<div class="flex-1 flex overflow-hidden">
		<!-- Editor -->
		<main class="flex-1 overflow-y-auto">
			{#if loading}
				<div class="flex items-center justify-center h-full">
					<div class="animate-spin rounded-full h-8 w-8 border-2 border-blue-600 border-t-transparent"></div>
				</div>
			{:else}
				<div class="max-w-4xl mx-auto px-8 py-12">
					<RichTextInput
						bind:editor
						bind:value={content}
						className="input-prose min-h-[60vh] text-lg"
						placeholder="Start writing your document..."
						richText={true}
						dragHandle={true}
						image={true}
						fileHandler={true}
						showFormattingToolbar={true}
						onChange={handleContentChange}
					/>
				</div>
			{/if}
		</main>

		<!-- AI Assistant Panel -->
		{#if showAIPanel}
			<aside
				class="w-80 border-l border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900 flex flex-col"
				transition:fade={{ duration: 150 }}
			>
				<div class="p-4 border-b border-gray-200 dark:border-gray-800">
					<div class="flex items-center justify-between">
						<h3 class="font-semibold text-gray-900 dark:text-white">AI Assistant</h3>
						<button
							on:click={() => (showAIPanel = false)}
							class="p-1 rounded-lg text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
						>
							<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
							</svg>
						</button>
					</div>
				</div>

				<div class="flex-1 p-4 overflow-y-auto">
					<div class="space-y-3">
						<p class="text-sm text-gray-600 dark:text-gray-400">
							Ask the AI to help you write, edit, or improve your document.
						</p>

						<!-- Quick Actions -->
						<div class="space-y-2">
							<p class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Quick Actions</p>
							<div class="grid grid-cols-2 gap-2">
								<button class="p-2 text-xs text-left rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600 transition-colors">
									Improve writing
								</button>
								<button class="p-2 text-xs text-left rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600 transition-colors">
									Make shorter
								</button>
								<button class="p-2 text-xs text-left rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600 transition-colors">
									Make longer
								</button>
								<button class="p-2 text-xs text-left rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600 transition-colors">
									Fix grammar
								</button>
								<button class="p-2 text-xs text-left rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600 transition-colors">
									Summarize
								</button>
								<button class="p-2 text-xs text-left rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600 transition-colors">
									Translate
								</button>
							</div>
						</div>
					</div>
				</div>

				<!-- Input -->
				<div class="p-4 border-t border-gray-200 dark:border-gray-800">
					<div class="flex gap-2">
						<input
							bind:value={aiPrompt}
							placeholder="Ask AI..."
							class="sirru-input flex-1 text-sm"
							on:keydown={(e) => e.key === 'Enter' && handleAIAssist()}
						/>
						<button
							on:click={handleAIAssist}
							disabled={aiLoading || !aiPrompt.trim()}
							class="sirru-btn sirru-btn-primary sirru-btn-sm"
						>
							{#if aiLoading}
								<div class="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
							{:else}
								<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
								</svg>
							{/if}
						</button>
					</div>
				</div>
			</aside>
		{/if}
	</div>
</div>

<SirruGlobalSearch />
