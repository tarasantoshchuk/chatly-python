
CREATE TABLE account_members (
    id integer NOT NULL,
    user_id integer,
    account_id integer
);


CREATE SEQUENCE account_members_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE account_members_id_seq OWNED BY account_members.id;


CREATE TABLE financial_accounts (
    id integer NOT NULL,
    name character varying(255),
    user_id integer
);



CREATE SEQUENCE financial_accounts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE financial_accounts_id_seq OWNED BY financial_accounts.id;



CREATE TABLE transactions (
    id integer NOT NULL,
    name character varying(255),
    amount double precision,
    account_id integer,
    user_id integer
);

CREATE SEQUENCE transactions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transactions_id_seq OWNED BY transactions.id;



CREATE TABLE users (
    id integer NOT NULL,
    username character varying(255),
    email character varying(255),
    password character varying(255)
);

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



ALTER SEQUENCE users_id_seq OWNED BY users.id;

ALTER TABLE ONLY account_members ALTER COLUMN id SET DEFAULT nextval('account_members_id_seq'::regclass);

ALTER TABLE ONLY financial_accounts ALTER COLUMN id SET DEFAULT nextval('financial_accounts_id_seq'::regclass);


ALTER TABLE ONLY transactions ALTER COLUMN id SET DEFAULT nextval('transactions_id_seq'::regclass);



ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);

ALTER TABLE ONLY account_members
    ADD CONSTRAINT account_members_pkey PRIMARY KEY (id);


ALTER TABLE ONLY financial_accounts
    ADD CONSTRAINT pk_financial_accounts PRIMARY KEY (id);


ALTER TABLE ONLY users
    ADD CONSTRAINT pk_user PRIMARY KEY (id);

ALTER TABLE ONLY transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (username);

ALTER TABLE ONLY transactions
    ADD CONSTRAINT fk_account FOREIGN KEY (account_id) REFERENCES financial_accounts(id);


ALTER TABLE ONLY account_members
    ADD CONSTRAINT fk_account_id FOREIGN KEY (account_id) REFERENCES financial_accounts(id);

ALTER TABLE ONLY financial_accounts
    ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE ONLY transactions
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);



ALTER TABLE ONLY account_members
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);










CREATE TABLE chat_members (
    id integer NOT NULL,
    user_id integer,
    chat_id integer
);


CREATE SEQUENCE chat_members_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE chat_members_id_seq OWNED BY chat_members.id;


CREATE TABLE chats (
    id integer NOT NULL,
    name character varying(255),
    user_id integer
);



CREATE SEQUENCE chat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE chat_id_seq OWNED BY chats.id;



CREATE TABLE messages (
    id integer NOT NULL,
    message character varying(255),
    chat_id integer,
    user_id integer
);

CREATE SEQUENCE messages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE messages_id_seq OWNED BY messages.id;



CREATE TABLE users (
    id integer NOT NULL,
    username character varying(255),
    email character varying(255),
    password character varying(255)
);

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



ALTER SEQUENCE users_id_seq OWNED BY users.id;

ALTER TABLE ONLY chat_members ALTER COLUMN id SET DEFAULT nextval('chat_members_id_seq'::regclass);

ALTER TABLE ONLY chats ALTER COLUMN id SET DEFAULT nextval('chats_id_seq'::regclass);


ALTER TABLE ONLY messages ALTER COLUMN id SET DEFAULT nextval('messages_id_seq'::regclass);



ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);

ALTER TABLE ONLY chat_members
    ADD CONSTRAINT chat_members_pkey PRIMARY KEY (id);


ALTER TABLE ONLY chats
    ADD CONSTRAINT pk_chats PRIMARY KEY (id);


ALTER TABLE ONLY users
    ADD CONSTRAINT pk_user PRIMARY KEY (id);

ALTER TABLE ONLY messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (username);

ALTER TABLE ONLY messages
    ADD CONSTRAINT fk_chat FOREIGN KEY (chat_id) REFERENCES chats(id);


ALTER TABLE ONLY chat_members
    ADD CONSTRAINT fk_chat_id FOREIGN KEY (chat_id) REFERENCES chats(id);

ALTER TABLE ONLY chats
    ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE ONLY messages
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);



ALTER TABLE ONLY chats
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);


