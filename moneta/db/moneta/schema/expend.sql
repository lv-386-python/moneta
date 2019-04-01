/*
    Table that holds information about expend.
*/
CREATE TABLE IF NOT EXISTS db_moneta.expend (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NULL,
  currency VARCHAR(45) NOT NULL,
  create_time INT(11) NULL,
  modification_time INT(11) NULL,
  planned_cost FLOAT NULL,
  image_id INT NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_expend_image
    FOREIGN KEY (image_id)
    REFERENCES image (id)
)
ENGINE = InnoDB  CHARSET=utf8;
