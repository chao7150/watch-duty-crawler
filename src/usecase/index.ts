import type { Site, Page } from "../domain.js";
import type {
	ISiteRepository,
	ISiteFetcher,
	IPageRepository,
} from "./interfaces.js";
import type { Result } from "ts-results-es";

export const adminAddSite = (repository: ISiteRepository, site: Site): void => {
	repository.add(site);
};

export const crawlerFetchSite = async (
	siteFetcher: ISiteFetcher,
	repository: IPageRepository,
	site: Site,
): Promise<Result<void, { code: string }>> => {
	return (await siteFetcher.fetch(site)).map((data) =>
		data.forEach((page) => repository.upsert(site, page)),
	);
};

export const userSearchPage = (
	repository: IPageRepository,
	q: string,
): Promise<Result<Page[], { code: string }>> => {
	return repository.findByQuery(q);
};
