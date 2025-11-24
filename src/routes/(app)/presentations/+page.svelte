<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { goto } from '$app/navigation';
	import { toast } from 'svelte-sonner';
	import { fade } from 'svelte/transition';

	import { user } from '$lib/stores';
	import {
		getPresentations,
		createPresentation,
		deletePresentation,
		archivePresentation,
		createTitleSlide,
		type Presentation
	} from '$lib/apis/presentations';

	import SirruGlobalSearch from '$lib/components/sirru/SirruGlobalSearch.svelte';

	const i18n = getContext('i18n');

	let presentations: Presentation[] = [];
	let loading = true;
	let searchQuery = '';
	let showArchived = false;

	$: filteredPresentations = presentations.filter((pres) =>
		pres.title.toLowerCase().includes(searchQuery.toLowerCase())
	);

	async function loadPresentations() {
		try {
			loading = true;
			presentations = await getPresentations(localStorage.token, showArchived);
		} catch (error) {
			toast.error('Failed to load presentations');
			console.error(error);
		} finally {
			loading = false;
		}
	}

	async function handleCreatePresentation() {
		try {
			const pres = await createPresentation(localStorage.token, {
				title: 'Untitled Presentation',
				slides: [createTitleSlide('Untitled Presentation', 'Click to add subtitle')]
			});
			goto(`/presentations/${pres.id}`);
		} catch (error) {
			toast.error('Failed to create presentation');
			console.error(error);
		}
	}

	async function handleDeletePresentation(id: string) {
		if (!confirm('Are you sure you want to delete this presentation?')) return;

		try {
			await deletePresentation(localStorage.token, id);
			presentations = presentations.filter((p) => p.id !== id);
			toast.success('Presentation deleted');
		} catch (error) {
			toast.error('Failed to delete presentation');
			console.error(error);
		}
	}

	async function handleArchivePresentation(id: string) {
		try {
			await archivePresentation(localStorage.token, id);
			presentations = presentations.filter((p) => p.id !== id);
			toast.success('Presentation archived');
		} catch (error) {
			toast.error('Failed to archive presentation');
			console.error(error);
		}
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
		return new Date(timestamp * 1000).toLocaleDateString('en-US', {
			month: 'short',
			day: 'numeric',
			year: 'numeric'
		});
	}

	onMount(() => {
		if (!$user) {
			goto('/auth');
			return;
		}
		loadPresentations();
	});
</script>

<svelte:head>
	<title>Slides AI - Sirru</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 dark:bg-gray-950">
	<!-- Header -->
	<header class="sirru-header">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex items-center justify-between h-16">
				<!-- Left: Back to Home & Title -->
				<div class="flex items-center gap-4">
					<a
						href="/home"
						class="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
					>
						<svg
							class="w-5 h-5"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
						</svg>
					</a>
					<div class="flex items-center gap-3">
						<div
							class="w-8 h-8 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center"
						>
							<svg
								class="w-4 h-4 text-purple-600 dark:text-purple-400"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
								stroke-width="2"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"
								/>
							</svg>
						</div>
						<h1 class="text-xl font-semibold text-gray-900 dark:text-white">Slides AI</h1>
					</div>
				</div>

				<!-- Right: Actions -->
				<div class="flex items-center gap-3">
					<button on:click={handleCreatePresentation} class="sirru-btn sirru-btn-primary sirru-btn-md">
						<svg
							class="w-4 h-4"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
						</svg>
						New Presentation
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
				<svg
					class="sirru-search-icon w-5 h-5"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					stroke-width="2"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
					/>
				</svg>
				<input
					type="text"
					bind:value={searchQuery}
					placeholder="Search presentations..."
					class="sirru-search-input"
				/>
			</div>

			<!-- Archive Toggle -->
			<label
				class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 cursor-pointer"
			>
				<input
					type="checkbox"
					bind:checked={showArchived}
					on:change={loadPresentations}
					class="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
				/>
				Show archived
			</label>
		</div>

		<!-- Presentations -->
		{#if loading}
			<div class="flex items-center justify-center py-20">
				<div
					class="animate-spin rounded-full h-8 w-8 border-2 border-purple-600 border-t-transparent"
				></div>
			</div>
		{:else if filteredPresentations.length === 0}
			<div class="sirru-empty-state py-20" transition:fade>
				<div
					class="w-20 h-20 mb-6 rounded-2xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center"
				>
					<svg
						class="w-10 h-10 text-purple-600 dark:text-purple-400"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="1.5"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"
						/>
					</svg>
				</div>
				<h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
					{searchQuery ? 'No presentations found' : 'No presentations yet'}
				</h3>
				<p class="text-gray-500 dark:text-gray-400 mb-6 max-w-sm">
					{searchQuery
						? 'Try adjusting your search query'
						: 'Create your first presentation with AI-powered slide generation'}
				</p>
				{#if !searchQuery}
					<button on:click={handleCreatePresentation} class="sirru-btn sirru-btn-primary sirru-btn-lg">
						<svg
							class="w-5 h-5"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
						</svg>
						Create Presentation
					</button>
				{/if}
			</div>
		{:else}
			<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3" transition:fade>
				{#each filteredPresentations as pres (pres.id)}
					<a href="/presentations/{pres.id}" class="sirru-slide-card group cursor-pointer">
						<!-- Slide Preview -->
						<div
							class="aspect-video bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 flex items-center justify-center p-6"
						>
							<div class="text-center">
								<h3
									class="text-lg font-semibold text-gray-900 dark:text-white group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors line-clamp-2"
								>
									{pres.title}
								</h3>
								{#if pres.slides[0]?.subtitle}
									<p class="text-sm text-gray-500 dark:text-gray-400 mt-1 line-clamp-1">
										{pres.slides[0].subtitle}
									</p>
								{/if}
							</div>
						</div>

						<!-- Info Bar -->
						<div
							class="absolute bottom-0 left-0 right-0 bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm px-4 py-3 border-t border-gray-200 dark:border-gray-700"
						>
							<div class="flex items-center justify-between">
								<div class="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
									<span>{pres.slide_count} slides</span>
									<span>&middot;</span>
									<span>{formatRelativeTime(pres.updated_at)}</span>
								</div>

								<!-- Actions -->
								<div
									class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity"
								>
									<button
										on:click|preventDefault|stopPropagation={() =>
											handleArchivePresentation(pres.id)}
										class="p-1.5 rounded-lg text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
										title="Archive"
									>
										<svg
											class="w-4 h-4"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
											stroke-width="2"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"
											/>
										</svg>
									</button>
									<button
										on:click|preventDefault|stopPropagation={() =>
											handleDeletePresentation(pres.id)}
										class="p-1.5 rounded-lg text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
										title="Delete"
									>
										<svg
											class="w-4 h-4"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
											stroke-width="2"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
											/>
										</svg>
									</button>
								</div>
							</div>
						</div>
					</a>
				{/each}
			</div>
		{/if}
	</main>
</div>

<SirruGlobalSearch />
