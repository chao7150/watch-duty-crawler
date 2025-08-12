export type Site = {
	title: string;
	rootUrl: string;
};

export type Page = {
	relativePath: string;
	title: string;
	content: string;
	noindex: boolean;
};
