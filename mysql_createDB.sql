use `ultimate_web_app`;

CREATE TABLE comment (
    id          INTEGER PRIMARY KEY NOT NULL auto_increment,
    description LONGTEXT NOT NULL,
    user_id     INTEGER NOT NULL,
    post_id     INTEGER NOT NULL
);

CREATE TABLE like_comment (
    user_id    INTEGER NOT NULL,
    comment_id INTEGER NOT NULL
);

ALTER TABLE like_comment ADD CONSTRAINT like_comment_pk PRIMARY KEY ( user_id,
                                                                      comment_id );

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

CREATE TABLE post (
    id         INTEGER PRIMARY KEY NOT NULL auto_increment,
    title     VARCHAR(180) NOT NULL,
    content    LONGTEXT,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6),
    user_id    INTEGER,
    project_id INTEGER
);

CREATE TABLE project (
    id          INTEGER PRIMARY KEY NOT NULL auto_increment,
    name        VARCHAR(180) NOT NULL,
    github_link VARCHAR(200),
    description LONGTEXT,
    created_at  DATETIME(6) NOT NULL,
    updated_at  DATETIME(6)
);


CREATE TABLE stat (
    action_name VARCHAR(100) NOT NULL,
    number    INTEGER,
    last_action DATETIME(6)
);

ALTER TABLE comment
    ADD CONSTRAINT comment_post_fk FOREIGN KEY ( post_id )
        REFERENCES post ( id );

ALTER TABLE comment
    ADD CONSTRAINT comment_user_fk FOREIGN KEY ( user_id )
        REFERENCES user ( id );

ALTER TABLE like_comment
    ADD CONSTRAINT like_comment_comment_fk FOREIGN KEY ( comment_id )
        REFERENCES comment ( id );

ALTER TABLE like_comment
    ADD CONSTRAINT like_comment_user_fk FOREIGN KEY ( user_id )
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

ALTER TABLE post
    ADD CONSTRAINT post_project_fk FOREIGN KEY ( project_id )
        REFERENCES project ( id );

ALTER TABLE post
    ADD CONSTRAINT post_user_fk FOREIGN KEY ( user_id )
        REFERENCES user ( id );
