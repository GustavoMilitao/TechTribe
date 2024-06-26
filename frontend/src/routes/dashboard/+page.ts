// SPDX-FileCopyrightText: 2023 
//
// SPDX-License-Identifier: MPL-2.0

import type { PageLoad } from './$types';

export const load = (async ({ fetch }) => {
	const quiz_res = await fetch('/api/v1/quiz/list?page_size=100');
	const quizzes = await quiz_res.json();
	return {
		quizzes
	};
}) satisfies PageLoad;
