/*
    This table holds users info
*/  
CREATE TABLE IF NOT EXISTS db_moneta.user (
  id INT NOT NULL AUTO_INCREMENT,
  password VARCHAR(45) NOT NULL,
  def_currency ENUM("UAH", "USD", "EUR", "GBP") NOT NULL,
  email VARCHAR(45) NOT NULL,
  is_activated TINYINT NOT NULL,
  PRIMARY KEY (id)
)
ENGINE = InnoDB DEFAULT CHARSET=utf8;
