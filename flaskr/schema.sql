drop table if exists entries;
create table guests (
	id integer primary key autoincrement,
	name string not null
);