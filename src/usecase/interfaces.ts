import type { Site, Page } from "../domain.js";

export interface ISiteRepository {
	add(site: Site): Promise<void>;
	getAll(): Promise<Array<Site>>;
}

export interface IPageRepository {
	upsert(site: Site, data: Page): Promise<void>;
	findByQuery(query: string): Array<Page>;
}

export interface ISiteFetcher {
	fetch(site: Site): Promise<Array<Page>>;
}
