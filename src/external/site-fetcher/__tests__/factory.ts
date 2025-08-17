import { Ok, type Result } from "ts-results-es";
import type { Site, Page } from "../../../domain.js";
import type { ISiteFetcher } from "../../../usecase/interfaces.js";

export const createMockService = (): ISiteFetcher => {
	return {
		fetch: async (
			_site: Site,
		): Promise<Result<Array<Page>, { code: string }>> => {
			return Ok([
				{
					title: "Mock Page 1",
					relativePath: "/",
					content: "This is a mock page.",
					noindex: false,
				},
				{
					title: "Mock Page 2",
					relativePath: "/mock-page-2",
					content: "This is another mock page.",
					noindex: false,
				},
			]);
		},
	};
};
