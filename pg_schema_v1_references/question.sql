create table question
(
    id              varchar(36)                not null
        primary key,
    answer          jsonb,
    is_like         boolean,
    stream          jsonb        default 'null'::jsonb,
    model           varchar(64)  default NULL::character varying,
    input_tokens    integer,
    output_tokens   integer,
    del_flag        boolean      default false not null,
    is_stop         boolean      default false not null,
    source          varchar(512) default NULL::character varying,
    updated_at      timestamp with time zone,
    created_at      timestamp with time zone,
    conversation_id varchar(36),
    message         jsonb        default 'null'::jsonb,
    api_key_id      integer
);

alter table question
    owner to myscale_kb_backend;

create index question_api_key_id_55d00654
    on question (api_key_id);

create index question_conversation_id_99cfdb8a
    on question (conversation_id);

create index question_conversation_id_99cfdb8a_like
    on question (conversation_id varchar_pattern_ops);

create index question_id_9b93cfd3_like
    on question (id varchar_pattern_ops);
