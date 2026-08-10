PRAGMA foreign_keys = ON;


CREATE TABLE Authors (
    AuthorID INTEGER PRIMARY KEY AUTOINCREMENT,
    AuthorName TEXT NOT NULL
);


CREATE TABLE Media (
    MediaID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    Type TEXT NOT NULL CHECK (Type IN ('Print Book','Online Book','Magazine','Scientific Journal','Record')),
    PublicationDate DATE
);


CREATE TABLE MediaAuthors (
    MediaID INTEGER NOT NULL,
    AuthorID INTEGER NOT NULL,
    PRIMARY KEY (MediaID, AuthorID),
    FOREIGN KEY (MediaID) REFERENCES Media(MediaID),
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID)
);


CREATE TABLE CandidateMedia (
    CandidateID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    Type TEXT NOT NULL,
    PublicationDate DATE,
    DonatedBy INTEGER,
    FOREIGN KEY (DonatedBy) REFERENCES Customers(CustomerID)
);


CREATE TABLE Customers (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    DOB DATE,
    Balance REAL NOT NULL DEFAULT 0 CHECK (Balance >= 0)
);


CREATE TABLE Loans (
    MediaID INTEGER NOT NULL,
    CheckoutDate DATE NOT NULL,
    CustomerID INTEGER NOT NULL,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    PRIMARY KEY (MediaID, CheckoutDate),
    FOREIGN KEY (MediaID) REFERENCES Media(MediaID),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);


CREATE TABLE Rooms (
    RoomNumber INTEGER PRIMARY KEY,
    Capacity INTEGER NOT NULL CHECK (Capacity > 0)
);


CREATE TABLE Bookings (
    CustomerID INTEGER NOT NULL,
    BookingDate DATE NOT NULL,
    RoomNumber INTEGER NOT NULL,
    StartTime TEXT NOT NULL,
    EndTime TEXT NOT NULL,
    PRIMARY KEY (CustomerID, BookingDate),
    FOREIGN KEY (RoomNumber) REFERENCES Rooms(RoomNumber),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);


CREATE TABLE Events (
    EventID INTEGER PRIMARY KEY AUTOINCREMENT,
    EventName TEXT NOT NULL,
    Audience TEXT NOT NULL CHECK (Audience IN ('Kids','Teens','Adults','Seniors','General')),
    RoomNumber INTEGER NOT NULL,
    EventDate DATE NOT NULL,
    StartTime TEXT NOT NULL,
    EndTime TEXT NOT NULL,
    FOREIGN KEY (RoomNumber) REFERENCES Rooms(RoomNumber)
);


CREATE TABLE EventRegistration (
    EventID INTEGER NOT NULL,
    CustomerID INTEGER NOT NULL,
    PRIMARY KEY (EventID, CustomerID),
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);


CREATE TABLE Employees (
    Email TEXT PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Position TEXT NOT NULL,
    PhoneNum TEXT,
    DOB DATE,
    DateHired DATE DEFAULT CURRENT_DATE
);

CREATE TABLE HelpRequests (
    CustomerID INTEGER NOT NULL,
    Request TEXT NOT NULL,
    RequestTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Response TEXT,
    PRIMARY KEY(CustomerID, RequestTimestamp),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);


-- can't borrow if you still owe money
CREATE TRIGGER trg_check_balance_before_borrow
BEFORE INSERT ON Loans
FOR EACH ROW
WHEN (SELECT Balance FROM Customers WHERE CustomerID = NEW.CustomerID) != 0
BEGIN
    SELECT RAISE(ABORT, 'Customer has an outstanding balance and cannot borrow.');
END;


-- stops the same item being checked out twice
CREATE TRIGGER trg_no_double_loan
BEFORE INSERT ON Loans
FOR EACH ROW
WHEN EXISTS (
    SELECT 1 FROM Loans WHERE MediaID = NEW.MediaID AND ReturnDate IS NULL
)
BEGIN
    SELECT RAISE(ABORT, 'This item is already checked out.');
END;


-- adds a $5 fine when something comes back late
CREATE TRIGGER trg_apply_late_fine
AFTER UPDATE OF ReturnDate ON Loans
FOR EACH ROW
WHEN NEW.ReturnDate IS NOT NULL AND NEW.ReturnDate > NEW.DueDate
BEGIN
    UPDATE Customers
    SET Balance = Balance + 5.00
    WHERE CustomerID = NEW.CustomerID;
END;


-- no booking a room that's already got an event that day
CREATE TRIGGER trg_no_booking_during_event
BEFORE INSERT ON Bookings
FOR EACH ROW
WHEN EXISTS (
    SELECT 1 FROM Events WHERE RoomNumber = NEW.RoomNumber AND EventDate = NEW.BookingDate
)
BEGIN
    SELECT RAISE(ABORT, 'Room is reserved for an event on this date.');
END;

