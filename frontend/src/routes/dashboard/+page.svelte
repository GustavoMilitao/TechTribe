<!--
SPDX-FileCopyrightText: 2023 

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import DownloadQuiz from '$lib/components/DownloadQuiz.svelte';
	import type { QuizData } from '$lib/quiz_types';
	import { getLocalization } from '$lib/i18n';
	import { navbarVisible, signedIn } from '$lib/stores';
	import CommandpaletteNotice from '$lib/components/popover/commandpalettenotice.svelte';
	import Fuse from 'fuse.js';
	import type { PageData } from './$types';
	import { fly } from 'svelte/transition';
	import StartGamePopup from '$lib/dashboard/start_game.svelte';
	import Analytics from './Analytics.svelte';
	import MediaComponent from '$lib/editor/MediaComponent.svelte';
	import { createTippy } from 'svelte-tippy';
	import GreenButton from '$lib/components/buttons/green.svelte';

	// import GrayButton from "$lib/components/buttons/gray.svelte";

	export let data: PageData;
	let search_term = '';
	let download_id: string | null = null;
	signedIn.set(true);
	navbarVisible.set(true);
	const { t } = getLocalization();

	let items_to_show = [];
	let all_items: Array<any>;
	let fuse;
	const tippy = createTippy({
		arrow: true,
		animation: 'perspective-subtle',
		placement: 'bottom'
	});

	let id_to_position_map = {};

	const start_game = async (id: string) => {
		let res;
		const cqcs_enabled_parsed = 'False';
		const randomized_answers_parsed = 'False';

		res = await fetch(
			`/api/v1/quiz/start/${id}?captcha_enabled=False&game_mode=normal&custom_field=&cqcs_enabled=${cqcs_enabled_parsed}&randomize_answers=${randomized_answers_parsed}`,
			{
				method: 'POST'
			}
		);
		if (res.status !== 200) {
			/*			alertModal.set({
				open: true,
				title: 'Start failed',
				body: `Failed to start game, ${await res.text()}`
			});*/
			/*alertModal.subscribe((_) => {
				window.location.assign('/account/login?returnTo=/dashboard');
			});*/
			alert('Starting game failed');
			window.location.assign('/account/login?returnTo=/dashboard');
		} else {
			const data = await res.json();
			// eslint-disable-next-line no-undef
			plausible('Started Game', { props: { quiz_id: id, game_id: data.game_id } });
			window.location.assign(
				`/admin?token=${data.game_id}&pin=${data.game_pin}&connect=1&cqc_code=${data.cqc_code}`
			);
		}
	};

	const getData = async (): Promise<Array<QuizData>> => {
		const quiz_res = await fetch('/api/v1/quiz/list?page_size=100');
		data.quizzes = await quiz_res.json();
		items_to_show = [];
		for (let i = 0; i < data.quizzes.length; i++) {
			items_to_show.push({ ...data.quizzes[i], type: 'quiz' });
		}
		fuse = new Fuse(items_to_show, {
			keys: ['title', 'description', 'questions.title'],
			findAllMatches: true
		});
		all_items = items_to_show;
		for (let i = 0; i < all_items.length; i++) {
			id_to_position_map[all_items[i].id] = i;
		}
		return all_items;
	};

	const search = () => {
		if (search_term === '') {
			items_to_show = all_items;
		} else {
			const res = fuse.search(search_term);
			console.log(res, 'search_res');
			items_to_show = [];
			for (const quiz_data of res) {
				items_to_show.push(quiz_data.item);
			}

			items_to_show = items_to_show;
		}
	};
	$: {
		search_term;
		search();
	}

	const deleteQuiz = async (to_delete: string, type: 'quiz') => {
		if (!confirm('Quer mesmo apagar esse quiz?')) {
			return;
		}
		if (type === 'quiz') {
			await fetch(`/api/v1/quiz/delete/${to_delete}`, {
				method: 'DELETE'
			});
		}
		window.location.reload();
	};
	let create_button_clicked = false;

	let analytics_quiz_selected: undefined | QuizData = undefined;
</script>

<svelte:head>
	<title>TechTribe - Dashboard</title>
</svelte:head>
<Analytics bind:quiz={analytics_quiz_selected} />
<CommandpaletteNotice />
<div class="min-h-screen flex flex-col">
	{#await getData()}
		<svg class="h-8 w-8 animate-spin mx-auto my-20" viewBox="3 3 18 18">
			<path
				class="fill-black"
				d="M12 5C8.13401 5 5 8.13401 5 12C5 15.866 8.13401 19 12 19C15.866 19 19 15.866 19 12C19 8.13401 15.866 5 12 5ZM3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12Z"
			/>
			<path
				class="fill-blue-100"
				d="M16.9497 7.05015C14.2161 4.31648 9.78392 4.31648 7.05025 7.05015C6.65973 7.44067 6.02656 7.44067 5.63604 7.05015C5.24551 6.65962 5.24551 6.02646 5.63604 5.63593C9.15076 2.12121 14.8492 2.12121 18.364 5.63593C18.7545 6.02646 18.7545 6.65962 18.364 7.05015C17.9734 7.44067 17.3403 7.44067 16.9497 7.05015Z"
			/>
		</svg>
	{:then quizzes}
		<div class="flex flex-col w-full mx-auto">
			<!--		<button
                    class='px-4 py-2 font-medium tracking-wide text-gray-500 whitespace-nowrap dark:text-gray-400 capitalize transition-colors dark:bg-gray-700 duration-200 transform bg-[#B07156] rounded-md hover:bg-green-600 focus:outline-none focus:ring focus:ring-blue-300 focus:ring-opacity-80'>
                    Primary
                </button>-->
			<div class="w-full grid lg:grid-cols-1 gap-2 grid-cols-2 px-4">
				{#if create_button_clicked}
					<div
						class="flex gap-2"
						transition:fly={{ y: 10 }}
						use:tippy={{ content: 'Unsure? Choose "Quiz".' }}
					>
						<GreenButton href="/create">{$t('words.quiz')}</GreenButton>
					</div>
				{:else}
					<GreenButton href="/create"
						>{$t('words.create') + ' ' + $t('words.quiz')}</GreenButton
					>
				{/if}
			</div>
			{#if quizzes.length !== 0}
				<div class="flex flex-col gap-4 mt-4 px-2">
					{#each items_to_show as quiz}
						<div
							class="grid grid-cols-2 lg:grid-cols-3 w-full rounded border-[#B07156] border-2 p-2 h-[20vh] overflow-hidden max-h-[20vh]"
						>
							<div class="hidden lg:flex w-auto h-full items-center relative">
								{#if quiz.cover_image}
									<!--									<img
										src="/api/v1/storage/download/{quiz.cover_image}"
										alt="user provided"
										loading="lazy"
										class="shrink-0 max-w-full max-h-full absolute rounded"
									/>-->
									<MediaComponent
										src={quiz.cover_image}
										css_classes="shrink-0 max-w-full max-h-full absolute rounded"
									/>
								{/if}
							</div>
							<div class="my-auto mx-auto max-h-full overflow-hidden">
								<p class="text-xl text-center">{@html quiz.title}</p>
								<p class="text-sm text-center text-clip overflow-hidden">
									{@html quiz.description ?? ''}
								</p>
							</div>
							<div
								class="grid grid-rows-2 ml-auto gap-2 w-fit self-end my-auto"
								class:grid-cols-3={quiz.type === 'quiz'}
							>
								{#if quiz.type === 'quiz'}
									<GreenButton
										on:click={() => {
											start_game(quiz.id);
										}}
										flex={true}
									>
										<!-- heroicons/legacy-outline/Play -->
										<svg
											class="w-5 h-5"
											aria-hidden="true"
											fill="none"
											stroke="currentColor"
											stroke-width="2"
											viewBox="0 0 24 24"
											xmlns="http://www.w3.org/2000/svg"
										>
											<path
												d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
												stroke-linecap="round"
												stroke-linejoin="round"
											/>
											<path
												d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
												stroke-linecap="round"
												stroke-linejoin="round"
											/>
										</svg>
									</GreenButton>
								{/if}

								<GreenButton
									on:click={() => {
										deleteQuiz(quiz.id, quiz.type);
									}}
									flex={true}
								>
									<!-- heroicons/trash -->
									<svg
										class="w-5 h-5"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
										xmlns="http://www.w3.org/2000/svg"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
										/>
									</svg>
								</GreenButton>
							</div>
						</div>
					{/each}
				</div>
			{:else}
				<div class="w-full grid lg:grid-cols-1 gap-1 grid-cols-1 px-4">
					<p style="color: white;">
						{$t('overview_page.no_quizzes')}
					</p>
				</div>
			{/if}
		</div>
	{:catch err}
		<p>{err}</p>
	{/await}
</div>
<!-- {#if start_game !== null}
	<StartGamePopup bind:quiz_id={start_game} />
{/if} -->
<DownloadQuiz bind:quiz_id={download_id} />
