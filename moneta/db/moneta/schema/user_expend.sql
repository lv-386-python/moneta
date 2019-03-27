/*
    Many-to-Many table between user and expend tables that additionally have can_edit field
    wich is used in sharing process.
*/
CREATE TABLE IF NOT EXISTS db_moneta.user_expend (
  user_id INT NOT NULL,
  expend_id INT NOT NULL,
  can_edit TINYINT NOT NULL,
  PRIMARY KEY (user_id, expend_id),
  CONSTRAINT fk_user2
    FOREIGN KEY (user_id)
    REFERENCES user (id),
  CONSTRAINT fk_expend
    FOREIGN KEY (expend_id)
    REFERENCES expend (id)
)
ENGINE = InnoDB  CHARSET=utf8;
