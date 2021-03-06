/*
    Table that describes current.
*/
CREATE TABLE IF NOT EXISTS db_moneta.current (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NULL,
  currency INT NOT NULL,
  create_time INT(11) NULL,
  mod_time INT(11) NULL,
  amount DECIMAL(13,1) NULL,
  image_id INT NOT NULL,
  owner_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_current_image
    FOREIGN KEY (image_id)
    REFERENCES image (id)
    ON DELETE CASCADE,
  CONSTRAINT fk_cur_curcur
    FOREIGN KEY (currency)
    REFERENCES currencies (id)
    ON DELETE CASCADE,
  CONSTRAINT fk_owner_cur_cur
    FOREIGN KEY (owner_id)
    REFERENCES user_settings (id)
    ON DELETE CASCADE
)
ENGINE = InnoDB CHARSET=utf8;
