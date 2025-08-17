import { Err, Ok } from "ts-results-es";
import { db } from "../../infra/postgres/insntance.js";
import type { ISiteRepository } from "../../usecase/interfaces.js";

export const service: ISiteRepository = {
	add: async (site) => {
		try {
			await db.insertInto("sites").values(site).execute();
			return new Ok(undefined);
		} catch (error) {
			console.error(error);
			return new Err({ code: "UNEXPECTED_DB_ERROR" });
		}
	},
	getAll: async () => {
		try {
			const sites = await db.selectFrom("sites").selectAll().execute();
			return new Ok(sites);
		} catch (error) {
			console.error(error);
			return new Err({ code: "UNEXPECTED_DB_ERROR" });
		}
	},
};
