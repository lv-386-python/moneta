/*
    This table holds users info
*/  
CREATE TABLE IF NOT EXISTS db_moneta.user_settings (
  id INT NOT NULL AUTO_INCREMENT,
  def_currency INT NOT NULL,
  is_activated TINYINT NOT NULL,
  PRIMARY KEY (id),
  INDEX `cur_cur` (`def_currency` ASC),
  CONSTRAINT fk_curcur
    FOREIGN KEY (def_currency)
    REFERENCES currencies (id)
    ON DELETE CASCADE
)
ENGINE = InnoDB DEFAULT CHARSET=utf8;
