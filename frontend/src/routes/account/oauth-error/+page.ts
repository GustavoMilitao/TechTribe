// SPDX-FileCopyrightText: 2023 
//
// SPDX-License-Identifier: MPL-2.0

export function load({ url }) {
	const error = url.searchParams.get('error');
	return {
		error
	};
}
