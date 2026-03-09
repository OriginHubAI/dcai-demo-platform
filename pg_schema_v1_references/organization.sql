create table organization
(
    id            integer default nextval('organization_id_seq'::regclass) not null
        primary key,
    title         varchar(1000)                                            not null,
    created_at    timestamp with time zone                                 not null,
    updated_at    timestamp with time zone                                 not null,
    token         varchar(256),
    contact_info  varchar(254),
    created_by_id integer
);

alter table organization
    owner to myscale_kb_backend;

create index organization_created_by_id_idx
    on organization (created_by_id);

INSERT INTO public.organization (id, title, created_at, updated_at, token, contact_info, created_by_id) VALUES (2, 'Default Organization', '2025-08-12 05:52:17.325263 +00:00', '2025-08-12 05:52:17.325276 +00:00', 'CiFu4NxE5uMusAskNnvaWCoqvWUcGVsF1mz6QnKE', null, null);
INSERT INTO public.organization (id, title, created_at, updated_at, token, contact_info, created_by_id) VALUES (3, 'MyScale AI团队', '2025-08-13 04:03:06.309834 +00:00', '2025-08-13 04:03:06.309883 +00:00', 'CSvSN7V-dwLOYtv1JwXT5u10KWftWrxCEORpSEJ9uGA', 'team@myscale.com', 100016);
INSERT INTO public.organization (id, title, created_at, updated_at, token, contact_info, created_by_id) VALUES (4, 'MyScale AI团队', '2025-08-13 04:08:59.190395 +00:00', '2025-08-13 04:08:59.190433 +00:00', '-6kL14gZmXmxsUN31-e9WAWkSlxedOFApfWLzjo-isM', 'team@myscale.com', 100016);
