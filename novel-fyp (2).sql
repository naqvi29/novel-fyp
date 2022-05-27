-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 27, 2022 at 11:56 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `novel-fyp`
--

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `author` text NOT NULL,
  `publisher` text NOT NULL,
  `category` text NOT NULL,
  `price` float NOT NULL,
  `quantity` int(11) NOT NULL,
  `image` text NOT NULL,
  `description` longtext NOT NULL,
  `rating` float DEFAULT NULL,
  `publisher_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `title`, `author`, `publisher`, `category`, `price`, `quantity`, `image`, `description`, `rating`, `publisher_id`) VALUES
(1, 'It Ends with Us: A Novel', 'Colleen Hoover', 'shop keeper', 'comics', 10.78, 100, '1501110365.01._SCLZZZZZZZ_SX500_.jpg', 'In this “brave and heartbreaking novel that digs its claws into you and doesn’t let go, long after you’ve finished it” (Anna Todd, New York Times bestselling author) from the #1 New York Times bestselling author of All Your Perfects, a workaholic with a too-good-to-be-true romance can’t stop thinking about her first love.\r\n\r\nLily hasn’t always had it easy, but that’s never stopped her from working hard for the life she wants. She’s come a long way from the small town where she grew up—she graduated from college, moved to Boston, and started her own business. And when she feels a spark with a gorgeous neurosurgeon named Ryle Kincaid, everything in Lily’s life seems too good to be true.\r\n\r\nRyle is assertive, stubborn, maybe even a little arrogant. He’s also sensitive, brilliant, and has a total soft spot for Lily. And the way he looks in scrubs certainly doesn’t hurt. Lily can’t get him out of her head. But Ryle’s complete aversion to relationships is disturbing. Even as Lily finds herself becoming the exception to his “no dating” rule, she can’t help but wonder what made him that way in the first place.\r\n\r\nAs questions about her new relationship overwhelm her, so do thoughts of Atlas Corrigan—her first love and a link to the past she left behind. He was her kindred spirit, her protector. When Atlas suddenly reappears, everything Lily has built with Ryle is threatened.\r\n\r\nAn honest, evocative, and tender novel, It Ends with Us is “a glorious and touching read, a forever keeper. The kind of book that gets handed down” (USA TODAY).', 5, 2),
(14, 'Where the Crawdads Sing', 'Delia Owens', 'shop keeper', 'fiction', 2000, 200, '0735219109.01._SCLZZZZZZZ_SX500_.jpg', 'SOON TO BE A MAJOR MOTION PICTURE—The #1 New York Times bestselling worldwide sensation with more than 12 million copies sold, hailed by The New York Times Book Review as “a painfully beautiful first novel that is at once a murder mystery, a coming-of-age narrative and a celebration of nature.”', NULL, 2),
(15, 'The Power of the Dog', 'Thomas Savage', 'shop keeper', 'comics', 1500, 299, '0316436607.01._SCLZZZZZZZ_SX500_.jpg', 'Now an Academy Award-winning Netflix film by Jane Campion, starring Benedict Cumberbatch and Kirsten Dunst: Thomas Savage\'s acclaimed Western is \"a pitch-perfect evocation of time and place\" (Boston Globe) for fans of East of Eden and Brokeback Mountain.', NULL, 2),
(17, 'Don\'t Let Me Fall', 'Kelsie Rae', 'shop keeper', 'fiction', 1200, 100, 'B09NWRYKXD.01._SCLZZZZZZZ_SX500_.jpg', 'We were never supposed to happen.\r\nHe was my boyfriend\'s roommate.\r\nHe was also my kryptonite.', NULL, 2),
(18, 'I Love You to the Moon and Back', 'Amelia Hepworth', 'shop keeper', 'fiction', 500, 100, 'B09ZPX7618.01._SCLZZZZZZZ_SX500_.jpg', 'Show a child just how strong your love is every minute of the day! Features a \"To\" and \"From\" personalization page, making this sweet offering an ideal gift for baby showers, birthdays, and new parents. ', NULL, 2),
(19, 'Book Lovers', 'Emily Henry', 'shop keeper', 'fiction', 2500, 100, '0593334833.01.S001.LXXXXXXX.jpg', '“One of my favorite authors.”—Colleen Hoover\r\n\r\nAn insightful, delightful, instant #1 New York Times bestseller from the author of Beach Read and People We Meet on Vacation.', NULL, 2),
(20, 'Slow Horses', 'Mick Herron', 'shop keeper', 'fiction', 6000, 100, '51xTXll-VL._SX329_BO1204203200_.jpg', 'Now an Apple Original series streaming on Apple TV+ starring Gary Oldman and Kristin Scott Thomas.\r\n\r\nWelcome to the thrilling and unnervingly prescient world of the slow horses. This team of MI5 agents is united by one common bond: They\'ve screwed up royally and will do anything to redeem themselves.', NULL, 2),
(21, 'Phil: The Rip-Roaring', 'Alan Shipnuck ', 'shop keeper', 'fiction', 1000, 100, '1476797099.01._SCLZZZZZZZ_SX500_.jpg', 'A juicy and freewheeling biography of legendary golf champion Phil Mickelson—who has led a big, controversial life—as reported by longtime Sports Illustrated writer and bestselling author Alan Shipnuck.\r\n', NULL, 2),
(22, 'Phil: The Rip-Roaring', 'Alan Shipnuck ', 'shop keeper', 'science', 1000, 100, '1476797099.01._SCLZZZZZZZ_SX500_.jpg', 'A juicy and freewheeling biography of legendary golf champion Phil Mickelson—who has led a big, controversial life—as reported by longtime Sports Illustrated writer and bestselling author Alan Shipnuck.\r\n', NULL, 2),
(23, 'Slow Horses', 'Mick Herron', 'shop keeper', 'science', 6000, 100, '51xTXll-VL._SX329_BO1204203200_.jpg', 'Now an Apple Original series streaming on Apple TV+ starring Gary Oldman and Kristin Scott Thomas.\r\n\r\nWelcome to the thrilling and unnervingly prescient world of the slow horses. This team of MI5 agents is united by one common bond: They\'ve screwed up royally and will do anything to redeem themselves.', NULL, 2),
(24, 'Where the Crawdads Sing', 'Delia Owens', 'shop keeper', 'science', 2000, 200, '0735219109.01._SCLZZZZZZZ_SX500_.jpg', 'SOON TO BE A MAJOR MOTION PICTURE—The #1 New York Times bestselling worldwide sensation with more than 12 million copies sold, hailed by The New York Times Book Review as “a painfully beautiful first novel that is at once a murder mystery, a coming-of-age narrative and a celebration of nature.”', NULL, 2),
(25, 'Don\'t Let Me Fall', 'Kelsie Rae', 'shop keeper', 'science', 1200, 100, 'B09NWRYKXD.01._SCLZZZZZZZ_SX500_.jpg', 'We were never supposed to happen.\r\nHe was my boyfriend\'s roommate.\r\nHe was also my kryptonite.', NULL, 2),
(26, 'I Love You to the Moon and Back', 'Amelia Hepworth', 'shop keeper', 'science', 500, 100, 'B09ZPX7618.01._SCLZZZZZZZ_SX500_.jpg', 'Show a child just how strong your love is every minute of the day! Features a \"To\" and \"From\" personalization page, making this sweet offering an ideal gift for baby showers, birthdays, and new parents. ', NULL, 2),
(27, 'Book Lovers', 'Emily Henry', 'shop keeper', 'science', 2500, 100, '0593334833.01.S001.LXXXXXXX.jpg', '“One of my favorite authors.”—Colleen Hoover\r\n\r\nAn insightful, delightful, instant #1 New York Times bestseller from the author of Beach Read and People We Meet on Vacation.', NULL, 2),
(28, 'Here\'s the Deal', 'Kellyanne Conway', 'shop keeper', 'fiction', 1200, 100, 'heres-the-deal-9781982187347_lg.jpg', 'Among the Trump era’s savviest insiders, one name stands especially tall: Kellyanne.\r\n\r\nAs a highly respected pollster for corporate and Republican clients and a frequent television talk show guest, Kellyanne Conway had already established herself as one of the brightest lights on the national political scene when Donald Trump asked her to run his presidential campaign. She agreed, delivering him to the White House, becoming the first woman in American history to manage a winning presidential campaign, and changing the American landscape forever. Who she is, how she did it, and who tried to stop her is a fascinating story of personal triumph and political intrigue that has never been told…until now.\r\n\r\nIn Here’s The Deal, Kellyanne takes you on a journey all the way to the White House and beyond with her trademark sharp wit, raw honesty, and level eye. It’s all here: what it’s like to be dissected on national television. How to outsmart the media mob. How to outclass the crazy critics. How to survive and succeed male-dominated industries. What happens when the perils of social media really hit home. And what happens when the divisions across the country start playing out in one’s own family.\r\n\r\nIn this open and vulnerable account, Kellyanne turns the camera on herself. What she has to share—about our politics, about the media, about her time in the White House, and about her personal journey—is an astonishing glimpse of visibility and vulnerability, of professional and personal highs and lows, and ultimately, of triumph.\r\n', NULL, 2),
(29, 'It Ends with Us: A Novel', 'Colleen Hoover', 'shop keeper', 'fiction', 10.78, 100, '1501110365.01._SCLZZZZZZZ_SX500_.jpg', 'In this “brave and heartbreaking novel that digs its claws into you and doesn’t let go, long after you’ve finished it” (Anna Todd, New York Times bestselling author) from the #1 New York Times bestselling author of All Your Perfects, a workaholic with a too-good-to-be-true romance can’t stop thinking about her first love.\r\n\r\nLily hasn’t always had it easy, but that’s never stopped her from working hard for the life she wants. She’s come a long way from the small town where she grew up—she graduated from college, moved to Boston, and started her own business. And when she feels a spark with a gorgeous neurosurgeon named Ryle Kincaid, everything in Lily’s life seems too good to be true.\r\n\r\nRyle is assertive, stubborn, maybe even a little arrogant. He’s also sensitive, brilliant, and has a total soft spot for Lily. And the way he looks in scrubs certainly doesn’t hurt. Lily can’t get him out of her head. But Ryle’s complete aversion to relationships is disturbing. Even as Lily finds herself becoming the exception to his “no dating” rule, she can’t help but wonder what made him that way in the first place.\r\n\r\nAs questions about her new relationship overwhelm her, so do thoughts of Atlas Corrigan—her first love and a link to the past she left behind. He was her kindred spirit, her protector. When Atlas suddenly reappears, everything Lily has built with Ryle is threatened.\r\n\r\nAn honest, evocative, and tender novel, It Ends with Us is “a glorious and touching read, a forever keeper. The kind of book that gets handed down” (USA TODAY).', 0, 2),
(30, 'The Power of the Dog', 'Thomas Savage', 'shop keeper', 'fiction', 1500, 299, '0316436607.01._SCLZZZZZZZ_SX500_.jpg', 'Now an Academy Award-winning Netflix film by Jane Campion, starring Benedict Cumberbatch and Kirsten Dunst: Thomas Savage\'s acclaimed Western is \"a pitch-perfect evocation of time and place\" (Boston Globe) for fans of East of Eden and Brokeback Mountain.', NULL, 2),
(31, 'Don\'t Let Me Fall', 'Kelsie Rae', 'shop keeper', 'science', 1200, 100, 'B09NWRYKXD.01._SCLZZZZZZZ_SX500_.jpg', 'We were never supposed to happen.\r\nHe was my boyfriend\'s roommate.\r\nHe was also my kryptonite.', NULL, 2);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `publisher_id` int(11) NOT NULL,
  `total_price` float NOT NULL,
  `status` text NOT NULL,
  `rating` int(11) DEFAULT NULL,
  `delivery_address` longtext NOT NULL,
  `city` text NOT NULL,
  `name` text DEFAULT NULL,
  `email` text DEFAULT NULL,
  `phone` text DEFAULT NULL,
  `del_ins` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `user_id`, `book_id`, `publisher_id`, `total_price`, `status`, `rating`, `delivery_address`, `city`, `name`, `email`, `phone`, `del_ins`) VALUES
(43, 6, 1, 2, 10.78, 'delivered', 5, 'R-1289 Block 14 Gulshan', 'karachi', 'Developer', 'developer@test.com', '03232629249', ''),
(44, 6, 14, 2, 2000, 'delivered', NULL, 'R-1289 Block 14 Gulshan', 'karachi', 'Developer', 'developer@test.com', '03232629249', ''),
(45, 6, 15, 2, 1500, 'pending', NULL, 'R-1289 Block 14 Gulshan', 'karachi', 'Developer', 'developer@test.com', '03232629249', ''),
(46, 6, 19, 2, 2500, 'pending', NULL, 'dasdjkasd', 'karachi', 'ZGr', 'asdas@asdda.com', '32989283490', 'sadasd');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `userid` int(11) NOT NULL,
  `email` text NOT NULL,
  `password` text NOT NULL,
  `first_name` text NOT NULL,
  `last_name` text NOT NULL,
  `gender` enum('male','female','','') NOT NULL,
  `type` varchar(200) NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userid`, `email`, `password`, `first_name`, `last_name`, `gender`, `type`) VALUES
(1, 'admin@bk.com', 'admin', 'admin', '', 'male', 'admin'),
(2, 'shopkeeper@bk.com', '123', 'shop', 'keeper', 'male', 'shopkeeper'),
(6, 'customer@bk.com', '123', 'customer', '', 'male', 'user'),
(9, 'bilalwaqar610@gmail.com', 'aaa', 'bilal', 'waqar', 'male', 'user'),
(10, 'bilalahmed@gmail.com', 'aaa', 'bilal', 'ahmed', 'male', 'shopkeeper'),
(11, 'alikhan@gmail.com', 'aaa', 'ali', 'khan', 'male', 'user'),
(12, 'heloa12@gmail.com', 'aaa', 'helo', 'a', 'male', 'shopkeeper');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `userid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
