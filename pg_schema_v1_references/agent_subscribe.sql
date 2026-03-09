create table agent_subscribe
(
    id         varchar(36)           not null
        primary key,
    del_flag   boolean default false not null,
    updated_at timestamp with time zone,
    created_at timestamp with time zone,
    agent_id   varchar(36)
        constraint agent_subscribe_agent_id_5cc71479_fk_agent_id
            references agent
            deferrable initially deferred,
    user_id    varchar(36)
);

alter table agent_subscribe
    owner to myscale_kb_backend;

create index agent_subscribe_agent_id_5cc71479
    on agent_subscribe (agent_id);

create index agent_subscribe_agent_id_5cc71479_like
    on agent_subscribe (agent_id varchar_pattern_ops);

create index agent_subscribe_id_02fb2fb2_like
    on agent_subscribe (id varchar_pattern_ops);

create index agent_subscribe_user_id_b6d08b02
    on agent_subscribe (user_id);

create index agent_subscribe_user_id_b6d08b02_like
    on agent_subscribe (user_id varchar_pattern_ops);

