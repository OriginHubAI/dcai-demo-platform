create table dataset
(
    id                varchar(255)             not null
        primary key,
    parent_dataset_id varchar(255),
    source_task_id    varchar(255),
    user_id           varchar(255),
    name              varchar(255),
    description       text,
    path              varchar(255),
    domain            varchar(255),
    record_count      integer                  not null,
    dataset_metadata  jsonb,
    del_flag          boolean                  not null,
    created_at        timestamp with time zone not null,
    updated_at        timestamp with time zone not null,
    tenant_config     jsonb,
    third_dataset_raw jsonb
);

alter table dataset
    owner to myscale_kb_backend;

create index dataset_id_cc80b040_like
    on dataset (id varchar_pattern_ops);

