<script lang="ts">
	import { onMount, onDestroy, getContext } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { toast } from 'svelte-sonner';
	import { fade, fly } from 'svelte/transition';

	import { user } from '$lib/stores';
	import {
		getPresentationById,
		updatePresentation,
		updateSlides,
		deletePresentation,
		duplicatePresentation,
		getThemes,
		createBlankSlide,
		type Presentation,
		type Slide,
		type Theme
	} from '$lib/apis/presentations';

	import SirruGlobalSearch from '$lib/components/sirru/SirruGlobalSearch.svelte';

	const i18n = getContext('i18n');

	let presentation: Presentation | null = null;
	let slides: Slide[] = [];
	let themes: Theme[] = [];
	let loading = true;
	let saving = false;

	let currentSlideIndex = 0;
	let editingTitle = false;
	let titleInput = '';

	let autoSaveTimer: ReturnType<typeof setTimeout> | null = null;
	let hasUnsavedChanges = false;

	// AI Generation modal
	let showAIModal = false;
	let aiPrompt = '';
	let aiGenerating = false;

	$: presentationId = $page.params.id;
	$: currentSlide = slides[currentSlideIndex] || null;

	async function loadPresentation() {
		try {
			loading = true;
			presentation = await getPresentationById(localStorage.token, presentationId);
			slides = presentation.slides || [];
			titleInput = presentation.title;
			themes = await getThemes(localStorage.token);
		} catch (error) {
			toast.error('Failed to load presentation');
			console.error(error);
			goto('/presentations');
		} finally {
			loading = false;
		}
	}

	async function handleSave() {
		if (!presentation) return;

		try {
			saving = true;
			await updateSlides(localStorage.token, presentationId, slides);
			if (titleInput !== presentation.title) {
				await updatePresentation(localStorage.token, presentationId, { title: titleInput });
				presentation.title = titleInput;
			}
			hasUnsavedChanges = false;
			toast.success('Presentation saved');
		} catch (error) {
			toast.error('Failed to save presentation');
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
		autoSaveTimer = setTimeout(handleSave, 5000);
	}

	function addSlide(type: Slide['type'] = 'content') {
		const newSlide = createBlankSlide(slides.length, type);
		slides = [...slides, newSlide];
		currentSlideIndex = slides.length - 1;
		scheduleAutoSave();
	}

	function deleteSlide(index: number) {
		if (slides.length <= 1) {
			toast.error('Cannot delete the last slide');
			return;
		}
		slides = slides.filter((_, i) => i !== index);
		if (currentSlideIndex >= slides.length) {
			currentSlideIndex = slides.length - 1;
		}
		scheduleAutoSave();
	}

	function duplicateSlide(index: number) {
		const original = slides[index];
		const copy: Slide = {
			...original,
			id: `slide-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
			order: slides.length
		};
		slides = [...slides.slice(0, index + 1), copy, ...slides.slice(index + 1)];
		currentSlideIndex = index + 1;
		scheduleAutoSave();
	}

	function moveSlide(fromIndex: number, toIndex: number) {
		if (toIndex < 0 || toIndex >= slides.length) return;
		const newSlides = [...slides];
		const [moved] = newSlides.splice(fromIndex, 1);
		newSlides.splice(toIndex, 0, moved);
		slides = newSlides.map((s, i) => ({ ...s, order: i }));
		currentSlideIndex = toIndex;
		scheduleAutoSave();
	}

	function updateCurrentSlide(field: keyof Slide, value: string | string[]) {
		if (!currentSlide) return;
		slides = slides.map((s, i) => (i === currentSlideIndex ? { ...s, [field]: value } : s));
		scheduleAutoSave();
	}

	async function handleDelete() {
		if (!presentation) return;
		if (!confirm('Are you sure you want to delete this presentation?')) return;

		try {
			await deletePresentation(localStorage.token, presentation.id);
			toast.success('Presentation deleted');
			goto('/presentations');
		} catch (error) {
			toast.error('Failed to delete presentation');
			console.error(error);
		}
	}

	async function handleDuplicate() {
		if (!presentation) return;

		try {
			const newPres = await duplicatePresentation(localStorage.token, presentation.id);
			toast.success('Presentation duplicated');
			goto(`/presentations/${newPres.id}`);
		} catch (error) {
			toast.error('Failed to duplicate presentation');
			console.error(error);
		}
	}

	async function handleGenerateWithAI() {
		if (!aiPrompt.trim()) return;

		try {
			aiGenerating = true;
			toast.info('AI generation coming soon!');
			// TODO: Integrate with AI to generate slides
		} catch (error) {
			toast.error('AI generation failed');
			console.error(error);
		} finally {
			aiGenerating = false;
			showAIModal = false;
		}
	}

	function handleKeydown(e: KeyboardEvent) {
		if ((e.ctrlKey || e.metaKey) && e.key === 's') {
			e.preventDefault();
			handleSave();
		}
		if (e.key === 'ArrowLeft' && currentSlideIndex > 0) {
			currentSlideIndex--;
		}
		if (e.key === 'ArrowRight' && currentSlideIndex < slides.length - 1) {
			currentSlideIndex++;
		}
	}

	onMount(() => {
		if (!$user) {
			goto('/auth');
			return;
		}
		loadPresentation();
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
	<title>{presentation?.title || 'Presentation'} - Slides AI - Sirru</title>
</svelte:head>

<div class="h-screen flex flex-col bg-gray-100 dark:bg-gray-950">
	<!-- Header -->
	<header class="sirru-header flex-shrink-0">
		<div class="max-w-full px-4">
			<div class="flex items-center justify-between h-14">
				<!-- Left: Back & Title -->
				<div class="flex items-center gap-3 flex-1 min-w-0">
					<a
						href="/presentations"
						class="p-2 rounded-lg text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
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

					<div class="flex items-center gap-2 flex-1 min-w-0">
						<div
							class="w-6 h-6 rounded bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center flex-shrink-0"
						>
							<svg
								class="w-3 h-3 text-purple-600 dark:text-purple-400"
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
						<input
							bind:value={titleInput}
							on:change={scheduleAutoSave}
							placeholder="Untitled Presentation"
							class="flex-1 min-w-0 bg-transparent border-0 text-lg font-medium text-gray-900 dark:text-white placeholder:text-gray-400 focus:outline-none focus:ring-0"
						/>
					</div>
				</div>

				<!-- Center: Slide Navigation -->
				<div class="hidden md:flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
					<span>Slide {currentSlideIndex + 1} of {slides.length}</span>
					{#if hasUnsavedChanges}
						<span class="text-amber-600 dark:text-amber-400">&middot; Unsaved</span>
					{/if}
				</div>

				<!-- Right: Actions -->
				<div class="flex items-center gap-2">
					<!-- AI Generate Button -->
					<button
						on:click={() => (showAIModal = true)}
						class="sirru-btn sirru-btn-secondary sirru-btn-sm"
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
								d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
							/>
						</svg>
						<span class="hidden sm:inline">AI Generate</span>
					</button>

					<!-- Save Button -->
					<button on:click={handleSave} disabled={saving} class="sirru-btn sirru-btn-primary sirru-btn-sm">
						{#if saving}
							<div
								class="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"
							></div>
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
		<!-- Slide Thumbnails Sidebar -->
		<aside
			class="w-48 lg:w-56 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col"
		>
			<div class="flex-1 overflow-y-auto p-3 space-y-2">
				{#each slides as slide, index (slide.id)}
					<button
						on:click={() => (currentSlideIndex = index)}
						class="w-full relative group"
						transition:fade={{ duration: 150 }}
					>
						<!-- Thumbnail -->
						<div
							class="aspect-video rounded-lg overflow-hidden border-2 transition-all {index ===
							currentSlideIndex
								? 'border-purple-500 ring-2 ring-purple-500/30'
								: 'border-gray-200 dark:border-gray-700 hover:border-purple-300 dark:hover:border-purple-700'}"
						>
							<div
								class="w-full h-full bg-white dark:bg-gray-800 p-2 flex items-center justify-center"
							>
								<div class="text-center overflow-hidden">
									<p class="text-[8px] font-medium text-gray-900 dark:text-white truncate">
										{slide.title || 'Untitled'}
									</p>
								</div>
							</div>
						</div>

						<!-- Slide Number -->
						<span
							class="absolute top-1 left-1 text-[10px] px-1.5 py-0.5 rounded bg-gray-900/70 text-white"
						>
							{index + 1}
						</span>

						<!-- Actions -->
						<div
							class="absolute top-1 right-1 opacity-0 group-hover:opacity-100 transition-opacity flex gap-0.5"
						>
							<button
								on:click|stopPropagation={() => duplicateSlide(index)}
								class="p-1 rounded bg-gray-900/70 text-white hover:bg-gray-900"
								title="Duplicate"
							>
								<svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
									/>
								</svg>
							</button>
							<button
								on:click|stopPropagation={() => deleteSlide(index)}
								class="p-1 rounded bg-red-600/70 text-white hover:bg-red-600"
								title="Delete"
							>
								<svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
									/>
								</svg>
							</button>
						</div>
					</button>
				{/each}
			</div>

			<!-- Add Slide Button -->
			<div class="p-3 border-t border-gray-200 dark:border-gray-800">
				<button
					on:click={() => addSlide('content')}
					class="w-full py-2 px-3 rounded-lg border-2 border-dashed border-gray-300 dark:border-gray-600 text-gray-500 dark:text-gray-400 hover:border-purple-400 hover:text-purple-600 dark:hover:text-purple-400 transition-colors text-sm flex items-center justify-center gap-2"
				>
					<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
					</svg>
					Add Slide
				</button>
			</div>
		</aside>

		<!-- Slide Editor -->
		<main class="flex-1 flex flex-col overflow-hidden">
			{#if loading}
				<div class="flex-1 flex items-center justify-center">
					<div
						class="animate-spin rounded-full h-8 w-8 border-2 border-purple-600 border-t-transparent"
					></div>
				</div>
			{:else if currentSlide}
				<!-- Slide Canvas -->
				<div class="flex-1 flex items-center justify-center p-8 overflow-auto">
					<div
						class="w-full max-w-4xl aspect-video bg-white dark:bg-gray-800 rounded-xl shadow-xl overflow-hidden"
					>
						<div class="w-full h-full p-12 flex flex-col items-center justify-center text-center">
							{#if currentSlide.type === 'title'}
								<input
									value={currentSlide.title || ''}
									on:input={(e) => updateCurrentSlide('title', e.currentTarget.value)}
									placeholder="Presentation Title"
									class="w-full text-center bg-transparent border-0 text-4xl font-bold text-gray-900 dark:text-white placeholder:text-gray-300 focus:outline-none focus:ring-0"
								/>
								<input
									value={currentSlide.subtitle || ''}
									on:input={(e) => updateCurrentSlide('subtitle', e.currentTarget.value)}
									placeholder="Subtitle"
									class="w-full text-center bg-transparent border-0 text-xl text-gray-500 dark:text-gray-400 placeholder:text-gray-300 focus:outline-none focus:ring-0 mt-4"
								/>
							{:else}
								<input
									value={currentSlide.title || ''}
									on:input={(e) => updateCurrentSlide('title', e.currentTarget.value)}
									placeholder="Slide Title"
									class="w-full bg-transparent border-0 text-3xl font-bold text-gray-900 dark:text-white placeholder:text-gray-300 focus:outline-none focus:ring-0 mb-6"
								/>
								<textarea
									value={currentSlide.content || ''}
									on:input={(e) => updateCurrentSlide('content', e.currentTarget.value)}
									placeholder="Add your content here..."
									class="w-full flex-1 bg-transparent border-0 text-lg text-gray-700 dark:text-gray-300 placeholder:text-gray-300 focus:outline-none focus:ring-0 resize-none"
								/>
							{/if}
						</div>
					</div>
				</div>

				<!-- Bottom Toolbar -->
				<div
					class="flex-shrink-0 px-6 py-4 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800"
				>
					<div class="flex items-center justify-between max-w-4xl mx-auto">
						<!-- Navigation -->
						<div class="flex items-center gap-2">
							<button
								on:click={() => currentSlideIndex > 0 && currentSlideIndex--}
								disabled={currentSlideIndex === 0}
								class="p-2 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
							>
								<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
								</svg>
							</button>
							<span class="text-sm text-gray-500 dark:text-gray-400">
								{currentSlideIndex + 1} / {slides.length}
							</span>
							<button
								on:click={() => currentSlideIndex < slides.length - 1 && currentSlideIndex++}
								disabled={currentSlideIndex === slides.length - 1}
								class="p-2 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
							>
								<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
								</svg>
							</button>
						</div>

						<!-- Slide Type Selector -->
						<div class="flex items-center gap-2">
							<span class="text-sm text-gray-500 dark:text-gray-400">Layout:</span>
							<select
								value={currentSlide.type}
								on:change={(e) => updateCurrentSlide('type', e.currentTarget.value)}
								class="text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white px-3 py-1.5 focus:ring-2 focus:ring-purple-500"
							>
								<option value="title">Title</option>
								<option value="content">Content</option>
								<option value="two-column">Two Column</option>
								<option value="image">Image</option>
								<option value="quote">Quote</option>
								<option value="blank">Blank</option>
							</select>
						</div>

						<!-- Move Buttons -->
						<div class="flex items-center gap-2">
							<button
								on:click={() => moveSlide(currentSlideIndex, currentSlideIndex - 1)}
								disabled={currentSlideIndex === 0}
								class="p-2 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
								title="Move slide up"
							>
								<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7" />
								</svg>
							</button>
							<button
								on:click={() => moveSlide(currentSlideIndex, currentSlideIndex + 1)}
								disabled={currentSlideIndex === slides.length - 1}
								class="p-2 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
								title="Move slide down"
							>
								<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
								</svg>
							</button>
						</div>
					</div>
				</div>
			{/if}
		</main>
	</div>
</div>

<!-- AI Generate Modal -->
{#if showAIModal}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
		on:click={() => (showAIModal = false)}
		transition:fade
	>
		<div
			class="w-full max-w-lg bg-white dark:bg-gray-900 rounded-2xl shadow-2xl"
			on:click|stopPropagation
			transition:fly={{ y: 20 }}
		>
			<div class="p-6">
				<h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">
					Generate Slides with AI
				</h3>
				<p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
					Describe what you want your presentation to be about and AI will generate slides for you.
				</p>
				<textarea
					bind:value={aiPrompt}
					placeholder="E.g., Create a 10-slide presentation about climate change impacts on African agriculture..."
					class="sirru-input min-h-[120px] resize-none"
				/>
			</div>
			<div
				class="px-6 py-4 bg-gray-50 dark:bg-gray-800/50 rounded-b-2xl flex justify-end gap-3"
			>
				<button on:click={() => (showAIModal = false)} class="sirru-btn sirru-btn-secondary sirru-btn-md">
					Cancel
				</button>
				<button
					on:click={handleGenerateWithAI}
					disabled={aiGenerating || !aiPrompt.trim()}
					class="sirru-btn sirru-btn-primary sirru-btn-md"
				>
					{#if aiGenerating}
						<div
							class="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"
						></div>
					{/if}
					Generate
				</button>
			</div>
		</div>
	</div>
{/if}

<SirruGlobalSearch />
