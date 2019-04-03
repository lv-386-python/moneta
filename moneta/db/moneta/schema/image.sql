/*
    Table holds links to images and .
*/
CREATE TABLE IF NOT EXISTS db_moneta.image (
  id INT NOT NULL AUTO_INCREMENT,
  css VARCHAR(45) NOT NULL,
  category VARCHAR(45) NOT NULL,
  PRIMARY KEY (id)
)
ENGINE = InnoDB CHARSET=utf8;

