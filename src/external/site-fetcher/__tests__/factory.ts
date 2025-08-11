import type { Site, Page } from "../../../domain.js";
import type { ISiteFetcher } from "../../../usecase/interfaces.js";

export const createMockService = (): ISiteFetcher => {
  return {
    fetch: async (_site: Site): Promise<Array<Page>> => {
      return [
        {
          title: "Mock Page 1",
          relativePath: "/",
          content: "This is a mock page.",
        },
        {
          title: "Mock Page 2",
          relativePath: "/mock-page-2",
          content: "This is another mock page.",
        },
      ];
    },
  };
};
