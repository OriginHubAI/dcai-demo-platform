create table adapter_external_task
(
    external_task_id varchar(128)             not null
        primary key,
    status           varchar(32)              not null,
    callback_status  varchar(32)              not null,
    error_message    text,
    callback_error   text,
    created_at       timestamp with time zone not null,
    updated_at       timestamp with time zone not null,
    completed_at     timestamp with time zone,
    callback_at      timestamp with time zone
);

alter table adapter_external_task
    owner to myscale_kb_backend;

create index adapter_external_task_external_task_id_96f37466_like
    on adapter_external_task (external_task_id varchar_pattern_ops);

create index idx_ext_task_callback
    on adapter_external_task (callback_status asc, callback_at desc);

create index idx_ext_task_status_created
    on adapter_external_task (status asc, created_at desc);
