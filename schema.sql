drop table if exists notes;
create table notes (
	id integer primary key autoincrement,
	title text not null,
	content text not null,
	datetime timestamp not null
);