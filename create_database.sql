create tabel memory(id integer primary key,
                            user_id integer not null,
                            predicate text not null,
                            object text not null,
                            num real,
                            finished timestamp not null);
