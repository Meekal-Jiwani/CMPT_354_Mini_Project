import sqlite3
import datetime
import os

DATABASE = "library.db"

# Clear the terminal to improve menu readability
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
# Connect to the database and enable foreign key support
def connect():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Search for items by title keyword and display their availability
def search_by_title():
    keyword = input("Enter a title keyword to search for: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT MediaID, Title, Type, PublicationDate FROM Media WHERE Title LIKE ?", ("%" + keyword + "%",))
    results = cur.fetchall()

    clear_screen()
    print("\nMatches:")
    if not results:
        print("No items found.")


    
    for media_id, title, mtype, pub_date in results:
        # Check most recent loan to see if it's out or not
        cur.execute("SELECT ReturnDate, DueDate FROM Loans WHERE MediaID = ? ORDER BY CheckoutDate DESC LIMIT 1", (media_id,))
        loan = cur.fetchone()
        status = "Available"

        if loan and loan[0] is None:
            status = "Checked out until " + str(loan[1])
        print("[" + str(media_id) + "] " + title + " (" + mtype + ", " + str(pub_date) + ") - " + status)

    conn.close()

# Search for items by author name and display their availability
def search_by_author():
    keyword = input("Enter an author name keyword to search for: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT m.MediaID, m.Title, m.Type, m.PublicationDate, a.AuthorName FROM Media m
        JOIN MediaAuthors ma ON m.MediaID = ma.MediaID
        JOIN Authors a ON ma.AuthorID = a.AuthorID
        WHERE a.AuthorName LIKE ?
    """, ("%" + keyword + "%",))
    
    results = cur.fetchall()

    clear_screen()
    print("\nMatches:")
    if not results:
        print("No items found.")

    
    for media_id, title, mtype, pub_date, author_name in results:
        # Check most recent loan to see if it's out or not
        cur.execute("SELECT ReturnDate, DueDate FROM Loans WHERE MediaID = ? ORDER BY CheckoutDate DESC LIMIT 1", (media_id,))
        loan = cur.fetchone()
        status = "Available"

        if loan and loan[0] is None:
            status = "Checked out until " + str(loan[1])
        print("[" + str(media_id) + "] " + title + " by " + author_name + " (" + mtype + ", " + str(pub_date) + ") - " + status)

    conn.close()

def find_item():
    clear_screen()
    print("Item Search")
    print("1. Search by Title")
    print("2. Search by Author")
    print("3. Return to the Main Menu")
    choice = input("\nChoose an option (1-3): ")
    print("")

    if choice == "1":
        search_by_title()
    elif choice == "2":
        search_by_author()
    elif choice == "3":
        clear_screen()
        return
    else:
        clear_screen()
        print("Not a valid option, try again.")


# Borrow an item if the customer has no outstanding balance and the item is available
def borrow_item():
    clear_screen()
    print("Borrow an item \n")
    customer_id = input("Enter your Customer ID: ")
    media_id = input("Enter the Media ID you want to borrow: ")
    checkout_date = str(datetime.date.today())
    due_date = str(datetime.date.today() + datetime.timedelta(days=14))  # 2 week loan period

    conn = connect()
    cur = conn.cursor()

    # Check customer and item are valid before doing anything
    cur.execute("SELECT Balance FROM Customers WHERE CustomerID = ?", (customer_id,))
    balance = cur.fetchone()
    cur.execute("SELECT 1 FROM Media WHERE MediaID = ?", (media_id,))
    media_exists = cur.fetchone()
    cur.execute("SELECT 1 FROM Loans WHERE MediaID = ? AND ReturnDate IS NULL", (media_id,))
    already_out = cur.fetchone()

    clear_screen()
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
        print("\nBorrowed successfully. Due date: " + due_date + "\n")

    conn.close()


# Return an item if the customer has an active loan for it
def return_item():
    clear_screen()
    print("Return an Item\n")
    customer_id = input("Enter your Customer ID: ")
    media_id = input("Enter the Media ID you're returning: ")
    clear_screen()

    conn = connect()
    cur = conn.cursor()

    # Need the checkout date since it's part of the primary key
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
    print("\nItem returned. Thanks!\n")


# Donate an item, which will be reviewed for addition to the collection
def donate_item():
    clear_screen()
    print("Donating an item\n")
    title = input("Title of the item you're donating: ")
    
    mtype = input("Type (Print Book/Online Book/Magazine/Scientific Journal/Record): ")
    clear_screen()

    valid_types = ['Print Book', 'Online Book', 'Magazine', 'Scientific Journal', 'Record']
    if mtype not in valid_types:
        print("Invalid type. It must be exactly one of the options provided.")
        return

    pub_date = input("Publication date (YYYY-MM-DD, leave blank if unknown): ") or None  # blank becomes NULL
    if pub_date is not None:
        try:
            # Validates that the string matches the exact date format
            datetime.datetime.strptime(pub_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD and enter a valid date.")
            return

    customer_id = input("Your Customer ID: ")

    clear_screen()
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
        print("\nThanks for the donation! It'll be reviewed for addition to the collection.\n")
        
    conn.close()
    
# Find upcoming events by name keyword
def find_event():
    clear_screen()
    print("Searching for an Event\n")
    keyword = input("Enter an event name keyword (or leave blank for all upcoming events): ")
    clear_screen()

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT EventID, EventName, Audience, EventDate, StartTime, EndTime FROM Events "
                "WHERE EventName LIKE ? ORDER BY EventDate", ("%" + keyword + "%",))
    results = cur.fetchall()

    conn.close()

    if not results:
        print("No events found.")

    print("\nMatches:")
    for event_id, name, audience, edate, start, end in results:
        print("[" + str(event_id) + "] " + name + " - " + audience + " - " + edate + " " + start + "-" + end)
    print()

# Register a customer for an event if they haven't already signed up
def register_for_event():
    clear_screen()
    print("Registering for an event\n")
    customer_id = input("Enter your Customer ID: ")
    event_id = input("Enter the Event ID: ")
    clear_screen()

    conn = connect()
    cur = conn.cursor()

    # Make sure both IDs exist and they're not already signed up
    cur.execute("SELECT 1 FROM Customers WHERE CustomerID = ?", (customer_id,))
    customer_exists = cur.fetchone()
    
    # Changed to select EventName so we can use it in the success message
    cur.execute("SELECT EventName FROM Events WHERE EventID = ?", (event_id,))
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
        
        # event_exists[0] contains the EventName we fetched earlier
        event_name = event_exists[0]
        print("\nSuccessfully registered for the event: " + event_name + "!")

    conn.close()


# Volunteer a customer for the library if they haven't already signed up
def volunteer():
    clear_screen()
    print("Register as a volunteer\n")
    customer_id = input("Enter your Customer ID: ")
    email = input("Enter your Email address: ")
    clear_screen()

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT FirstName, LastName, DOB FROM Customers WHERE CustomerID = ?", (customer_id,))
    customer = cur.fetchone()
    cur.execute("SELECT 1 FROM Employees WHERE Email = ?", (email,))
    already_employee = cur.fetchone()

    if customer is None:
        print("Customer not found.")

    elif already_employee is not None:
        print("You are already an employee or have registered this email.")

    else:
        date_hired = str(datetime.date.today())
        cur.execute("INSERT INTO Employees (Email, FirstName, LastName, Position, DOB, DateHired) VALUES (?, ?, ?, ?, ?, ?)",
                    (email, customer[0], customer[1], 'Volunteer', customer[2], date_hired))
        conn.commit()
        print("\nThanks for volunteering! You have been added as an employee with a Volunteer position.")

    conn.close()

# Show a specific customer all their requests and answers
def see_help_requests():
    clear_screen()
    print("Check your requests\n")
    customer_id = input("Enter your Customer ID: ")

    clear_screen()
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("SELECT 1 FROM Customers WHERE CustomerID = ?", (customer_id,))
    if cur.fetchone() is None:
        print("Customer not found.")
    else:
        # Changed to RequestTimestamp and removed responseDate
        cur.execute("SELECT RequestTimestamp, Request, Response FROM HelpRequests WHERE CustomerID = ? ORDER BY RequestTimestamp DESC", (customer_id,))
        requests = cur.fetchall()

        if not requests:
            print("No help requests found for this account.")
        else:
            print("\nMatches:")
            for rstamp, req, res in requests:
                if res:
                    print("[" + str(rstamp) + "] Request: " + str(req) + "\n  Response: " + str(res))
                else:
                    print("[" + str(rstamp) + "] Request: " + str(req) + "\n  Response: Pending")
            print()

    conn.close()

def create_request():
    clear_screen()
    print("Create a help request\n")
    customer_id = input("Enter your Customer ID: ")
    request = input("What do you need help with? ")
    # request_date generation removed; DB will handle DEFAULT CURRENT_TIMESTAMP
    clear_screen()
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM Customers WHERE CustomerID = ?", (customer_id,))
    customer_exists = cur.fetchone()

    if customer_exists is None:
        print("Customer not found.")
    else:
        try:
            # Let SQL apply the DEFAULT CURRENT_TIMESTAMP
            cur.execute("INSERT INTO HelpRequests (CustomerID, Request) VALUES (?, ?)", (customer_id, request))
            conn.commit()
            print("Your request has been sent to a librarian.")
        except sqlite3.IntegrityError:
            print("You have already submitted an identical request at this exact time.")

    conn.close()

# Ask for help from a librarian sub-menu
def ask_for_help():
    
    while True:
        print("\nHelp Menu:")
        print("1. Create a help request")
        print("2. See my help requests")
        print("3. Back to main menu")
        choice = input("Choose an option (1-3): ")
        print("")

        if choice == "1":
            create_request()
        elif choice == "2":
            see_help_requests()
        elif choice == "3":
            clear_screen()
            break
        else:
            clear_screen()
            print("Not a valid option, try again.")

# Let an employee answer a pending help request
def answer_help_request(Email):
    clear_screen()
    print("Select a request to respond to\n")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM Employees WHERE Email = ?", (Email,))
    employee_exists = cur.fetchone()

    if employee_exists is None:
        print("Invalid employee email.")
    else:
        # Changed to RequestTimestamp and capitalized columns
        cur.execute("SELECT CustomerID, RequestTimestamp, Request FROM HelpRequests WHERE Response IS NULL")
        requests = cur.fetchall()

        if not requests:
            print("No pending help requests.")
        else:
            print("Pending Requests:")
            for cid, rstamp, req in requests:
                print("[" + str(cid) + " on " + str(rstamp) + "] " + str(req))
            
            customer_id = input("\nEnter the Customer ID to answer: ")
            request_timestamp = input("Enter the request timestamp to answer (exactly as shown): ")
            response = input("Enter your response: ")
            
            # Removed responseDate from the UPDATE
            cur.execute("UPDATE HelpRequests SET Response = ? WHERE CustomerID = ? AND RequestTimestamp = ? AND Response IS NULL",
                        (response, customer_id, request_timestamp))
            
            clear_screen()
            if cur.rowcount > 0:
                conn.commit()
                print("\nResponse recorded successfully.")
            else:
                print("\nRequest not found or it was already answered.")

    conn.close()

# Let an employee review donated items and add them to the main collection
def review_donations(Email):
    clear_screen()
    print("Select candidate media to add to the catalogue\n")
    

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM Employees WHERE Email = ?", (Email,))
    employee_exists = cur.fetchone()



    cur.execute("SELECT CandidateID, Title, Type, PublicationDate, DonatedBy FROM CandidateMedia")
    candidates = cur.fetchall()

    if not candidates:
        print("No pending donations to review.")
        conn.close()
        return

    print("Pending Donations:")
    for cid, title, mtype, pdate, donor in candidates:
        print("[" + str(cid) + "] '" + title + "' (" + mtype + ", " + str(pdate) + ") - Donated by Customer " + str(donor))

    candidate_id = input("\nEnter the Candidate ID to approve (or leave blank to cancel): ")
    if not candidate_id:
        conn.close()
        return

    cur.execute("SELECT Title, Type, PublicationDate FROM CandidateMedia WHERE CandidateID = ?", (candidate_id,))
    candidate = cur.fetchone()

    clear_screen()
    if candidate is None:
        print("Candidate Media ID not found.")
    else:
        title = candidate[0]
        mtype = candidate[1]
        pub_date = candidate[2]
        
        # Ask for the author so the MediaAuthors table can be correctly populated
        author_name = input("Enter the author's name for '" + title + "': ")
        
        # 1. Insert the new media item
        cur.execute("INSERT INTO Media (Title, Type, PublicationDate) VALUES (?, ?, ?)", (title, mtype, pub_date))
        media_id = cur.lastrowid
        
        # 2. Check if the author exists; if not, add them to the database
        cur.execute("SELECT AuthorID FROM Authors WHERE AuthorName = ?", (author_name,))
        author = cur.fetchone()
        if author:
            author_id = author[0]
        else:
            cur.execute("INSERT INTO Authors (AuthorName) VALUES (?)", (author_name,))
            author_id = cur.lastrowid
            
        # 3. Link the media item to the author
        cur.execute("INSERT INTO MediaAuthors (MediaID, AuthorID) VALUES (?, ?)", (media_id, author_id))
        
        # 4. Remove the item from the candidate pool
        cur.execute("DELETE FROM CandidateMedia WHERE CandidateID = ?", (candidate_id,))
        
        conn.commit()
        print("\nSuccessfully added '" + title + "' to the main library collection!")
        

    conn.close()

def employeeMenu():
    print("Note: Any input works for testing and grading purposes")
    input("Please enter the employee password: ")

    print("any valid email works. For convenience: test@library.org")
    Email = input("please enter your Email: ")

    conn = connect()
    cur = conn.cursor()

    # Fetch the employee's first and last name
    cur.execute("SELECT FirstName, LastName FROM Employees WHERE Email = ?", (Email,))
    employee = cur.fetchone()
    conn.close()

    clear_screen()
    # Ensure the employee exists before letting them access the menu
    if employee is None:
        print("\nEmail does not match any records. Returning to main menu.\n")
        return

    # Welcome back "Employee name"
    print("\nWelcome back, " + employee[0] + " " + employee[1] + "!")

    while True:
        print("Employee Menu")
        print("\n1. Answer a help Request")
        print("2. Review Candidate Media") 
        print("3. Return to the main menu.\n")
        choice = input("Please select an option (1-3): ")

        if choice == "1":
            answer_help_request(Email)
        elif choice == "2":
            review_donations(Email)
        elif choice == "3":
            clear_screen()
            break
        else:
            clear_screen()
            print("\nNot a valid option, try again.")




def main():
    # main menu loop, keeps going until they pick exit
    clear_screen()
    while True:
        print("\nLibrary Main Menu")
        print("1. Find an item")
        print("2. Borrow an item")
        print("3. Return an item")
        print("4. Donate an item")
        print("5. Find an event")
        print("6. Register for an event")
        print("7. Volunteer for the library")
        print("8. Librarian Help Menu")
        print("9. Employee Menu")
        print("0. Exit\n")
        
        choice = input("Choose an option (0-9): ")
        print()

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
            clear_screen()
            ask_for_help()
        elif choice == "9":
            clear_screen()
            employeeMenu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Not a valid option, try again.\n\n")

main()

