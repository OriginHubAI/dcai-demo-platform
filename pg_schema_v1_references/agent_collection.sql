create table agent_collection
(
    id            varchar(36)           not null
        primary key,
    type          varchar(36),
    collection_id varchar(36),
    kb_id         varchar(128),
    del_flag      boolean default false not null,
    updated_at    timestamp with time zone,
    created_at    timestamp with time zone,
    agent_id      varchar(36),
    constraint unique_agent_id_collection_id_kb_id
        unique (agent_id, collection_id, kb_id)
);

alter table agent_collection
    owner to myscale_kb_backend;

create index agent_collection_agent_id_2d7db3f9
    on agent_collection (agent_id);

create index agent_collection_agent_id_2d7db3f9_like
    on agent_collection (agent_id varchar_pattern_ops);

create index agent_collection_id_251550d4_like
    on agent_collection (id varchar_pattern_ops);
