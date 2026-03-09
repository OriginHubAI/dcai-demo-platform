create table agent_tools
(
    id                       varchar(36)           not null
        primary key,
    name                     varchar               not null,
    url                      varchar,
    openapi_json_path        varchar,
    auth_type                varchar,
    username_password_base64 varchar,
    token                    varchar,
    api_key                  varchar,
    custom_header            varchar,
    endpoints                jsonb,
    description              text,
    checked                  boolean default false not null,
    del_flag                 boolean default false not null,
    updated_at               timestamp with time zone,
    created_at               timestamp with time zone,
    agent_id                 varchar(36),
    user_id                  varchar(36)
);

alter table agent_tools
    owner to myscale_kb_backend;

create index agent_tools_agent_id_3dd065da
    on agent_tools (agent_id);

create index agent_tools_agent_id_3dd065da_like
    on agent_tools (agent_id varchar_pattern_ops);

create index agent_tools_id_fe9a32b7_like
    on agent_tools (id varchar_pattern_ops);

create index agent_tools_user_id_8449fe0c
    on agent_tools (user_id);

create index agent_tools_user_id_8449fe0c_like
    on agent_tools (user_id varchar_pattern_ops);

