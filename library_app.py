import sqlite3
import datetime

DATABASE = "library.db"

def connect():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def find_item():
    keyword = input("Enter a title keyword to search for: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT MediaID, Title, Type, PublicationDate FROM Media WHERE Title LIKE ?", ("%" + keyword + "%",))
    results = cur.fetchall()

    if not results:
        print("No items found.")


    for media_id, title, mtype, pub_date in results:
        cur.execute("SELECT ReturnDate FROM Loans WHERE MediaID = ? ORDER BY CheckoutDate DESC LIMIT 1", (media_id,))
        loan = cur.fetchone()
        status = "Available"

        if loan and loan[0] is None:
            status = "Checked out"
        print("[" + str(media_id) + "] " + title + " (" + mtype + ", " + str(pub_date) + ") - " + status)

    conn.close()

def borrow_item():
    customer_id = input("Enter your Customer ID: ")
    media_id = input("Enter the Media ID you want to borrow: ")
    checkout_date = str(datetime.date.today())
    due_date = str(datetime.date.today() + datetime.timedelta(days=14))

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT Balance FROM Customers WHERE CustomerID = ?", (customer_id,))
    balance = cur.fetchone()
    cur.execute("SELECT 1 FROM Media WHERE MediaID = ?", (media_id,))
    media_exists = cur.fetchone()
    cur.execute("SELECT 1 FROM Loans WHERE MediaID = ? AND ReturnDate IS NULL", (media_id,))
    already_out = cur.fetchone()

    if balance is None:
        print("Customer not found.")

    elif media_exists is None:
        print("Item not found.")

    elif balance[0] != 0:
        print("You have an outstanding balance and cannot borrow.")

    elif already_out is not None:
        print("This item is already checked out.")

    else:
        cur.execute("INSERT INTO Loans (MediaID, CheckoutDate, CustomerID, DueDate) VALUES (?, ?, ?, ?)",
                     (media_id, checkout_date, customer_id, due_date))
        conn.commit()
        print("Borrowed successfully. Due date: " + due_date)

    conn.close()


def return_item():
    customer_id = input("Enter your Customer ID: ")
    media_id = input("Enter the Media ID you're returning: ")
    
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT CheckoutDate FROM Loans WHERE MediaID = ? AND CustomerID = ? AND ReturnDate IS NULL",
                (media_id, customer_id))
    row = cur.fetchone()

    if row is None:
        print("No active loan found for that item and customer.")
        conn.close()
        return
    
    return_date = str(datetime.date.today())
    cur.execute("UPDATE Loans SET ReturnDate = ? WHERE MediaID = ? AND CheckoutDate = ?",
                (return_date, media_id, row[0]))
    
    conn.commit()
    conn.close()
    print("Item returned. Thanks!")


def donate_item():
    title = input("Title of the item you're donating: ")
    mtype = input("Type (Print Book/Online Book/Magazine/Scientific Journal/Record): ")
    pub_date = input("Publication date (YYYY-MM-DD, leave blank if unknown): ") or None
    customer_id = input("Your Customer ID: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM Customers WHERE CustomerID = ?", (customer_id,))
    customer_exists = cur.fetchone()

    if customer_exists is None:
        print("Customer not found.")

    else:
        cur.execute("INSERT INTO CandidateMedia (Title, Type, PublicationDate, DonatedBy) VALUES (?, ?, ?, ?)",
                    (title, mtype, pub_date, customer_id))
        conn.commit()
        print("Thanks for the donation! It'll be reviewed for addition to the collection.")
        
    conn.close()

def find_event():
    keyword = input("Enter an event name keyword (or leave blank for all upcoming events): ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT EventID, EventName, Audience, EventDate, StartTime, EndTime FROM Events "
                "WHERE EventName LIKE ? ORDER BY EventDate", ("%" + keyword + "%",))
    results = cur.fetchall()

    conn.close()

    if not results:
        print("No events found.")


    for event_id, name, audience, edate, start, end in results:
        print("[" + str(event_id) + "] " + name + " - " + audience + " - " + edate + " " + start + "-" + end)


def register_for_event():
    customer_id = input("Enter your Customer ID: ")
    event_id = input("Enter the Event ID: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM Customers WHERE CustomerID = ?", (customer_id,))
    customer_exists = cur.fetchone()
    cur.execute("SELECT 1 FROM Events WHERE EventID = ?", (event_id,))
    event_exists = cur.fetchone()
    cur.execute("SELECT 1 FROM EventRegistration WHERE EventID = ? AND CustomerID = ?", (event_id, customer_id))
    already_registered = cur.fetchone()

    if customer_exists is None:
        print("Customer not found.")

    elif event_exists is None:
        print("Event not found.")

    elif already_registered is not None:
        print("You're already registered for this event.")

    else:
        cur.execute("INSERT INTO EventRegistration (EventID, CustomerID) VALUES (?, ?)", (event_id, customer_id))
        conn.commit()
        print("Registered for the event!")

    conn.close()


def volunteer():
    customer_id = input("Enter your Customer ID: ")
    availability = input("What's your availability (e.g. Weekday evenings)? ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM Customers WHERE CustomerID = ?", (customer_id,))
    customer_exists = cur.fetchone()
    cur.execute("SELECT 1 FROM Volunteers WHERE CustomerID = ?", (customer_id,))
    already_volunteer = cur.fetchone()

    if customer_exists is None:
        print("Customer not found.")

    elif already_volunteer is not None:
        print("You're already signed up to volunteer.")

    else:
        cur.execute("INSERT INTO Volunteers (CustomerID, Availability) VALUES (?, ?)", (customer_id, availability))
        conn.commit()
        print("Thanks for volunteering! The Volunteer Coordinator will reach out.")

    conn.close()

def ask_for_help():
    customer_id = input("Enter your Customer ID: ")
    message = input("What do you need help with? ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM Customers WHERE CustomerID = ?", (customer_id,))
    customer_exists = cur.fetchone()

    if customer_exists is None:
        print("Customer not found.")

    else:
        cur.execute("INSERT INTO HelpRequests (CustomerID, Message) VALUES (?, ?)", (customer_id, message))
        conn.commit()
        print("Your request has been sent to a librarian.")

    conn.close()


def main():
    print("Welcome to the Library!")

    while True:
        print("1. Find an item")
        print("2. Borrow an item")
        print("3. Return an item")
        print("4. Donate an item")
        print("5. Find an event")
        print("6. Register for an event")
        print("7. Volunteer for the library")
        print("8. Ask for help from a librarian")
        print("9. Exit")
        choice = input("Choose an option (1-9): ")

        if choice == "1":
            find_item()
        elif choice == "2":
            borrow_item()
        elif choice == "3":
            return_item()
        elif choice == "4":
            donate_item()
        elif choice == "5":
            find_event()
        elif choice == "6":
            register_for_event()
        elif choice == "7":
            volunteer()
        elif choice == "8":
            ask_for_help()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Not a valid option, try again.")

main()

