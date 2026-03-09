create table kps_callback
(
    id                 varchar(255)             not null
        primary key,
    tenant_id          varchar(255),
    dataset_id         varchar(255),
    task_id            varchar(255),
    result             jsonb                    not null,
    "failureMsgFormat" text,
    delivery           boolean                  not null,
    resp               jsonb                    not null,
    created_at         timestamp with time zone not null,
    updated_at         timestamp with time zone not null
);

alter table kps_callback
    owner to myscale_kb_backend;

create index idx_dataset_id
    on kps_callback (dataset_id);

create index idx_kps_callback_created_at
    on kps_callback (created_at);

create index idx_kps_callback_updated_at
    on kps_callback (updated_at);

create index kps_callback_id_cda319a7_like
    on kps_callback (id varchar_pattern_ops);

