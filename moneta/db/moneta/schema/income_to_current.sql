/*
    Table that holds information about transaction between income and current.
*/
CREATE TABLE IF NOT EXISTS db_moneta.income_to_current (
  id INT NOT NULL AUTO_INCREMENT,
  from_income_id INT NOT NULL,
  to_current_id INT NOT NULL,
  amount FLOAT NULL,
  cur_coef FLOAT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX `income_to_current_inc_idx` (`from_income_id` ASC),
  INDEX `income_to_current_cur_idx` (`to_current_id` ASC),
  INDEX `inc_to_cur_usr_idx` (`user_id` ASC),
  CONSTRAINT fk_income1
    FOREIGN KEY (from_income_id)
    REFERENCES income (id),
  CONSTRAINT fk_current3
    FOREIGN KEY (to_current_id)
    REFERENCES current (id),
  CONSTRAINT fk_user_trans
    FOREIGN KEY (user_id)
    REFERENCES user (id)
)
ENGINE = InnoDB CHARSET=utf8;