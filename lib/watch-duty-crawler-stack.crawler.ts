import { Handler } from "aws-lambda";
import fetch, { RequestInit } from "node-fetch";
import {
  assertIsYahooProgram,
  assertIsYahooResponse,
  isYahooResponse,
} from "./predicates";
import { YahooResponse } from "./types";
import set from "date-fns/set";

const delay = (delayMs: number) =>
  new Promise((resolve) => {
    setTimeout(resolve, delayMs);
  });

const createFetchArgs = ({
  start,
  broadCastStartDate,
  broadCastStartDateEnd,
}: {
  start: number;
  broadCastStartDate: number;
  broadCastStartDateEnd: number;
}): RequestInit => {
  const requestBody = {
    query: "",
    siTypeId: "3",
    majorGenreId: "0x7",
    areaId: "23",
    duration: "",
    element: "",
    broadCastStartDate,
    broadCastStartDateEnd,
    start,
    results: 10,
    sort: "+broadCastStartDate",
  };
  return {
    method: "POST",
    headers: {
      "User-Agent": "chao7150",
      accept: "application/json, text/plain, */*",
      "accept-language": "ja,en-US;q=0.9,en;q=0.8",
      "cache-control": "no-cache",
      "content-type": "application/json",
      pragma: "no-cache",
      "sec-ch-ua": '"Chromium";v="96", " Not A;Brand";v="99"',
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": '"Linux"',
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "same-origin",
      "target-path": "/TVWebService/V2/contents",
      "Referrer-Policy": "strict-origin-when-cross-origin",
    },
    body: JSON.stringify(requestBody),
  };
};

const ONE_DAY_SEC = 60 * 60 * 24;

const fetchYahooPrograms = async (
  fetchArgs: RequestInit
): Promise<YahooResponse> => {
  const response = await fetch(
    "https://tv.yahoo.co.jp/api/adapter?_api=mindsSiQuery",
    fetchArgs
  );
  const data = await response.json();
  data.ResultSet.Result.map(assertIsYahooProgram);
  assertIsYahooResponse(data);
  console.log(data);
  return data;
};

export const handler: Handler = async () => {
  const nowSec = Math.floor(new Date().getTime() / 1000);
  const broadCastStartDate = nowSec + 6 * ONE_DAY_SEC;
  const broadCastStartDateEnd = broadCastStartDate + ONE_DAY_SEC;

  const yahooResponse = await fetchYahooPrograms(
    createFetchArgs({ start: 0, broadCastStartDate, broadCastStartDateEnd })
  );
  const total = yahooResponse.ResultSet.attribute.totalResultsAvailable;
  const yahooPrograms = yahooResponse.ResultSet.Result;

  const moreFetchCount = Math.floor((total - 1) / 10);
  for (let i = 1; i <= moreFetchCount; i++) {
    await delay(10 * 1000);
    const yahooResponse = await fetchYahooPrograms(
      createFetchArgs({
        start: i * 10,
        broadCastStartDate,
        broadCastStartDateEnd,
      })
    );
    yahooPrograms.push(...yahooResponse.ResultSet.Result);
  }
  console.log(yahooPrograms.map((program) => program.title));
};
