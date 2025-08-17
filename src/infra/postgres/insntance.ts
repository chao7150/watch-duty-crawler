import type { Database } from "./schema.js";
import { Pool } from "pg";
import { Kysely, PostgresDialect } from "kysely";

const dialect = new PostgresDialect({
	pool: new Pool({
		database: "test",
		host: "localhost",
		user: "admin",
		port: 5434,
		max: 10,
	}),
});

export const db: Kysely<Database> = new Kysely<Database>({
	dialect,
});
