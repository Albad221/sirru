<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { goto } from '$app/navigation';
	import { user, chats, knowledge } from '$lib/stores';
	import { SIRRU_APPS } from '$lib/constants';
	import SirruLogo from '$lib/components/sirru/SirruLogo.svelte';
	import SirruAppCard from '$lib/components/sirru/SirruAppCard.svelte';
	import SirruGlobalSearch from '$lib/components/sirru/SirruGlobalSearch.svelte';

	const i18n = getContext('i18n');

	// Stats
	$: chatCount = $chats?.length || 0;
	$: documentCount = $knowledge?.length || 0;
	$: presentationCount = 0; // Will be populated when Presentations module is built

	// Recent activity (mock for now, will be connected to real data)
	let recentActivity = [
		{ type: 'chat', title: 'Budget Planning Discussion', time: '2 hours ago' },
		{ type: 'document', title: 'Q4 Report Draft', time: '4 hours ago' },
		{ type: 'chat', title: 'Policy Analysis', time: 'Yesterday' }
	];

	// Organization (will be connected to backend)
	let organization = {
		name: 'Demo Organization',
		logo: null
	};
</script>

<svelte:head>
	<title>Sirru - Sovereign AI Workspace</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 dark:bg-gray-950">
	<!-- Hero Section -->
	<div class="bg-sirru-gradient text-white">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
			<div class="text-center">
				<!-- Logo -->
				<div class="flex justify-center mb-6">
					<div class="bg-white/10 backdrop-blur-sm rounded-2xl p-4">
						<SirruLogo size="xl" showText={false} />
					</div>
				</div>

				<!-- Welcome Message -->
				<h1 class="text-3xl sm:text-4xl lg:text-5xl font-bold mb-4">
					Welcome to Sirru
				</h1>
				<p class="text-lg sm:text-xl text-white/80 max-w-2xl mx-auto mb-8">
					Your sovereign AI workspace. Secure, private, and built for African governments and enterprises.
				</p>

				<!-- Quick Stats -->
				<div class="flex flex-wrap justify-center gap-6 sm:gap-12">
					<div class="text-center">
						<div class="text-3xl sm:text-4xl font-bold">{chatCount}</div>
						<div class="text-sm text-white/70">Conversations</div>
					</div>
					<div class="text-center">
						<div class="text-3xl sm:text-4xl font-bold">{documentCount}</div>
						<div class="text-sm text-white/70">Documents</div>
					</div>
					<div class="text-center">
						<div class="text-3xl sm:text-4xl font-bold">{presentationCount}</div>
						<div class="text-sm text-white/70">Presentations</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Wave decoration -->
		<div class="relative h-16">
			<svg class="absolute bottom-0 w-full h-16" preserveAspectRatio="none" viewBox="0 0 1440 54">
				<path fill="currentColor" class="text-gray-50 dark:text-gray-950" d="M0 22L60 16.7C120 11 240 1.00001 360 0.700012C480 1.00001 600 11 720 19.3C840 27 960 33 1080 32.3C1200 31 1320 23 1380 18.7L1440 15V54H1380C1320 54 1200 54 1080 54C960 54 840 54 720 54C600 54 480 54 360 54C240 54 120 54 60 54H0V22Z" />
			</svg>
		</div>
	</div>

	<!-- Main Content -->
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
		<!-- Apps Section -->
		<section class="mb-16">
			<div class="flex items-center justify-between mb-6">
				<h2 class="text-2xl font-bold text-gray-900 dark:text-white">Applications</h2>
				<span class="text-sm text-gray-500 dark:text-gray-400">Your AI-powered tools</span>
			</div>

			<div class="sirru-app-grid">
				<!-- Chat AI -->
				<SirruAppCard
					app={SIRRU_APPS.CHAT}
					title="Chat AI"
					description="Engage with AI assistants for analysis, writing, coding, and strategic planning. Connect to your organization's knowledge base."
					href="/"
					badge="Active"
				/>

				<!-- Docs AI -->
				<SirruAppCard
					app={SIRRU_APPS.DOCS}
					title="Docs AI"
					description="Create, edit, and analyze documents with AI assistance. Search across your entire document corpus with natural language."
					href="/docs"
					badge="New"
				/>

				<!-- Presentations AI -->
				<SirruAppCard
					app={SIRRU_APPS.PRESENTATIONS}
					title="Slides AI"
					description="Generate professional presentations from prompts or documents. Customize with your organization's branding."
					href="/presentations"
					badge="New"
				/>
			</div>
		</section>

		<!-- Quick Actions & Recent Activity -->
		<div class="grid lg:grid-cols-2 gap-8">
			<!-- Quick Actions -->
			<section>
				<h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Quick Actions</h2>
				<div class="space-y-3">
					<a
						href="/"
						class="sirru-doc-card flex items-center gap-4 group"
					>
						<div class="w-10 h-10 rounded-lg bg-sirru-primary-100 dark:bg-sirru-primary-900/30 flex items-center justify-center group-hover:bg-sirru-primary-200 dark:group-hover:bg-sirru-primary-900/50 transition-colors">
							<svg class="w-5 h-5 text-sirru-primary-600 dark:text-sirru-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
							</svg>
						</div>
						<div>
							<p class="font-medium text-gray-900 dark:text-white">New Chat</p>
							<p class="text-sm text-gray-500 dark:text-gray-400">Start a conversation with AI</p>
						</div>
					</a>

					<a
						href="/docs/new"
						class="sirru-doc-card flex items-center gap-4 group"
					>
						<div class="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center group-hover:bg-blue-200 dark:group-hover:bg-blue-900/50 transition-colors">
							<svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
							</svg>
						</div>
						<div>
							<p class="font-medium text-gray-900 dark:text-white">New Document</p>
							<p class="text-sm text-gray-500 dark:text-gray-400">Create an AI-assisted document</p>
						</div>
					</a>

					<a
						href="/workspace/knowledge"
						class="sirru-doc-card flex items-center gap-4 group"
					>
						<div class="w-10 h-10 rounded-lg bg-sirru-gold-100 dark:bg-sirru-gold-900/30 flex items-center justify-center group-hover:bg-sirru-gold-200 dark:group-hover:bg-sirru-gold-900/50 transition-colors">
							<svg class="w-5 h-5 text-sirru-gold-600 dark:text-sirru-gold-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
							</svg>
						</div>
						<div>
							<p class="font-medium text-gray-900 dark:text-white">Knowledge Base</p>
							<p class="text-sm text-gray-500 dark:text-gray-400">Upload and query documents</p>
						</div>
					</a>
				</div>
			</section>

			<!-- Recent Activity -->
			<section>
				<h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Recent Activity</h2>
				<div class="sirru-doc-card">
					{#if $chats && $chats.length > 0}
						<div class="space-y-4">
							{#each $chats.slice(0, 5) as chat}
								<a
									href="/c/{chat.id}"
									class="flex items-center gap-3 p-2 -mx-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
								>
									<div class="w-8 h-8 rounded-lg bg-sirru-primary-100 dark:bg-sirru-primary-900/30 flex items-center justify-center flex-shrink-0">
										<svg class="w-4 h-4 text-sirru-primary-600 dark:text-sirru-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
											<path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
										</svg>
									</div>
									<div class="flex-1 min-w-0">
										<p class="font-medium text-gray-900 dark:text-white truncate">
											{chat.title || 'Untitled Chat'}
										</p>
										<p class="text-xs text-gray-500 dark:text-gray-400">
											Chat
										</p>
									</div>
								</a>
							{/each}
						</div>
					{:else}
						<div class="sirru-empty-state py-8">
							<svg class="sirru-empty-state-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
							<p class="sirru-empty-state-title">No recent activity</p>
							<p class="sirru-empty-state-description">Start a conversation or create a document to see your activity here</p>
						</div>
					{/if}
				</div>
			</section>
		</div>

		<!-- Features Overview -->
		<section class="mt-16">
			<div class="text-center mb-10">
				<h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Built for Sovereignty</h2>
				<p class="text-gray-600 dark:text-gray-400">Secure, private, and deployed on your infrastructure</p>
			</div>

			<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
				<div class="sirru-stats-card text-center">
					<div class="w-12 h-12 mx-auto mb-4 rounded-xl bg-sirru-primary-100 dark:bg-sirru-primary-900/30 flex items-center justify-center">
						<svg class="w-6 h-6 text-sirru-primary-600 dark:text-sirru-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
						</svg>
					</div>
					<h3 class="font-semibold text-gray-900 dark:text-white mb-1">Air-Gap Ready</h3>
					<p class="text-sm text-gray-500 dark:text-gray-400">Deploy without internet connectivity</p>
				</div>

				<div class="sirru-stats-card text-center">
					<div class="w-12 h-12 mx-auto mb-4 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
						<svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
						</svg>
					</div>
					<h3 class="font-semibold text-gray-900 dark:text-white mb-1">Multi-Tenant</h3>
					<p class="text-sm text-gray-500 dark:text-gray-400">Isolated workspaces per organization</p>
				</div>

				<div class="sirru-stats-card text-center">
					<div class="w-12 h-12 mx-auto mb-4 rounded-xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
						<svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
						</svg>
					</div>
					<h3 class="font-semibold text-gray-900 dark:text-white mb-1">Local AI</h3>
					<p class="text-sm text-gray-500 dark:text-gray-400">All inference runs on your hardware</p>
				</div>

				<div class="sirru-stats-card text-center">
					<div class="w-12 h-12 mx-auto mb-4 rounded-xl bg-sirru-gold-100 dark:bg-sirru-gold-900/30 flex items-center justify-center">
						<svg class="w-6 h-6 text-sirru-gold-600 dark:text-sirru-gold-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
						</svg>
					</div>
					<h3 class="font-semibold text-gray-900 dark:text-white mb-1">Audit Logging</h3>
					<p class="text-sm text-gray-500 dark:text-gray-400">Complete activity tracking</p>
				</div>
			</div>
		</section>
	</div>

	<!-- Footer -->
	<footer class="border-t border-gray-200 dark:border-gray-800 mt-16">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
			<div class="flex flex-col sm:flex-row items-center justify-between gap-4">
				<div class="flex items-center gap-2">
					<SirruLogo size="sm" showText={true} />
					<span class="text-sm text-gray-500 dark:text-gray-400">Sovereign AI Workspace</span>
				</div>
				<div class="text-sm text-gray-500 dark:text-gray-400">
					Built for African governments and enterprises
				</div>
			</div>
		</div>
	</footer>
</div>

<SirruGlobalSearch />
