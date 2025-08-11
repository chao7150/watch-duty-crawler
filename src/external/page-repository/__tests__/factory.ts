import type { Site, Page } from "../../../domain.js";
import type { IPageRepository } from "../../../usecase/interfaces.js";

export const createMockService = (): IPageRepository => {
  return {
    upsert: (_site: Site, _data: Page) => {
      // Mock implementation
    },
    findByQuery: (_query: string) => {
      // Mock implementation
      return [];
    },
  };
};
