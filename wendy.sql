USE wworks_db;

DROP TABLE IF EXISTS replies;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `uid` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(25) NOT NULL,
  `email` VARCHAR(25) NOT NULL,
  `f_name` VARCHAR(20),
  `l_name` VARCHAR(50),
  `password` VARCHAR(30) NOT NULL 
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
  FOREIGN KEY (`uid`) REFERENCES `user` (`uid`) ON DELETE CASCADE
) 
ENGINE=InnoDB;

CREATE TABLE replies (
  `rid` INT AUTO_INCREMENT PRIMARY KEY,
  `pid` INT NOT NULL,
  `uid` INT NOT NULL,
  `body` TEXT NOT NULL,
  FOREIGN KEY (`pid`) REFERENCES `post` (`pid`) ON DELETE CASCADE,
  FOREIGN KEY (`uid`) REFERENCES `user` (`uid`) ON DELETE CASCADE
) 
ENGINE=InnoDB;


INSERT INTO `user` (username, email, f_name, l_name, `password`) VALUES
('nd105', 'nd105@welleseley.edu', 'Noelle', 'Davis', 'pw123'),
('janedoe', 'jane.doe@wellesley.edu', 'Jane', 'Doe', 'pw456'),
('wendywells', 'ww123@wellesley.edu', 'Wendy', 'Wellesley', 'redtomato');


INSERT INTO `post` (`uid`, `title`, `body`, `post_date`, `categories`, `status`) VALUES
(1, 'The Best Fitness Routines?', 'In the KSC, how do I use the stairmaster?', '2023-09-10', 'fitness', 'open'),
(1, 'Photography Tips for Beginners?', 'When framing Galen Stone Tower, how do I keep the light from reflecting in my lens? ', '2023-10-02', 'photography', 'in progress'),
(2, 'DIY Crafts for Home Decor?', 'I need help creating a wreath', '2023-08-20', 'crafts', 'closed');


INSERT INTO `replies` (`pid`, `uid`, `body`) VALUES
(1, 2, ' Hopping on the Stair master now! I can show you SO soon :)'),
(2, 3, 'I have some photography tips! Let me know when you are free'),
(1, 2, 'DIY Crafts are really my thing! I make fall decor all the time');




