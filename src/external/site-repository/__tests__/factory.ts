import type { Site } from "../../../domain.js";
import type { ISiteRepository } from "../../../usecase/interfaces.js";

export const createMockService = (): ISiteRepository => {
	return {
		add: (_site: Site) => {
			// Mock implementation
		},
	};
};
