import { Ok } from "ts-results-es";
import type { Site } from "../../../domain.js";
import type { ISiteRepository } from "../../../usecase/interfaces.js";

export const createMockService = (): ISiteRepository => {
	return {
		add: async (_site: Site) => {
			// Mock implementation
			return Ok(undefined);
		},
		getAll: async () => {
			return Ok([
				{
					title: "薫る花は凛と咲く",
					rootUrl: "https://kaoruhana-anime.com",
				},
				{
					title: "ポケットモンスター(2023)",
					rootUrl: "https://www.tv-tokyo.co.jp/anime/pocketmonster2023/",
				},
			]);
		},
	};
};
