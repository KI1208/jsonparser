drop table if exists file_entries;
create table file_entries (
  id integer primary key autoincrement,
  filename string not null,
  desc string,
  created string
);
