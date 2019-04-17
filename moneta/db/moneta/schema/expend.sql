/*
    Table that holds information about expend.
*/
CREATE TABLE IF NOT EXISTS db_moneta.expend (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NULL,
  currency INT NOT NULL,
  create_time INT(11) NULL,
  mod_time INT(11) NULL,
  amount FLOAT NULL,
  image_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_expend_image
    FOREIGN KEY (image_id)
    REFERENCES image (id)
    ON DELETE CASCADE,
  CONSTRAINT fk_expend_curcur
    FOREIGN KEY (currency)
    REFERENCES currencies (id)
    ON DELETE CASCADE
)
ENGINE = InnoDB  CHARSET=utf8;
