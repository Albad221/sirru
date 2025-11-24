<script lang="ts">
	import { createEventDispatcher, getContext, onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { showSearch, chats } from '$lib/stores';
	import { fade, scale } from 'svelte/transition';

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	let searchQuery = '';
	let searchInput: HTMLInputElement;
	let selectedIndex = 0;
	let results: SearchResult[] = [];

	interface SearchResult {
		id: string;
		type: 'chat' | 'document' | 'presentation' | 'action';
		title: string;
		subtitle?: string;
		href: string;
		icon: string;
	}

	// Quick actions
	const quickActions: SearchResult[] = [
		{ id: 'new-chat', type: 'action', title: 'New Chat', subtitle: 'Start a conversation with AI', href: '/', icon: 'chat' },
		{ id: 'new-doc', type: 'action', title: 'New Document', subtitle: 'Create a new document', href: '/docs/new', icon: 'docs' },
		{ id: 'new-presentation', type: 'action', title: 'New Presentation', subtitle: 'Create AI-powered slides', href: '/presentations/new', icon: 'slides' },
		{ id: 'knowledge', type: 'action', title: 'Knowledge Base', subtitle: 'Browse indexed documents', href: '/workspace/knowledge', icon: 'knowledge' }
	];

	$: filteredResults = searchQuery.trim()
		? [
			...quickActions.filter(a =>
				a.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
				a.subtitle?.toLowerCase().includes(searchQuery.toLowerCase())
			),
			// Search in chats
			...($chats || [])
				.filter(chat =>
					chat.title?.toLowerCase().includes(searchQuery.toLowerCase())
				)
				.slice(0, 5)
				.map(chat => ({
					id: chat.id,
					type: 'chat' as const,
					title: chat.title || 'Untitled Chat',
					subtitle: 'Chat',
					href: `/c/${chat.id}`,
					icon: 'chat'
				}))
		]
		: quickActions;

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'ArrowDown') {
			e.preventDefault();
			selectedIndex = Math.min(selectedIndex + 1, filteredResults.length - 1);
		} else if (e.key === 'ArrowUp') {
			e.preventDefault();
			selectedIndex = Math.max(selectedIndex - 1, 0);
		} else if (e.key === 'Enter' && filteredResults[selectedIndex]) {
			e.preventDefault();
			handleSelect(filteredResults[selectedIndex]);
		} else if (e.key === 'Escape') {
			showSearch.set(false);
		}
	}

	function handleSelect(result: SearchResult) {
		showSearch.set(false);
		goto(result.href);
	}

	onMount(() => {
		if (searchInput) {
			searchInput.focus();
		}
	});

	$: selectedIndex = Math.min(selectedIndex, Math.max(0, filteredResults.length - 1));
</script>

{#if $showSearch}
	<div
		class="fixed inset-0 z-50 overflow-y-auto"
		on:click={() => showSearch.set(false)}
		on:keydown={handleKeydown}
		transition:fade={{ duration: 150 }}
	>
		<!-- Backdrop -->
		<div class="fixed inset-0 bg-black/50 backdrop-blur-sm" />

		<!-- Search Modal -->
		<div class="relative min-h-screen flex items-start justify-center pt-[15vh] px-4">
			<div
				class="relative w-full max-w-2xl bg-white dark:bg-gray-900 rounded-2xl shadow-2xl overflow-hidden"
				on:click|stopPropagation
				transition:scale={{ duration: 200, start: 0.95 }}
			>
				<!-- Search Input -->
				<div class="flex items-center gap-3 p-4 border-b border-gray-200 dark:border-gray-800">
					<svg class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
					</svg>
					<input
						bind:this={searchInput}
						bind:value={searchQuery}
						type="text"
						placeholder="Search across chat history, documents, and more..."
						class="flex-1 bg-transparent border-0 outline-none text-gray-900 dark:text-white placeholder:text-gray-400"
					/>
					<kbd class="hidden sm:inline-flex items-center px-2 py-1 text-xs text-gray-400 bg-gray-100 dark:bg-gray-800 rounded">
						ESC
					</kbd>
				</div>

				<!-- Results -->
				<div class="max-h-[60vh] overflow-y-auto p-2">
					{#if filteredResults.length === 0}
						<div class="sirru-empty-state py-8">
							<svg class="sirru-empty-state-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
							</svg>
							<p class="sirru-empty-state-title">No results found</p>
							<p class="sirru-empty-state-description">Try searching for something else</p>
						</div>
					{:else}
						<div class="space-y-1">
							{#if !searchQuery.trim()}
								<p class="px-3 py-2 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
									Quick Actions
								</p>
							{/if}
							{#each filteredResults as result, index}
								<button
									class="w-full flex items-center gap-3 px-3 py-3 rounded-xl transition-colors {index === selectedIndex ? 'bg-sirru-primary-50 dark:bg-sirru-primary-900/20' : 'hover:bg-gray-100 dark:hover:bg-gray-800'}"
									on:click={() => handleSelect(result)}
									on:mouseenter={() => selectedIndex = index}
								>
									<!-- Icon -->
									<div class="flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center {
										result.type === 'chat' || result.icon === 'chat'
											? 'bg-sirru-primary-100 dark:bg-sirru-primary-900/30 text-sirru-primary-600 dark:text-sirru-primary-400'
											: result.icon === 'docs'
												? 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
												: result.icon === 'slides'
													? 'bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400'
													: 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'
									}">
										{#if result.icon === 'chat'}
											<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
												<path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
											</svg>
										{:else if result.icon === 'docs'}
											<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
												<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
											</svg>
										{:else if result.icon === 'slides'}
											<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
												<path stroke-linecap="round" stroke-linejoin="round" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
											</svg>
										{:else if result.icon === 'knowledge'}
											<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
												<path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
											</svg>
										{/if}
									</div>

									<!-- Content -->
									<div class="flex-1 min-w-0 text-left">
										<p class="font-medium text-gray-900 dark:text-white truncate">
											{result.title}
										</p>
										{#if result.subtitle}
											<p class="text-sm text-gray-500 dark:text-gray-400 truncate">
												{result.subtitle}
											</p>
										{/if}
									</div>

									<!-- Arrow -->
									{#if index === selectedIndex}
										<svg class="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
											<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
										</svg>
									{/if}
								</button>
							{/each}
						</div>
					{/if}
				</div>

				<!-- Footer -->
				<div class="flex items-center justify-between px-4 py-3 border-t border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-800/50">
					<div class="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400">
						<span class="flex items-center gap-1">
							<kbd class="px-1.5 py-0.5 bg-gray-200 dark:bg-gray-700 rounded">↑</kbd>
							<kbd class="px-1.5 py-0.5 bg-gray-200 dark:bg-gray-700 rounded">↓</kbd>
							Navigate
						</span>
						<span class="flex items-center gap-1">
							<kbd class="px-1.5 py-0.5 bg-gray-200 dark:bg-gray-700 rounded">↵</kbd>
							Select
						</span>
					</div>
					<span class="text-xs text-gray-400">
						Powered by Sirru
					</span>
				</div>
			</div>
		</div>
	</div>
{/if}
