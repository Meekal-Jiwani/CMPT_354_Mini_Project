INSERT INTO Authors (AuthorName) VALUES
('George Orwell'), ('Harper Lee'), ('Isaac Asimov'), ('Agatha Christie'),
('Toni Morrison'), ('J.R.R. Tolkien'), ('Bill Bryson'), ('Neil Gaiman'),
('Andy Weir'), ('Margaret Atwood'),

('James Patterson'), ('Ann Patchett'), ('Colleen Hoover'), ('Brandon Sanderson'), ('Liane Moriarty');

INSERT INTO Media (Title, Type, PublicationDate) VALUES
('1984', 'Print Book', '1949-06-08'),
('To Kill a Mockingbird', 'Print Book', '1960-07-11'),
('Foundation', 'Print Book', '1951-05-01'),
('Murder on the Orient Express', 'Online Book', '1934-01-01'),
('Beloved', 'Print Book', '1987-09-02'),
('The Hobbit', 'Print Book', '1937-09-21'),
('Sapiens', 'Online Book', '2011-01-01'),
('Half of a Yellow Sun', 'Print Book', '2006-08-01'),
('Project Hail Mary', 'Online Book', '2021-05-04'),
('The Handmaid''s Tale', 'Print Book', '1985-08-01'),
('National Geographic Magazine', 'Magazine', '2026-08-01'),
('Computer Science Journal', 'Scientific Journal', '2026-06-15'),
('Kind of Blue', 'Record', '1959-08-17'),

('Along Came a Spider', 'Print Book', '1993-01-01'),
('Commonwealth', 'Print Book', '2016-09-13'),
('It Ends with Us', 'Print Book', '2016-08-02'),
('Mistborn', 'Print Book', '2006-07-17'),
('Big Little Lies', 'Print Book', '2014-07-29');

INSERT INTO Customers (FirstName, LastName, DOB, Balance) VALUES
('Jon', 'Doe', '2003-02-14', 0),
('Ayesha', 'Khan', '1998-11-02', 0),
('Daniel', 'Nguyen', '2000-05-19', 5.00),
('Priya', 'Sharma', '1995-03-30', 0),
('Liam', 'Chen', '1990-12-08', 0),
('Sofia', 'Martinez', '2002-07-22', 0),
('Ethan', 'Brown', '1999-09-15', 0),
('Zara', 'Ahmed', '2001-01-27', 10.00),
('Noah', 'Kim', '1997-06-11', 0),
('Amara', 'Okafor', '2004-04-05', 0),

('Alex', 'Wong', '1996-08-10', 0),
('Maya', 'Patel', '2000-02-02', 0),
('Chris', 'Lee', '1993-05-05', 0),
('Jordan', 'Smith', '1998-12-01', 0),
('Taylor', 'Brooks', '2001-03-15', 0);

INSERT INTO Employees (Email, FirstName, LastName, Position, PhoneNum, DOB, DateHired) VALUES
('j.wilson@library.org', 'James', 'Wilson', 'Head Librarian', '604-555-0101', '1980-04-12', '2010-06-01'),
('test@library.org', 'John', 'Doe', 'Test Dummy', '111-111-1111','1980-04-12', '2010-06-01'),
('m.tran@library.org', 'Mai', 'Tran', 'Librarian', '604-555-0102', '1988-09-23', '2015-03-15'),
('r.patel@library.org', 'Raj', 'Patel', 'Librarian', '604-555-0103', '1992-01-30', '2018-08-20'),
('s.lee@library.org', 'Sarah', 'Lee', 'Circulation Assistant', '604-555-0104', '1996-06-17', '2020-01-10'),
('k.singh@library.org', 'Karan', 'Singh', 'Circulation Assistant', '604-555-0105', '1998-11-05', '2021-05-05'),
('d.cooper@library.org', 'Diane', 'Cooper', 'Events Coordinator', '604-555-0106', '1985-02-28', '2016-09-01'),
('a.garcia@library.org', 'Ana', 'Garcia', 'IT Support', '604-555-0107', '1993-07-14', '2019-02-11'),
('t.nakamura@library.org', 'Taro', 'Nakamura', 'Archivist', '604-555-0108', '1979-12-03', '2008-04-22'),
('e.robinson@library.org', 'Emily', 'Robinson', 'Volunteer Coordinator', '604-555-0109', '1990-10-09', '2017-07-19'),
('b.osei@library.org', 'Ben', 'Osei', 'Security', '604-555-0110', '1987-03-21', '2012-11-30'),

('l.chen@library.org', 'Lily', 'Chen', 'Librarian', '604-555-0111', '1991-04-18', '2019-10-01'),
('m.davis@library.org', 'Mark', 'Davis', 'Circulation Assistant', '604-555-0112', '1995-09-09', '2021-11-15'),
('p.wong@library.org', 'Paul', 'Wong', 'IT Support', '604-555-0113', '1989-06-06', '2014-03-20');

INSERT INTO MediaAuthors (MediaID, AuthorID) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
(6, 6), (7, 7), (8, 8), (9, 9), (10, 10),
(3, 9),

(14, 11), (15, 12), (16, 13), (17, 14), (18, 15);

INSERT INTO CandidateMedia (Title, Type, PublicationDate, DonatedBy) VALUES
('Dune', 'Print Book', '1965-08-01', 1),
('The Left Hand of Darkness', 'Print Book', '1969-03-01', 2),
('Cosmos', 'Print Book', '1980-01-01', NULL),
('Time Magazine - July 2026', 'Magazine', '2026-07-01', NULL),
('Brief Answers to the Big Questions', 'Online Book', '2018-10-16', 3),
('The Martian', 'Print Book', '2011-09-27', NULL),
('Klara and the Sun', 'Print Book', '2021-03-02', 4),
('Nature - June 2026', 'Scientific Journal', '2026-06-01', NULL),
('Abbey Road', 'Record', '1969-09-26', 5),
('Circe', 'Print Book', '2018-04-10', NULL),

('Neverwhere', 'Print Book', '1996-09-16', 6),
('Coraline', 'Print Book', '2002-07-02', NULL),
('Ready Player One', 'Print Book', '2011-08-16', 7),
('The Night Circus', 'Print Book', '2011-09-13', NULL),
('Verity', 'Print Book', '2018-10-02', 9);

INSERT INTO Loans (MediaID, CheckoutDate, CustomerID, DueDate, ReturnDate) VALUES
(1, '2026-07-01', 1, '2026-07-15', '2026-07-14'),
(2, '2026-07-02', 2, '2026-07-16', '2026-07-16'),
(3, '2026-07-03', 4, '2026-07-17', NULL),
(4, '2026-07-04', 5, '2026-07-18', '2026-07-25'),
(5, '2026-07-05', 6, '2026-07-19', '2026-07-19'),
(6, '2026-07-06', 7, '2026-07-20', NULL),
(7, '2026-07-07', 9, '2026-07-21', '2026-07-21'),
(8, '2026-07-08', 10, '2026-07-22', NULL),
(9, '2026-07-09', 1, '2026-07-23', '2026-07-23'),
(10, '2026-07-10', 4, '2026-07-24', NULL),

(14, '2026-07-11', 2, '2026-07-25', NULL),
(15, '2026-07-12', 4, '2026-07-26', '2026-07-24'),
(16, '2026-07-13', 5, '2026-07-27', NULL),
(17, '2026-07-14', 6, '2026-07-28', '2026-07-30'),
(18, '2026-07-15', 9, '2026-07-29', NULL);

INSERT INTO Rooms (RoomNumber, Capacity) VALUES
(101, 20), (102, 15), (103, 30), (104, 10), (105, 50),
(111, 22), (112, 35), (113, 14), (114, 45), (115, 16),
(106, 25), (107, 12), (108, 40), (109, 18), (110, 8);

INSERT INTO Bookings (CustomerID, BookingDate, RoomNumber, StartTime, EndTime) VALUES
(1, '2026-08-01', 104, '10:00', '11:00'),
(2, '2026-08-02', 107, '13:00', '14:30'),
(3, '2026-08-03', 110, '09:00', '10:00'),
(4, '2026-08-04', 102, '15:00', '16:00'),
(5, '2026-08-05', 109, '11:00', '12:00'),
(6, '2026-08-06', 104, '14:00', '15:00'),
(7, '2026-08-07', 107, '10:30', '11:30'),
(8, '2026-08-08', 110, '16:00', '17:00'),
(9, '2026-08-09', 102, '09:30', '10:30'),

(10, '2026-08-10', 109, '13:30', '14:30'),
(11, '2026-08-22', 111, '09:00', '10:00'),
(12, '2026-08-23', 112, '11:00', '12:00'),
(13, '2026-08-24', 113, '13:00', '14:00'),
(14, '2026-08-25', 114, '15:00', '16:00'),
(15, '2026-08-26', 115, '10:00', '11:00');

INSERT INTO Events (EventName, Audience, RoomNumber, EventDate, StartTime, EndTime) VALUES
('Picture Book Storytime', 'Kids', 101, '2026-08-12', '10:00', '11:00'),
('Teen Manga Club', 'Teens', 103, '2026-08-13', '15:00', '16:30'),
('Author Talk: Local Sci-Fi Writers', 'Adults', 105, '2026-08-14', '18:00', '19:30'),
('Senior Tech Help Hour', 'Seniors', 106, '2026-08-15', '13:00', '14:00'),
('Community Film Screening', 'General', 105, '2026-08-16', '19:00', '21:00'),
('Book Club: Sci-Fi Picks', 'Adults', 103, '2026-08-17', '17:00', '18:30'),
('Art Show: Local Painters', 'General', 108, '2026-08-18', '12:00', '17:00'),
('Toddler Craft Hour', 'Kids', 101, '2026-08-19', '10:30', '11:30'),
('Teen Volunteer Orientation', 'Teens', 106, '2026-08-20', '16:00', '17:00'),
('Genealogy Workshop', 'Seniors', 106, '2026-08-21', '14:00', '15:30'),

('Poetry Night', 'Adults', 111, '2026-08-27', '18:00', '19:30'),
('Kids Puppet Show', 'Kids', 112, '2026-08-28', '10:00', '11:00'),
('Teen Trivia Night', 'Teens', 113, '2026-08-29', '16:00', '17:30'),
('Senior Chess Club', 'Seniors', 114, '2026-08-30', '13:00', '15:00'),
('Community Potluck', 'General', 115, '2026-08-31', '17:00', '19:00');

INSERT INTO EventRegistration (EventID, CustomerID) VALUES
(1, 6), (2, 8), (3, 1), (4, 5), (5, 2),
(6, 4), (7, 9), (8, 3), (9, 10), (10, 7),

(11, 11), (12, 12), (13, 13), (14, 14), (15, 15);

INSERT INTO HelpRequests (CustomerID, Request, RequestTimestamp, Response) VALUES
(1, 'Need help finding books on machine learning.', '2026-07-01 10:00:00', 'Here is a list of machine learning books in section 006.3.'),
(2, 'How do I renew a loan online?', '2026-07-02 10:00:00', 'You can renew under the "My Account" section of the catalog.'),
(3, 'Looking for large-print books.', '2026-07-03 10:00:00', NULL),
(4, 'Question about my account balance.', '2026-07-04 10:00:00', 'Your current balance has been cleared.'),
(5, 'Need help using the microfilm reader.', '2026-07-05 10:00:00', NULL),
(6, 'Where can I find local newspaper archives?', '2026-07-06 10:00:00', 'They are located on the second floor in the archives room.'),
(7, 'Interested in booking a room for a study group.', '2026-07-07 10:00:00', NULL),
(8, 'Asking about interlibrary loan process.', '2026-07-08 10:00:00', 'Forms are available at the front desk for interlibrary loans.'),
(9, 'Need a printout of my event registration.', '2026-07-09 10:00:00', NULL),
(10, 'Question about volunteering hours logged.', '2026-07-10 10:00:00', 'Your logged hours have been verified and updated.'),

(11, 'Need help finding the periodicals section.', '2026-07-11 10:00:00', NULL),
(12, 'Question about donating old textbooks.', '2026-07-12 10:00:00', 'We accept textbook donations published within the last 5 years.'),
(13, 'Trouble logging into the online catalog.', '2026-07-13 10:00:00', NULL),
(14, 'Asking about study room availability.', '2026-07-14 10:00:00', 'Study room 3 is available tomorrow at 2 PM.'),
(15, 'Need help with the self-checkout kiosk.', '2026-07-15 10:00:00', NULL);

