/*
    Table that holds information about transaction between current and current.
*/
CREATE TABLE IF NOT EXISTS db_moneta.current_to_current (
  id INT NOT NULL AUTO_INCREMENT,
  from_current_id INT NOT NULL,
  to_current_id INT NOT NULL,
  amount FLOAT NULL,
  cur_coef FLOAT NULL, 
  user_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX `cur_to_cur_fcur_idx` (`from_current_id` ASC),
  INDEX `cur_to_cur_tcur_idx` (`to_current_id` ASC),
  INDEX `cur_to_cur_usr_idx` (`user_id` ASC),
  CONSTRAINT fk_current1
    FOREIGN KEY (from_current_id)
    REFERENCES current (id)
    ON DELETE CASCADE,
  CONSTRAINT fk_current2
    FOREIGN KEY (to_current_id)
    REFERENCES current (id)
    ON DELETE CASCADE,
  CONSTRAINT fk_cur_user
    FOREIGN KEY (user_id)
    REFERENCES user (id)
    ON DELETE CASCADE 
)
ENGINE = InnoDB CHARSET=utf8;

