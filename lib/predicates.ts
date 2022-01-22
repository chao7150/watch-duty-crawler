import type { YahooProgram, YahooResponse } from "./types";

const isNumber = (value: unknown): value is number => typeof value === "number";
const isString = (value: unknown): value is string => typeof value === "string";
const isUndefined = (value: unknown): value is undefined =>
  typeof value === "undefined";
const isObject = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value);
const isUnion =
  (unionChecks: ((value: unknown) => boolean)[]) =>
  (value: unknown): boolean =>
    unionChecks.reduce((s: boolean, isT) => s || isT(value), false);
type ArrayCheckOption = "all" | "first";
const isArray =
  <T>(
    childCheckFn:
      | ((value: unknown) => value is T)
      | ((value: unknown) => boolean),
    checkOption: ArrayCheckOption = "all"
  ) =>
  (array: unknown): boolean =>
    Array.isArray(array) &&
    (checkOption === "all"
      ? ((array) => {
          for (const val of array) {
            if (!childCheckFn(val)) return false;
          }
          return true;
        })(array)
      : typeof array[0] === "undefined" || childCheckFn(array[0]));

export const isYahooProgram = (arg_0: unknown): arg_0 is YahooProgram =>
  isObject(arg_0) &&
  "broadCastEndDate" in arg_0 &&
  isNumber(arg_0["broadCastEndDate"]) &&
  "broadCastStartDate" in arg_0 &&
  isNumber(arg_0["broadCastStartDate"]) &&
  "broadCasterName" in arg_0 &&
  isString(arg_0["broadCasterName"]) &&
  "descriptions" in arg_0 &&
  isString(arg_0["descriptions"]) &&
  ((arg_1: unknown): boolean =>
    isUnion([
      isUndefined,
      (arg_2: unknown): boolean => isArray(isString)(arg_2),
    ])(arg_1))(arg_0["element"]) &&
  "majorGenreId" in arg_0 &&
  ((arg_1: unknown): boolean => isArray(isString)(arg_1))(
    arg_0["majorGenreId"]
  ) &&
  "minorGenreName" in arg_0 &&
  ((arg_1: unknown): boolean => isArray(isString)(arg_1))(
    arg_0["minorGenreName"]
  ) &&
  "programTitle" in arg_0 &&
  isString(arg_0["programTitle"]) &&
  "relationUrlsContainer" in arg_0 &&
  isString(arg_0["relationUrlsContainer"]) &&
  "serviceName" in arg_0 &&
  isString(arg_0["serviceName"]) &&
  "summary" in arg_0 &&
  isString(arg_0["summary"]) &&
  "title" in arg_0 &&
  isString(arg_0["title"]);
export function assertIsYahooProgram(
  value: unknown
): asserts value is YahooProgram {
  if (!isYahooProgram(value))
    throw new TypeError(`value must be YahooProgram but received ${value}`);
}
export const isYahooResponse = (arg_0: unknown): arg_0 is YahooResponse =>
  isObject(arg_0) &&
  "ResultSet" in arg_0 &&
  ((arg_1: unknown): boolean =>
    isObject(arg_1) &&
    "Result" in arg_1 &&
    ((arg_2: unknown): boolean => isArray(isYahooProgram)(arg_2))(
      arg_1["Result"]
    ) &&
    "attribute" in arg_1 &&
    ((arg_2: unknown): boolean =>
      isObject(arg_2) &&
      "firstResultPosition" in arg_2 &&
      isNumber(arg_2["firstResultPosition"]) &&
      "totalResultsAvailable" in arg_2 &&
      isNumber(arg_2["totalResultsAvailable"]) &&
      "totalResultsReturned" in arg_2 &&
      isNumber(arg_2["totalResultsReturned"]))(arg_1["attribute"]))(
    arg_0["ResultSet"]
  );
export function assertIsYahooResponse(
  value: unknown
): asserts value is YahooResponse {
  if (!isYahooResponse(value))
    throw new TypeError(`value must be YahooResponse but received ${value}`);
}
