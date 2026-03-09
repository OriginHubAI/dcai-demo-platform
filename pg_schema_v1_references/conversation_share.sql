create table conversation_share
(
    id                 varchar(36)                not null
        primary key,
    title              varchar(200) default NULL::character varying,
    agent_id           varchar(36)  default NULL::character varying,
    collection_and_kbs jsonb        default 'null'::jsonb,
    knowledge_scopes   jsonb        default 'null'::jsonb,
    model              varchar(64)  default NULL::character varying,
    content            jsonb        default 'null'::jsonb,
    num                integer,
    del_flag           boolean      default false not null,
    updated_at         timestamp with time zone,
    created_at         timestamp with time zone,
    conversation_id    varchar(36),
    user_id            varchar(36)
);

alter table conversation_share
    owner to myscale_kb_backend;

create index conversation_share_conversation_id_0c534976
    on conversation_share (conversation_id);

create index conversation_share_conversation_id_0c534976_like
    on conversation_share (conversation_id varchar_pattern_ops);

create index conversation_share_id_12d16513_like
    on conversation_share (id varchar_pattern_ops);

create index conversation_share_user_id_aaa84001
    on conversation_share (user_id);

create index conversation_share_user_id_aaa84001_like
    on conversation_share (user_id varchar_pattern_ops);

