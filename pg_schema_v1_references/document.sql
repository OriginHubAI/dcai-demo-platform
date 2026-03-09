create table document
(
    id           varchar(36)           not null
        primary key,
    kb_type      varchar(36),
    kb_id        varchar(128),
    doc_id       bigint,
    task_type    varchar,
    task_id      varchar(36),
    task_status  varchar(32),
    error        jsonb,
    filename     varchar(512),
    object_path  varchar(512),
    del_flag     boolean default false not null,
    updated_at   timestamp with time zone,
    created_at   timestamp with time zone,
    user_id      varchar(36),
    chunks_count integer               not null,
    source_url   varchar(1024),
    content_hash varchar(64),
    move_params  jsonb,
    tags         jsonb                 not null
);

alter table document
    owner to myscale_kb_backend;

create index document_id_77928f29_like
    on document (id varchar_pattern_ops);

create index document_kb_type_kb_id_doc_id_e05febbe_idx
    on document (kb_type, kb_id, doc_id);

create index document_task_status_b75b8079
    on document (task_status);

create index document_task_status_b75b8079_like
    on document (task_status varchar_pattern_ops);

create index document_user_id_9e7ccb71
    on document (user_id);

create index document_user_id_9e7ccb71_like
    on document (user_id varchar_pattern_ops);
