USE wworks_db;

DROP TABLE IF EXISTS replies;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS skills; 
DROP TABLE IF EXISTS user;

CREATE TABLE user (
  `uid` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(25) NOT NULL,
  `email` VARCHAR(25) NOT NULL,
  `f_name` VARCHAR(20),
  `l_name` VARCHAR(50),
  `password` VARCHAR(50) NOT NULL
) 
ENGINE=InnoDB;


CREATE TABLE skills (
  `uid` INT NOT NULL, 
  `skill` VARCHAR(30),
  foreign key (`uid`) references user(`uid`) 
        on update restrict 
        on delete restrict
)
ENGINE=InnoDB;


CREATE TABLE post (
  `pid` INT AUTO_INCREMENT PRIMARY KEY,
  `uid` INT NOT NULL, 
  `title` VARCHAR(40) NOT NULL, 
  `body` TEXT NOT NULL, 
  `post_date` DATE NOT NULL,
  `categories` SET('clothing', 'fitness', 'beauty', 'crafts', 'transportation', 'photography', 'other') NOT NULL,
  `status` ENUM('open', 'closed', 'in progress') NOT NULL, 
  foreign key (`uid`) references user(`uid`) 
        on update restrict 
        on delete restrict 
        ) 
ENGINE=InnoDB;


CREATE TABLE replies (
  `rid` INT AUTO_INCREMENT PRIMARY KEY,
  `pid` INT NOT NULL,
  `uid` INT NOT NULL,
  `body` TEXT NOT NULL,
  foreign key (`pid`) references post(`pid`) 
    on update restrict 
    on delete restrict
) 
ENGINE=InnoDB;







