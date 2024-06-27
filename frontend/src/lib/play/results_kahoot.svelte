<!--
SPDX-FileCopyrightText: 2023 

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	export let scores;

	export let question_results: Array<{
		username: string;
		answer: string;
		right: boolean;
		time_taken: number;
		score: number;
	}>;

	function sortObjectbyValue(obj) {
		const ret = {};
		Object.keys(obj)
			.sort((a, b) => obj[b] - obj[a])
			.forEach((s) => (ret[s] = obj[s]));
		return ret;
	}

	export let username;
	let score_by_username = {};

	if (JSON.stringify(scores) === '{}') {
		for (const i of question_results) {
			scores[i.username] = 0;
		}
	}

	$: console.log(score_by_username, scores, 'dieter');
	for (const i of question_results) {
		score_by_username[i.username] = i.score;
	}

	$: scores = sortObjectbyValue(scores);

	const do_sth = () => {
		for (const i of Object.keys(score_by_username)) {
			scores[i] = (score_by_username[i] ?? 0) + (scores[i] ?? 0);
		}
		scores = scores;
	};

	const getJoke = async () => {
		const joke_resp = await fetch('https://v2.jokeapi.dev/joke/Any?lang=pt&type=twopart');
		const joke = await joke_resp.json();
		return joke;
	}

	do_sth();
</script>

<div>
	<div class="flex justify-center mb-8">
		<div class="m-auto flex flex-col">
			<p class="p-4 bg-black bg-opacity-40 rounded-lg text-2xl">
				+{score_by_username[username] ?? '0'}
			</p>
			<p>Pontos totais: {scores[username] ?? '0'}</p>
		</div>
	</div>
	{#await getJoke()}
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
	{:then joke} 
	<div class="flex justify-center mb-8">			
		<div class="m-auto flex flex-col">
			<h2 class="text-center text-xl">PIADOCA DO INTERVALO:</h2>
			<h2 class="text-xl">
				Pergunta: {joke["setup"]}
			</h2>
			<p class="text-xl"> Resposta: {joke["delivery"]}</p>
		</div>
	</div>
	{/await}
</div>
