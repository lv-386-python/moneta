/*
    Table that holds information about currencies.
*/
CREATE TABLE IF NOT EXISTS db_moneta.currencies (
  id INT NOT NULL AUTO_INCREMENT,
  currency VARCHAR(3) NOT NULL,
  PRIMARY KEY (id)
)
ENGINE = InnoDB  CHARSET=utf8;
