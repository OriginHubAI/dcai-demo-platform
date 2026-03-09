create table agent
(
    id          varchar(36)                not null
        primary key,
    agent_id    varchar(36),
    author      varchar(128) default NULL::character varying,
    title       varchar(200) default NULL::character varying,
    prompt      jsonb        default 'null'::jsonb,
    description text,
    questions   jsonb        default 'null'::jsonb,
    llm         jsonb        default 'null'::jsonb,
    tools       jsonb        default 'null'::jsonb,
    cover_url   varchar(256) default NULL::character varying,
    type        varchar(32)  default 'personal'::character varying,
    pub_date    date,
    "order"     integer      default 0     not null,
    total       integer      default 0,
    extension   jsonb,
    del_flag    boolean      default false not null,
    updated_at  timestamp with time zone,
    created_at  timestamp with time zone,
    user_id     varchar(36)
);

alter table agent
    owner to myscale_kb_backend;

create index agent_id_5fda41bf_like
    on agent (id varchar_pattern_ops);

create index agent_user_id_1ff77acc
    on agent (user_id);

create index agent_user_id_1ff77acc_like
    on agent (user_id varchar_pattern_ops);

