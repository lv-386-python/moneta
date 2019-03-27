/*
    Table that holds information about transaction between current and expend.
*/
CREATE TABLE IF NOT EXISTS db_moneta.current_to_expend (
  id INT NOT NULL AUTO_INCREMENT,
  from_current_id INT NOT NULL,
  to_expend_id INT NOT NULL,
  amount FLOAT NULL,
  cur_coef FLOAT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX `cur_to_exp_fcur_idx` (`from_current_id` ASC),
  INDEX `cur_to_exp_tcur_idx` (`to_expend_id` ASC),
  INDEX `cur_to_exp_usr_idx` (`user_id` ASC),
  CONSTRAINT fk_cur
    FOREIGN KEY (from_current_id)
    REFERENCES current (id),
  CONSTRAINT fk_expend1
    FOREIGN KEY (to_expend_id)
    REFERENCES expend (id),
  CONSTRAINT fk_user_trans1
    FOREIGN KEY (user_id)
    REFERENCES user (id)
)
ENGINE = InnoDB CHARSET=utf8;

