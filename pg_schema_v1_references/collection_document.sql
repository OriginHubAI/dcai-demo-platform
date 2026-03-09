create table collection_document
(
    id            varchar(36)           not null
        primary key,
    kb_type       varchar(36),
    kb_id         varchar(128),
    doc_id        bigint,
    del_flag      boolean default false not null,
    updated_at    timestamp with time zone,
    created_at    timestamp with time zone,
    collection_id varchar(36)
);

alter table collection_document
    owner to myscale_kb_backend;

create index collection_document_collection_id_95459599
    on collection_document (collection_id);

create index collection_document_collection_id_95459599_like
    on collection_document (collection_id varchar_pattern_ops);

create index collection_document_id_8a360cce_like
    on collection_document (id varchar_pattern_ops);

create index collection_document_kb_type_kb_id_doc_id_747d4332_idx
    on collection_document (kb_type, kb_id, doc_id);
