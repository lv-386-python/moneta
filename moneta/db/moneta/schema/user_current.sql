/*
    Many-to-Many table between user and current tables that additionally have can_edit field
    wich is used in sharing process.
*/  
CREATE TABLE IF NOT EXISTS db_moneta.user_current (
  user_id INT NOT NULL,
  current_id INT NOT NULL,
  can_edit TINYINT NOT NULL,
  PRIMARY KEY (user_id, current_id),
  CONSTRAINT fk_user_cur
    FOREIGN KEY (user_id)
    REFERENCES user (id)
    ON DELETE CASCADE,
  CONSTRAINT fk_current
    FOREIGN KEY (current_id)
    REFERENCES current (id)
    ON DELETE CASCADE
)
ENGINE = InnoDB CHARSET=utf8;
