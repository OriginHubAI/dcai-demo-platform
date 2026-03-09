create table adapter_internal_task_mapping
(
    external_task_id varchar(128)             not null,
    df_task_id       uuid                     not null
        primary key,
    status           varchar(32)              not null,
    error_message    text,
    created_at       timestamp with time zone not null,
    updated_at       timestamp with time zone not null,
    completed_at     timestamp with time zone
);

alter table adapter_internal_task_mapping
    owner to myscale_kb_backend;

create index adapter_internal_task_mapping_external_task_id_7f34380d
    on adapter_internal_task_mapping (external_task_id);

create index adapter_internal_task_mapping_external_task_id_7f34380d_like
    on adapter_internal_task_mapping (external_task_id varchar_pattern_ops);

create index idx_int_task_ext_status
    on adapter_internal_task_mapping (external_task_id, status);

create index idx_int_task_status_created
    on adapter_internal_task_mapping (status asc, created_at desc);
