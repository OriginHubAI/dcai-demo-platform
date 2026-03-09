create table file
(
    id            varchar(64)              not null
        primary key,
    dataset_id    varchar(64)              not null,
    user_id       varchar(64)              not null,
    name          varchar(255)             not null,
    description   text,
    path          varchar(1024)            not null,
    mime_type     varchar(128)             not null,
    size          bigint                   not null,
    file_metadata jsonb                    not null,
    del_flag      boolean                  not null,
    created_at    timestamp with time zone not null,
    updated_at    timestamp with time zone not null,
    constraint file_user_id_dataset_id_name_path_5b0118bd_uniq
        unique (user_id, dataset_id, name, path)
);

alter table file
    owner to myscale_kb_backend;

create index file_id_51b3dc25_like
    on file (id varchar_pattern_ops);

