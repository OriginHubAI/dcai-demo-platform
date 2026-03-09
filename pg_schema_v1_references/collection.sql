create table collection
(
    id         varchar(36)                not null
        primary key,
    title      varchar(255) default NULL::character varying,
    total      integer      default 0     not null,
    del_flag   boolean      default false not null,
    updated_at timestamp with time zone,
    created_at timestamp with time zone,
    user_id    varchar(36)
);

alter table collection
    owner to myscale_kb_backend;

create index collection_id_42415fa8_like
    on collection (id varchar_pattern_ops);

create index collection_user_id_e8aa841d
    on collection (user_id);

create index collection_user_id_e8aa841d_like
    on collection (user_id varchar_pattern_ops);

