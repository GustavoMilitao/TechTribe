<!--
SPDX-FileCopyrightText: 2023 

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import GreenButton from '$lib/components/buttons/green.svelte';
	import GrayButton from '$lib/components/buttons/gray.svelte';

	export let autoReturn = false;
	export let quiz_id: string;
	let mod_rating: number | undefined;

	const submit = async () => {
		const res = await fetch(`/api/v1/moderation/rating/set/${quiz_id}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ rating: mod_rating })
		});
		if (res.ok && autoReturn) {
			window.history.back();
		}
		if (!res.ok) {
			alert('Setting rating failed');
		}
	};
</script>

<div class="rounded border-2 border-[#B07156] flex flex-col w-fit gap-2 p-2">
	<div class:opacity-50={mod_rating !== null && mod_rating !== undefined} class="transition">
		<GreenButton on:click={() => (mod_rating = null)}>Not Checked</GreenButton>
	</div>
	<div class:opacity-50={mod_rating !== 0 && mod_rating !== undefined} class="transition">
		<GreenButton on:click={() => (mod_rating = 0)}>Ok</GreenButton>
	</div>
	<div class:opacity-50={mod_rating !== 1 && mod_rating !== undefined} class="transition">
		<GreenButton on:click={() => (mod_rating = 1)}>Attention</GreenButton>
	</div>
	<div class:opacity-50={mod_rating !== 2 && mod_rating !== undefined} class="transition">
		<GreenButton on:click={() => (mod_rating = 2)}>NFSW</GreenButton>
	</div>
	<div class:opacity-50={mod_rating !== 3 && mod_rating !== undefined} class="transition">
		<GreenButton on:click={() => (mod_rating = 3)}>Plausibility Checked</GreenButton>
	</div>
	<div class:opacity-50={mod_rating !== 4 && mod_rating !== undefined} class="transition">
		<GreenButton on:click={() => (mod_rating = 4)}>Fact Checked</GreenButton>
	</div>
	<div class:opacity-50={mod_rating !== 5 && mod_rating !== undefined} class="transition">
		<GreenButton on:click={() => (mod_rating = 5)}>Exceptional</GreenButton>
	</div>
	<GrayButton on:click={submit} disabled={mod_rating === undefined}>Submit</GrayButton>
</div>
