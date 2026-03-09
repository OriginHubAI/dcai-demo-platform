create table django_celery_beat_periodictasks
(
    ident       smallint                 not null
        primary key,
    last_update timestamp with time zone not null
);

alter table django_celery_beat_periodictasks
    owner to myscale_kb_backend;

