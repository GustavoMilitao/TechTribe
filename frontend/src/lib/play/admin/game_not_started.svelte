<!--
SPDX-FileCopyrightText: 2023 

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import ControllerCodeDisplay from '$lib/components/controller/code.svelte';
	import { getLocalization } from '$lib/i18n';
	import GrayButton from '$lib/components/buttons/gray.svelte';

	export let game_pin: string;
	export let players;
	export let socket;
	export let cqc_code: string;

	const { t } = getLocalization();

	if (cqc_code === 'null') {
		cqc_code = null;
	}
</script>

<div class="w-full">
	<div class="grid grid-cols-3 mt-12">
		<div class="flex justify-center">
		</div>
		{#if cqc_code}
			<div class="m-auto">
				<div class="flex justify-center my-4">
					<p class="m-auto text-2xl">
						{$t('play_page.players_waiting', {
							count: players.length ?? 0
						})}
					</p>
				</div>
				<div class="flex-col flex justify-center">
					<p class="mx-auto">{$t('play_page.join_by_entering_code')}</p>
					<ControllerCodeDisplay code={cqc_code} />
				</div>
			</div>
		{:else}
			<div class="flex justify-center">
				<p class="m-auto text-2xl">
					{$t('play_page.players_waiting', {
						count: players.length ?? 0
					})}
				</p>
			</div>
		{/if}
	</div>
	<p class="text-3xl text-center">
		{$t('words.pin')}: <span class="select-all">{game_pin}</span>
	</p>
	<div class="flex justify-center w-full mt-4">
		<div>
			<GrayButton
				disabled={players.length < 1}
				on:click={() => {
					socket.emit('start_game', '');
				}}
				>{$t('admin_page.start_game')}
			</GrayButton>
		</div>
	</div>
	<div class="flex flex-row w-full mt-4 px-10 flex-wrap">
		{#if players.length > 0}
			{#each players as player}
				<div class="p-2 m-2 border-2 border-[#B07156] rounded">
					<span
						class="text-lg">{player.username}</span
					>
					<!--					<button>{$t('words.kick')}</button>-->
				</div>
			{/each}
		{/if}
	</div>
</div>
