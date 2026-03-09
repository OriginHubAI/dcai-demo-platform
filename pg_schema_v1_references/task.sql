create table task
(
    status            varchar(20)              not null,
    id                varchar(255)             not null
        primary key,
    pipeline_id       varchar(255),
    name              varchar(255),
    description       text,
    created_at        timestamp with time zone not null,
    updated_at        timestamp with time zone not null,
    started_at        timestamp with time zone,
    completed_at      timestamp with time zone,
    del_flag          boolean                  not null,
    dataset_ids       jsonb                    not null,
    extend_rules      jsonb                    not null,
    notification      jsonb                    not null,
    pipeline_config   jsonb                    not null,
    schedule_config   jsonb                    not null,
    template_id       varchar(255),
    progress          double precision         not null,
    user_id           varchar(255),
    task_type         varchar(50),
    chat_enable       boolean                  not null,
    api_key           varchar(255) default ''::character varying,
    error_message     text,
    pipeline_config_a jsonb                    not null,
    pipeline_config_v jsonb                    not null
);

alter table task
    owner to myscale_kb_backend;

create index idx_task_created_at
    on task (created_at);

create index idx_task_del_flag
    on task (del_flag);

create index idx_task_name
    on task (name);

create index idx_task_pipeline_id
    on task (pipeline_id);

create index idx_task_updated_at
    on task (updated_at);

create index idx_task_user_id
    on task (user_id);

create index task_id_290f60eb_like
    on task (id varchar_pattern_ops);