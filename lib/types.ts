export type YahooProgram = {
  broadCastEndDate: number;
  broadCastStartDate: number;
  broadCasterName: string;
  /**
   * 作品説明文
   */
  descriptions: string;
  element: string[] | undefined;
  majorGenreId: string[];
  minorGenreName: string[];
  programTitle: string;
  relationUrlsContainer: string;
  serviceName: string;
  /**
   * 話数説明文
   */
  summary: string;
  /**
   * 話数タイトル
   */
  title: string;
};

export type YahooResponse = {
  ResultSet: {
    Result: YahooProgram[];
    attribute: {
      firstResultPosition: number;
      totalResultsAvailable: number;
      totalResultsReturned: number;
    };
  };
};
