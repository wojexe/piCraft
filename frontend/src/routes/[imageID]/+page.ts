import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load = (({ params }) => {
	if (params.imageID === "world") {
		return {
			title: "Hello world!"
		}
	}

	throw error(404, 'Not found');
}) satisfies PageLoad;
