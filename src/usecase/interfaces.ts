import type { Site, Page } from "../domain.js";

export interface ISiteRepository {
  add(site: Site): void;
}

export interface IPageRepository {
  upsert(site: Site, data: Page): void;
  findByQuery(query: string): Array<Page>;
}

export interface ISiteFetcher {
  fetch(site: Site): Promise<Array<Page>>;
}