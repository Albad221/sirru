<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { goto } from '$app/navigation';
	import { toast } from 'svelte-sonner';
	import { fade } from 'svelte/transition';

	import { user } from '$lib/stores';
	import {
		getDocuments,
		createDocument,
		deleteDocument,
		archiveDocument,
		type Document
	} from '$lib/apis/documents';

	import SirruLogo from '$lib/components/sirru/SirruLogo.svelte';
	import SirruGlobalSearch from '$lib/components/sirru/SirruGlobalSearch.svelte';

	const i18n = getContext('i18n');

	let documents: Document[] = [];
	let loading = true;
	let searchQuery = '';
	let viewMode: 'grid' | 'list' = 'grid';
	let showArchived = false;

	$: filteredDocuments = documents.filter(
		(doc) =>
			doc.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
			doc.tags?.some((tag) => tag.toLowerCase().includes(searchQuery.toLowerCase()))
	);

	async function loadDocuments() {
		try {
			loading = true;
			documents = await getDocuments(localStorage.token, showArchived);
		} catch (error) {
			toast.error('Failed to load documents');
			console.error(error);
		} finally {
			loading = false;
		}
	}

	async function handleCreateDocument() {
		try {
			const doc = await createDocument(localStorage.token, {
				title: 'Untitled Document'
			});
			goto(`/docs/${doc.id}`);
		} catch (error) {
			toast.error('Failed to create document');
			console.error(error);
		}
	}

	async function handleDeleteDocument(id: string) {
		if (!confirm('Are you sure you want to delete this document?')) return;

		try {
			await deleteDocument(localStorage.token, id);
			documents = documents.filter((d) => d.id !== id);
			toast.success('Document deleted');
		} catch (error) {
			toast.error('Failed to delete document');
			console.error(error);
		}
	}

	async function handleArchiveDocument(id: string) {
		try {
			await archiveDocument(localStorage.token, id);
			documents = documents.filter((d) => d.id !== id);
			toast.success('Document archived');
		} catch (error) {
			toast.error('Failed to archive document');
			console.error(error);
		}
	}

	function formatDate(timestamp: number): string {
		return new Date(timestamp * 1000).toLocaleDateString('en-US', {
			month: 'short',
			day: 'numeric',
			year: 'numeric'
		});
	}

	function formatRelativeTime(timestamp: number): string {
		const now = Date.now();
		const diff = now - timestamp * 1000;
		const minutes = Math.floor(diff / 60000);
		const hours = Math.floor(diff / 3600000);
		const days = Math.floor(diff / 86400000);

		if (minutes < 1) return 'Just now';
		if (minutes < 60) return `${minutes}m ago`;
		if (hours < 24) return `${hours}h ago`;
		if (days < 7) return `${days}d ago`;
		return formatDate(timestamp);
	}

	onMount(() => {
		if (!$user) {
			goto('/auth');
			return;
		}
		loadDocuments();
	});
</script>

<svelte:head>
	<title>Docs AI - Sirru</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 dark:bg-gray-950">
	<!-- Header -->
	<header class="sirru-header">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex items-center justify-between h-16">
				<!-- Left: Back to Home & Title -->
				<div class="flex items-center gap-4">
					<a href="/home" class="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
						<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
						</svg>
					</a>
					<div class="flex items-center gap-3">
						<div class="w-8 h-8 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
							<svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
							</svg>
						</div>
						<h1 class="text-xl font-semibold text-gray-900 dark:text-white">Docs AI</h1>
					</div>
				</div>

				<!-- Right: Actions -->
				<div class="flex items-center gap-3">
					<button
						on:click={handleCreateDocument}
						class="sirru-btn sirru-btn-primary sirru-btn-md"
					>
						<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
						</svg>
						New Document
					</button>
				</div>
			</div>
		</div>
	</header>

	<!-- Main Content -->
	<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
		<!-- Search & Filters -->
		<div class="flex flex-col sm:flex-row gap-4 mb-8">
			<!-- Search -->
			<div class="flex-1 sirru-search">
				<svg class="sirru-search-icon w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
					<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
				</svg>
				<input
					type="text"
					bind:value={searchQuery}
					placeholder="Search documents..."
					class="sirru-search-input"
				/>
			</div>

			<!-- View Toggle -->
			<div class="flex items-center gap-2 bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
				<button
					on:click={() => (viewMode = 'grid')}
					class="p-2 rounded-md transition-colors {viewMode === 'grid' ? 'bg-white dark:bg-gray-700 shadow-sm' : 'hover:bg-gray-200 dark:hover:bg-gray-700'}"
					title="Grid view"
				>
					<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
					</svg>
				</button>
				<button
					on:click={() => (viewMode = 'list')}
					class="p-2 rounded-md transition-colors {viewMode === 'list' ? 'bg-white dark:bg-gray-700 shadow-sm' : 'hover:bg-gray-200 dark:hover:bg-gray-700'}"
					title="List view"
				>
					<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
					</svg>
				</button>
			</div>

			<!-- Archive Toggle -->
			<label class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 cursor-pointer">
				<input
					type="checkbox"
					bind:checked={showArchived}
					on:change={loadDocuments}
					class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
				/>
				Show archived
			</label>
		</div>

		<!-- Documents -->
		{#if loading}
			<div class="flex items-center justify-center py-20">
				<div class="animate-spin rounded-full h-8 w-8 border-2 border-blue-600 border-t-transparent"></div>
			</div>
		{:else if filteredDocuments.length === 0}
			<div class="sirru-empty-state py-20" transition:fade>
				<div class="w-20 h-20 mb-6 rounded-2xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
					<svg class="w-10 h-10 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
					</svg>
				</div>
				<h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
					{searchQuery ? 'No documents found' : 'No documents yet'}
				</h3>
				<p class="text-gray-500 dark:text-gray-400 mb-6 max-w-sm">
					{searchQuery ? 'Try adjusting your search query' : 'Create your first document to get started with AI-powered writing'}
				</p>
				{#if !searchQuery}
					<button on:click={handleCreateDocument} class="sirru-btn sirru-btn-primary sirru-btn-lg">
						<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
						</svg>
						Create Document
					</button>
				{/if}
			</div>
		{:else if viewMode === 'grid'}
			<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4" transition:fade>
				{#each filteredDocuments as doc (doc.id)}
					<a
						href="/docs/{doc.id}"
						class="sirru-doc-card group"
					>
						<!-- Document Preview -->
						<div class="aspect-[4/3] mb-3 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center overflow-hidden">
							<div class="w-full h-full p-4 text-xs text-gray-400 dark:text-gray-500 overflow-hidden">
								{#if doc.content}
									<div class="line-clamp-6">{doc.content.slice(0, 500)}</div>
								{:else}
									<div class="flex items-center justify-center h-full">
										<svg class="w-12 h-12 text-gray-300 dark:text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
											<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
										</svg>
									</div>
								{/if}
							</div>
						</div>

						<!-- Document Info -->
						<div class="flex items-start justify-between gap-2">
							<div class="flex-1 min-w-0">
								<h3 class="font-medium text-gray-900 dark:text-white truncate group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
									{doc.title}
								</h3>
								<p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
									{formatRelativeTime(doc.updated_at)}
								</p>
							</div>

							<!-- Actions Menu -->
							<div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
								<button
									on:click|preventDefault|stopPropagation={() => handleArchiveDocument(doc.id)}
									class="p-1.5 rounded-lg text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
									title="Archive"
								>
									<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
										<path stroke-linecap="round" stroke-linejoin="round" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
									</svg>
								</button>
								<button
									on:click|preventDefault|stopPropagation={() => handleDeleteDocument(doc.id)}
									class="p-1.5 rounded-lg text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
									title="Delete"
								>
									<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
										<path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
									</svg>
								</button>
							</div>
						</div>

						<!-- Tags -->
						{#if doc.tags && doc.tags.length > 0}
							<div class="flex flex-wrap gap-1 mt-2">
								{#each doc.tags.slice(0, 3) as tag}
									<span class="sirru-badge sirru-badge-info text-xs">{tag}</span>
								{/each}
								{#if doc.tags.length > 3}
									<span class="text-xs text-gray-400">+{doc.tags.length - 3}</span>
								{/if}
							</div>
						{/if}
					</a>
				{/each}
			</div>
		{:else}
			<!-- List View -->
			<div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden" transition:fade>
				<table class="w-full">
					<thead class="bg-gray-50 dark:bg-gray-800/50">
						<tr>
							<th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Title</th>
							<th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider hidden sm:table-cell">Updated</th>
							<th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider hidden md:table-cell">Created</th>
							<th class="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-200 dark:divide-gray-800">
						{#each filteredDocuments as doc (doc.id)}
							<tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
								<td class="px-4 py-4">
									<a href="/docs/{doc.id}" class="flex items-center gap-3">
										<div class="w-8 h-8 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center flex-shrink-0">
											<svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
												<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
											</svg>
										</div>
										<div class="min-w-0">
											<p class="font-medium text-gray-900 dark:text-white truncate hover:text-blue-600 dark:hover:text-blue-400">
												{doc.title}
											</p>
											{#if doc.tags && doc.tags.length > 0}
												<div class="flex gap-1 mt-1">
													{#each doc.tags.slice(0, 2) as tag}
														<span class="text-xs text-gray-400">{tag}</span>
													{/each}
												</div>
											{/if}
										</div>
									</a>
								</td>
								<td class="px-4 py-4 text-sm text-gray-500 dark:text-gray-400 hidden sm:table-cell">
									{formatRelativeTime(doc.updated_at)}
								</td>
								<td class="px-4 py-4 text-sm text-gray-500 dark:text-gray-400 hidden md:table-cell">
									{formatDate(doc.created_at)}
								</td>
								<td class="px-4 py-4 text-right">
									<div class="flex items-center justify-end gap-1">
										<button
											on:click={() => handleArchiveDocument(doc.id)}
											class="p-1.5 rounded-lg text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
											title="Archive"
										>
											<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
												<path stroke-linecap="round" stroke-linejoin="round" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
											</svg>
										</button>
										<button
											on:click={() => handleDeleteDocument(doc.id)}
											class="p-1.5 rounded-lg text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
											title="Delete"
										>
											<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
												<path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
											</svg>
										</button>
									</div>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
	</main>
</div>

<SirruGlobalSearch />
