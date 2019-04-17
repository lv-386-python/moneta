/*
    This table holds users info
*/
CREATE TABLE IF NOT EXISTS db_moneta.auth_user (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  password VARCHAR(128) NOT NULL,
  email VARCHAR(45) NOT NULL,
  last_login DATETIME DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_auth_user
    FOREIGN KEY (user_id)
    REFERENCES user_settings (id)
    ON DELETE CASCADE
)
ENGINE = InnoDB DEFAULT CHARSET=utf8;

