import type { ColumnType, Generated } from "kysely";

export interface Database {
	sites: SiteTable;
	pages: PageTable;
}

export interface SiteTable {
	id: Generated<number>;
	title: string;
	rootUrl: string;
	created_at: ColumnType<Date, string | undefined, never>;
}

export interface PageTable {
	id: Generated<number>;
	siteId: number;
	relativePath: string;
	title: string;
	content: string;
	noindex: boolean;
	created_at: ColumnType<Date, string | undefined, never>;
}
