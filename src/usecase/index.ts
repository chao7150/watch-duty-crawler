import type { Site, Page } from "../domain.js";
import type { ISiteRepository, ISiteFetcher, IPageRepository } from "./interfaces.js";

export const adminAddSite = (repository: ISiteRepository, site: Site): void => {
  repository.add(site);
};

export const crawlerFetchSite = async (
  siteFetcher: ISiteFetcher,
  repository: IPageRepository,
  site: Site
): Promise<void> => {
  const data = await siteFetcher.fetch(site);
  data.forEach((page) => {
    repository.upsert(site, page);
  });
};

export const userSearchPage = (
  repository: IPageRepository,
  q: string
): Page[] => {
  return repository.findByQuery(q);
};
