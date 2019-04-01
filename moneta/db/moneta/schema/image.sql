/*
    Table holds links to images.
*/
CREATE TABLE IF NOT EXISTS db_moneta.image (
  id INT NOT NULL,
  link VARCHAR(45) NOT NULL,
  PRIMARY KEY (id)
)
ENGINE = InnoDB CHARSET=utf8;
