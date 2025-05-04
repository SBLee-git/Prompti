-- public.members definition

-- Drop table

-- DROP TABLE public.members;

CREATE TABLE public.members (
	id uuid DEFAULT uuid_generate_v4() NOT NULL,
	email varchar(255) NOT NULL,
	password_hash text NOT NULL,
	user_type varchar(10) NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT members_email_user_type_key UNIQUE (email, user_type),
	CONSTRAINT members_pkey PRIMARY KEY (id),
	CONSTRAINT members_user_type_check CHECK (((user_type)::text = ANY ((ARRAY['개인'::character varying, '기업'::character varying])::text[])))
);

-- public.login_history definition

-- Drop table

-- DROP TABLE public.login_history;

CREATE TABLE public.login_history (
	id uuid DEFAULT uuid_generate_v4() NOT NULL,
	user_id uuid NULL,
	ip_address varchar(45) NULL,
	user_agent text NULL,
	login_time timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT login_history_pkey PRIMARY KEY (id),
	CONSTRAINT login_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.members(id) ON DELETE CASCADE
);

-- public.chat_history definition

-- Drop table

-- DROP TABLE public.chat_history;

CREATE TABLE public.chat_history (
	id uuid NOT NULL,
	user_id uuid NOT NULL,
	position_name text NOT NULL,
	experience text NOT NULL,
	created_at timestamp DEFAULT now() NULL,
	CONSTRAINT chat_history_metadata_pkey PRIMARY KEY (id)
);