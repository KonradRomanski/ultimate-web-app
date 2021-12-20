
CREATE TABLE comments (
    id          INTEGER NOT NULL,
    description CLOB NOT NULL,
    user_id     INTEGER NOT NULL,
    post_id     INTEGER NOT NULL
);

ALTER TABLE comments ADD CONSTRAINT comments_pk PRIMARY KEY ( id );

CREATE TABLE like_comments (
    user_id    INTEGER NOT NULL,
    comments_id INTEGER NOT NULL
);

ALTER TABLE like_comments ADD CONSTRAINT like_comments_pk PRIMARY KEY ( user_id,
                                                                      comments_id );

CREATE TABLE like_post (
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL
);

ALTER TABLE like_post ADD CONSTRAINT like_post_pk PRIMARY KEY ( user_id,
                                                                post_id );

CREATE TABLE like_project (
    user_id    INTEGER NOT NULL,
    project_id INTEGER NOT NULL
);

ALTER TABLE like_project ADD CONSTRAINT like_project_pk PRIMARY KEY ( user_id,
                                                                      project_id );

CREATE TABLE log (
    action_type VARCHAR2(100) NOT NULL,
    action_time TIMESTAMP NOT NULL,
    table_name  VARCHAR2(100) NOT NULL,
    user_id     INTEGER NOT NULL
);

CREATE TABLE post (
    id         INTEGER NOT NULL,
    title     VARCHAR2(180) NOT NULL,
    content    CLOB,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    user_id    INTEGER,
    project_id INTEGER
);

ALTER TABLE post ADD CONSTRAINT post_pk PRIMARY KEY ( id );

CREATE TABLE project (
    id          INTEGER NOT NULL,
    name        VARCHAR2(180) NOT NULL,
    github_link VARCHAR2(200),
    description CLOB,
    created_at  TIMESTAMP NOT NULL,
    updated_at  TIMESTAMP
);

ALTER TABLE project ADD CONSTRAINT project_pk PRIMARY KEY ( id );

CREATE TABLE role (
    name             VARCHAR2(30) NOT NULL,
    permission_level INTEGER NOT NULL
);

ALTER TABLE role ADD CONSTRAINT role_pk PRIMARY KEY ( name );

CREATE TABLE stat (
    action_name VARCHAR2(100) NOT NULL,
    number    INTEGER,
    last_action TIMESTAMP
);

CREATE TABLE user (
    id              INTEGER NOT NULL,
    email           VARCHAR2(50) NOT NULL,
    password        VARCHAR2(30) NOT NULL,
    email_confirmed BLOB,
    first_name      VARCHAR2(20),
    last_name       VARCHAR2(20),
    created_at      TIMESTAMP NOT NULL,
    updated_at      TIMESTAMP,
    role_name       VARCHAR2(30) NOT NULL
);

CREATE UNIQUE INDEX user__idx ON
    user (
        role_name
    ASC );

ALTER TABLE user ADD CONSTRAINT user_pk PRIMARY KEY ( id );

ALTER TABLE comments
    ADD CONSTRAINT comments_post_fk FOREIGN KEY ( post_id )
        REFERENCES post ( id );

ALTER TABLE comments
    ADD CONSTRAINT comments_user_fk FOREIGN KEY ( user_id )
        REFERENCES user ( id );

ALTER TABLE like_comments
    ADD CONSTRAINT like_comments_comments_fk FOREIGN KEY ( comments_id )
        REFERENCES comments ( id );

ALTER TABLE like_comments
    ADD CONSTRAINT like_comments_user_fk FOREIGN KEY ( user_id )
        REFERENCES user ( id );

ALTER TABLE like_post
    ADD CONSTRAINT like_post_post_fk FOREIGN KEY ( post_id )
        REFERENCES post ( id );

ALTER TABLE like_post
    ADD CONSTRAINT like_post_user_fk FOREIGN KEY ( user_id )
        REFERENCES user ( id );

ALTER TABLE like_project
    ADD CONSTRAINT like_project_project_fk FOREIGN KEY ( project_id )
        REFERENCES project ( id );

ALTER TABLE like_project
    ADD CONSTRAINT like_project_user_fk FOREIGN KEY ( user_id )
        REFERENCES user ( id );

ALTER TABLE log
    ADD CONSTRAINT log_user_fk FOREIGN KEY ( user_id )
        REFERENCES user ( id );

ALTER TABLE post
    ADD CONSTRAINT post_project_fk FOREIGN KEY ( project_id )
        REFERENCES project ( id );

ALTER TABLE post
    ADD CONSTRAINT post_user_fk FOREIGN KEY ( user_id )
        REFERENCES user ( id );

ALTER TABLE user
    ADD CONSTRAINT user_role_fk FOREIGN KEY ( role_name )
        REFERENCES role ( name );

CREATE SEQUENCE comments_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER comments_id_trg BEFORE
    INSERT ON comments
    FOR EACH ROW
    WHEN ( new.id IS NULL )
BEGIN
    :new.id := comments_id_seq.nextval;
END;
/

CREATE SEQUENCE post_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER post_id_trg BEFORE
    INSERT ON post
    FOR EACH ROW
    WHEN ( new.id IS NULL )
BEGIN
    :new.id := post_id_seq.nextval;
END;
/

CREATE SEQUENCE project_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER project_id_trg BEFORE
    INSERT ON project
    FOR EACH ROW
    WHEN ( new.id IS NULL )
BEGIN
    :new.id := project_id_seq.nextval;
END;
/

CREATE SEQUENCE user_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER user_id_trg BEFORE
    INSERT ON user
    FOR EACH ROW
    WHEN ( new.id IS NULL )
BEGIN
    :new.id := user_id_seq.nextval;
END;
/

CREATE OR REPLACE FUNCTION PostAboutProject
    (v_project_id NUMBER, v_user_id NUMBER)
    RETURN NATURAL IS status NATURAL;


v_name VARCHAR(40);

BEGIN 
    SELECT name INTO v_name FROM project WHERE project_id = v_project_id;
    INSERT INTO POST(title, project_project_id, user_user_id) VALUES('Let`s talk about ' || v_name, v_project_id, v_user_id);
    status := 1;
RETURN status;
EXCEPTION WHEN NO_DATA_FOUND THEN
    status := 0;
    RETURN status;
END PostAboutProject;


CREATE OR REPLACE PROCEDURE SetDefaultStats AS
if_exists NUMBER;
BEGIN
    SELECT count(*) into if_exists FROM stat where action_name = 'UserCounter';
    IF if_exists = 0 THEN
        INSERT INTO stat(action_name)
            VALUES(
            'UserCounter'
        );
    END IF;
    
    SELECT count(*) into if_exists FROM stat where action_name = 'PostCounter';
    IF if_exists = 0 THEN
        INSERT INTO stat(action_name)
            VALUES(
            'PostCounter'
        );
    END IF;
    
    
    UPDATE stat
        SET counter = (SELECT count(*) FROM user),
        last_action = CURRENT_DATE
        WHERE action_name = 'UserCounter';
    
    
    UPDATE stat
        SET counter = (SELECT count(*) FROM post),
        last_action = CURRENT_DATE
        WHERE action_name = 'PostCounter';

    
END SetDefaultStats;