import type { Result } from "ts-results-es";
import type { Site, Page } from "../domain.js";

export interface ISiteRepository {
	add(site: Site): Promise<Result<void, { code: string }>>;
	getAll(): Promise<Result<Array<Site>, { code: string }>>;
}

export interface IPageRepository {
	upsert(site: Site, data: Page): Promise<Result<void, { code: string }>>;
	findByQuery(query: string): Promise<Result<Array<Page>, { code: string }>>;
}

export interface ISiteFetcher {
	fetch(site: Site): Promise<Result<Array<Page>, { code: string }>>;
}
