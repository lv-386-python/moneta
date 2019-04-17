/*
    Many-to-Many table between user and income.
*/  
CREATE TABLE IF NOT EXISTS db_moneta.user_income (
  user_id INT NOT NULL,
  income_id INT NOT NULL,
  PRIMARY KEY (user_id, income_id),
  CONSTRAINT fk_user
    FOREIGN KEY (user_id)
    REFERENCES user (id)
    ON DELETE CASCADE,
  CONSTRAINT fk_income
    FOREIGN KEY (income_id)
    REFERENCES income (id)
    ON DELETE CASCADE
)
ENGINE = InnoDB CHARSET=utf8;
