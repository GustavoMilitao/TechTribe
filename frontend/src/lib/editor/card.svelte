<!--
SPDX-FileCopyrightText: 2023 

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import type { EditorData } from '$lib/quiz_types';
	import { QuizQuestionType } from '$lib/quiz_types';
	import { reach } from 'yup';
	import { dataSchema } from '$lib/yupSchemas';
	import Spinner from '../Spinner.svelte';
	// import { createTippy } from 'svelte-tippy';
	import { getLocalization } from '$lib/i18n';
	// import MediaComponent from "$lib/editor/MediaComponent.svelte";

	const { t } = getLocalization();

	/*	const tippy = createTippy({
        arrow: true,
        animation: 'perspective-subtle',
        placement: 'top'
    });*/

	export let data: EditorData;
	export let selected_question: number;
	export let edit_id: string;

	let uppyOpen = false;
	let unique = {};

	/*eslint no-unused-vars: ["error", { "argsIgnorePattern": "^_" }]*/
	const correctTimeInput = (_) => {
		let time = data.questions[selected_question].time;
		if (time === null || time === undefined) {
			data.questions[selected_question].time = '';
			time = '';
		}
		if (data.questions[selected_question].time > 3) {
			data.questions[selected_question].time = data.questions[selected_question].time
				.toString()
				.slice(0, 3);
		}
	};
	const set_unique = () => {
		unique = {};
	};
	$: correctTimeInput(data.questions[selected_question].time);
	$: {
		selected_question;
		set_unique();
	}
	let image_url = '';

	const update_image_url = () => {
		image_url = data.questions[selected_question].image;
	};
	$: {
		update_image_url();
		selected_question;
		data.questions;
	}

	const type_to_name = {
		RANGE: $t('words.range'),
		ABCD: $t('words.multiple_choice'),
		VOTING: $t('words.voting'),
		TEXT: $t('words.text'),
		ORDER: $t('words.order'),
		CHECK: $t('words.check_choice')
	};

	/*
    if (typeof data.questions[selected_question].type !== QuizQuestionType) {
        console.log(data.questions[selected_question].type !== QuizQuestionType.ABCD || data.questions[selected_question].type !== QuizQuestionType.RANGE)
        data.questions[selected_question].type = QuizQuestionType.ABCD;
    }
     */
</script>

<div class="w-full max-h-full pb-10 px-10 h-full">
	<div class="rounded-lg bg-white w-full h-full border-gray-500 dark:bg-gray-700 shadow-2xl">
		<div class="h-12 bg-gray-300 rounded-t-lg dark:bg-gray-500">
			<div class="flex align-middle p-4 gap-3">
			</div>
		</div>
			<div class="flex flex-col">
				<div class="flex justify-center pt-10 w-full">
					{#key unique}
						{#await import('$lib/inline-editor.svelte')}
							<Spinner my_20={false} />
						{:then c}
							<div
								class="rounded-lg placeholder:italic placeholder:font-normal dark:bg-gray-500"
								class:bg-yellow-500={!reach(
									dataSchema,
									'questions[].question'
								).isValidSync(data.questions[selected_question].question)}
							>
								<svelte:component
									this={c.default}
									bind:text={data.questions[selected_question].question}
								/>
							</div>
						{/await}
					{/key}
				</div>
				<div class="flex justify-center pt-10 w-full">
					<div>
						<svg
							class="w-8 h-8 inline-block"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
							/>
						</svg>
						<input
							type="number"
							max="999"
							min="1"
							class="w-20 bg-transparent rounded-lg text-lg border-2 border-gray-500 p-1 outline-none focus:shadow-2xl"
							bind:value={data.questions[selected_question].time}
						/>
						<p class="inline-block">s</p>
					</div>
				</div>
				<div class="flex justify-center py-5">
					<p>{type_to_name[String(data.questions[selected_question].type)]}</p>
				</div>
				<div class="flex justify-center w-full">
						{#await import('$lib/editor/ABCDEditorPart.svelte')}
							<Spinner my_20={false} />
						{:then c}
							<svelte:component
								this={c.default}
								bind:data
								bind:selected_question
								check_choice={data.questions[selected_question].type === QuizQuestionType.CHECK}
							/>
						{/await}
				</div>
			</div>
	</div>
</div>
