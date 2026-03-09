create table conversation
(
    id                 varchar(36)                 not null
        primary key,
    title              varchar(200)  default NULL::character varying,
    agent_id           varchar(36)   default NULL::character varying,
    collection_and_kbs jsonb         default 'null'::jsonb,
    knowledge_scopes   jsonb         default 'null'::jsonb,
    type               varchar(32)   default NULL::character varying,
    model              varchar(64)   default NULL::character varying,
    del_flag           boolean       default false not null,
    last_used_at       timestamp with time zone,
    is_named           boolean       default false not null,
    is_api             boolean       default false not null,
    source             varchar(1024) default NULL::character varying,
    updated_at         timestamp with time zone,
    created_at         timestamp with time zone,
    user_id            varchar(36),
    share_id           varchar(36)   default NULL::character varying
);

alter table conversation
    owner to myscale_kb_backend;

create index conversation_id_8d8250b9_like
    on conversation (id varchar_pattern_ops);

create index conversation_share_id_ca2445a0
    on conversation (share_id);

create index conversation_share_id_ca2445a0_like
    on conversation (share_id varchar_pattern_ops);

create index conversation_user_id_cc13e167
    on conversation (user_id);

create index conversation_user_id_cc13e167_like
    on conversation (user_id varchar_pattern_ops);
