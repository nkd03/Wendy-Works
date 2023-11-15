USE wworks_db;

INSERT INTO `user` (username, email, f_name, l_name, `password`, skills) VALUES
('nd105', 'nd105@wellesley.edu', 'Noelle', 'Davis', 'pw123', 'sewing, fitness ,car'),
('janedoe', 'jane.doe@wellesley.edu', 'Jane','Doe','pw456', 'car'),
('wendywells', 'ww123@wellesley.edu', 'Wendy', 'Wellesley', 'redtomato', 'automobile');


INSERT INTO `post` (`uid`, `title`, `body`, `post_date`, `categories`, `status`) VALUES
(1, 'The Best Fitness Routines?', 'In the KSC, how do I use the stairmaster?', '2023-09-10', 'fitness', 'open'),
(1, 'Photography Tips for Beginners?', 'When framing Galen Stone Tower, how do I keep the light from reflecting in my lens? ', '2023-10-02', 'photography', 'in progress'),
(2, 'DIY Crafts for Home Decor?', 'I need help creating a wreath', '2023-08-20', 'crafts', 'closed');


INSERT INTO `replies` (`pid`, `uid`, `body`) VALUES
(1, 2, ' Hopping on the Stair master now! I can show you SO soon :)'),
(2, 3, 'I have some photography tips! Let me know when you are free'),
(1, 2, 'DIY Crafts are really my thing! I make fall decor all the time');