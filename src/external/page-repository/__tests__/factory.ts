import { Ok } from "ts-results-es";
import type { Site, Page } from "../../../domain.js";
import type { IPageRepository } from "../../../usecase/interfaces.js";

export const createMockService = (): IPageRepository => {
	return {
		upsert: async (_site: Site, _data: Page) => {
			// Mock implementation
			return Ok(undefined);
		},
		findByQuery: async (_query: string) => {
			// Mock implementation
			return Ok([]);
		},
	};
};
