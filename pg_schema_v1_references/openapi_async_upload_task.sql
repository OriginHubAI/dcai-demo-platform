create table openapi_async_upload_task
(
    id                  varchar(36)              not null
        primary key,
    user_id             varchar(36)              not null,
    kb_id               varchar(128)             not null,
    task_name           varchar(256)             not null,
    status              varchar(20)              not null,
    total_files         integer                  not null,
    processed_files     integer                  not null,
    success_files       integer                  not null,
    failed_files        integer                  not null,
    file_info           jsonb                    not null,
    error_message       text,
    error_details       jsonb,
    progress_percentage double precision         not null,
    current_step        varchar(128)             not null,
    created_at          timestamp with time zone not null,
    updated_at          timestamp with time zone not null,
    started_at          timestamp with time zone,
    completed_at        timestamp with time zone,
    celery_task_id      varchar(128)
);

alter table openapi_async_upload_task
    owner to myscale_kb_backend;

create index openapi_asy_celery__0263e6_idx
    on openapi_async_upload_task (celery_task_id);

create index openapi_asy_status_2e6807_idx
    on openapi_async_upload_task (status asc, created_at desc);

create index openapi_asy_user_id_a17b48_idx
    on openapi_async_upload_task (user_id asc, created_at desc);

create index openapi_async_upload_task_id_bf824c34_like
    on openapi_async_upload_task (id varchar_pattern_ops);

