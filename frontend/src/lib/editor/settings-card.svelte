<!--
SPDX-FileCopyrightText: 2023 

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import type { EditorData } from '$lib/quiz_types';
	import { getLocalization } from '$lib/i18n';
	import Spinner from '$lib/Spinner.svelte';
	import { createTippy } from 'svelte-tippy';

	const { t } = getLocalization();

	export let edit_id: string;
	export let data: EditorData;

	let custom_bg_color = Boolean(data.background_color);
	const tippy = createTippy({
		arrow: true,
		animation: 'perspective-subtle'
	});

	$: data.background_color = custom_bg_color ? data.background_color : undefined;
</script>

<div class="w-full h-full pb-20 px-20">
	<div class="rounded-lg bg-white w-full h-full border-gray-500 dark:bg-gray-700">
		<div class="h-fit bg-gray-300 rounded-t-lg dark:bg-gray-500">
			<div class="flex align-middle p-4 gap-3">
			</div>
		</div>
		<div
			class="dark:bg-gray-700 h-full"
			style="background-repeat: no-repeat;background-size: 100% 100%;background-image: {data.background_image
				? `url("/api/v1/storage/download/${data.background_image}")`
				: `unset`}"
		>
			<div class="flex justify-center pt-10 w-full">
				<!--<input
				type="text"
				bind:value={data.title}
				class="p-3 rounded-lg border-gray-500 border text-center w-1/3 text-lg font-semibold dark:bg-gray-500"
			/>-->
				{#await import('$lib/inline-editor.svelte')}
					<Spinner my_20={false} />
				{:then c}
					<svelte:component this={c.default} bind:text={data.title} />
				{/await}
			</div>
			<div class="flex justify-center pt-10 w-full max-h-32">
				<textarea
					type="text"
					placeholder="Description"
					bind:value={data.description}
					class="p-3 rounded-lg border-gray-500 border text-center w-1/3 h-20 resize-none dark:bg-gray-500 outline-none focus:shadow-2xl transition-all"
				/>
			</div>

			<div class="w-full flex justify-center -mt-8">
			</div>
		</div>
	</div>
</div>
