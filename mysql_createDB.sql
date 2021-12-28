use `ultimate_web_app`;

CREATE TABLE comments (
    id          INTEGER PRIMARY KEY NOT NULL auto_increment,
    description LONGTEXT NOT NULL,
    user_id     INTEGER NOT NULL,
    post_id     INTEGER NOT NULL
);

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
    action_type VARCHAR(100) NOT NULL,
    action_time DATETIME(6) NOT NULL,
    table_name  VARCHAR(100) NOT NULL,
    user_id     INTEGER NOT NULL
);

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

CREATE TABLE user (
    id              INTEGER PRIMARY KEY NOT NULL auto_increment,
    email           VARCHAR(50) NOT NULL,
    password        VARCHAR(30) NOT NULL,
    email_confirmed LONGBLOB,
    first_name      VARCHAR(20),
    last_name       VARCHAR(20),
    created_at      DATETIME(6) NOT NULL,
    updated_at      DATETIME(6),
    role_name       VARCHAR(30) NOT NULL
);


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

DROP FUNCTION IF EXISTS PostAboutProject;

SET GLOBAL log_bin_trust_function_creators = 1;


DELIMITER //

CREATE FUNCTION PostAboutProject
    (v_project_id DOUBLE, v_user_id DOUBLE)
    RETURNS INT
 BEGIN DECLARE status INT;


DECLARE v_name VARCHAR(40);

  DECLARE EXIT HANDLER FOR NOT FOUND BEGIN
    SET status = 0;
    RETURN status;
 END; 
    SELECT name INTO v_name FROM project WHERE project_id = v_project_id;
    INSERT INTO POST(title, project_project_id, user_user_id) VALUES(CONCAT('Let`s talk about ' , ifnull(v_name, '')), v_project_id, v_user_id);
    SET status = 1;
RETURN status;
END;
//

DELIMITER ;

DROP PROCEDURE IF EXISTS SetDefaultStats;

DELIMITER //

CREATE PROCEDURE SetDefaultStats()
 BEGIN
DECLARE if_exists DOUBLE;
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
        last_action = NOW()
        WHERE action_name = 'UserCounter';
    
    
    UPDATE stat
        SET counter = (SELECT count(*) FROM post),
        last_action = NOW()
        WHERE action_name = 'PostCounter';

    
END ;
//

DELIMITER ;
