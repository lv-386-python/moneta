/*
    Table that describes income.
*/
CREATE TABLE IF NOT EXISTS db_moneta.income (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NULL,
  currency VARCHAR(45) NOT NULL,
  user_id INT NOT NULL,
  create_time INT(11) NULL,
  mod_time INT(11) NULL,
  image_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_income_image
    FOREIGN KEY (image_id)
    REFERENCES image (id),
  CONSTRAINT fk_income_user
    FOREIGN KEY (user_id)
    REFERENCES user (id)
)
ENGINE = InnoDB CHARSET=utf8;


