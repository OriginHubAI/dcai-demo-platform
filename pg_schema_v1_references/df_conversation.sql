create table df_conversation
(
    id            uuid                     not null
        primary key,
    user_id       uuid                     not null,
    conversion_id varchar(128)             not null,
    title         varchar(200),
    content       jsonb                    not null,
    del_flag      boolean                  not null,
    created_at    timestamp with time zone not null
);

alter table df_conversation
    owner to myscale_kb_backend;

create index df_conversa_convers_fb30e4_idx
    on df_conversation (conversion_id asc, del_flag asc, created_at desc);

create index df_conversa_user_id_cbe1af_idx
    on df_conversation (user_id asc, conversion_id asc, created_at desc);

create index df_conversation_conversion_id_31673291
    on df_conversation (conversion_id);

create index df_conversation_conversion_id_31673291_like
    on df_conversation (conversion_id varchar_pattern_ops);

create index df_conversation_del_flag_58d6d37e
    on df_conversation (del_flag);

create index df_conversation_user_id_fda7a174
    on df_conversation (user_id);

