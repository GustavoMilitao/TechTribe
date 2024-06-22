<!--
SPDX-FileCopyrightText: 2023 

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import type { PageData } from './$types';
	import GreenButton from '$lib/components/buttons/green.svelte';

	export let data: PageData;
</script>

<div class="flex flex-col p-2">
	{#each data.quizzes as quiz}
		<div class="border-2 border-[#B07156] rounded w-full h-[20vh] p-2 flex flex-col gap-2">
			<div class="grid grid-cols-3 h-full">
				<div class="hidden lg:flex w-auto h-full items-center relative">
					{#if quiz.cover_image}
						<img
							src="/api/v1/storage/download/{quiz.cover_image}"
							alt="user provided"
							loading="lazy"
							class="shrink-0 max-w-full max-h-full absolute rounded"
						/>
					{/if}
				</div>
				<div class="my-auto mx-auto max-h-full overflow-hidden">
					<p class="text-xl text-center">{@html quiz.title}</p>
					<p class="text-sm text-center text-clip overflow-hidden">
						{@html quiz.description ?? ''}
					</p>
				</div>
				<div class="flex justify-center">
					<p class="m-auto">Questions: {quiz.questions.length}</p>
				</div>
			</div>
			<div class="flex w-full">
				<GreenButton href="/view/{quiz.id}?mod=true&autoExpand=true&autoReturn=true"
					>View</GreenButton
				>
			</div>
		</div>
	{/each}
</div>
<div class="flex">
	<div class="grid grid-cols-3 mx-auto">
		<GreenButton disabled={data.page === '1'} href="/moderation?page={parseInt(data.page) + 1}"
			>Previous Page</GreenButton
		>
		<p class="m-auto">Page {data.page}</p>
		<GreenButton
			disabled={data.quizzes.length !== 20}
			href="/moderation?page={parseInt(data.page) - 1}">Next Page</GreenButton
		>
	</div>
</div>
