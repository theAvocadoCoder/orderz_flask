CREATE TABLE
    IF NOT EXISTS businesses (
        business_id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_name TEXT NOT NULL,
        business_address TEXT,
        business_phonenumber TEXT,
        business_email TEXT
    );

CREATE TABLE
    IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS user_business (
        user_id INTEGER,
        business_id INTEGER,
        PRIMARY KEY (user_id, business_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (business_id) REFERENCES businesses(business_id)
    );

CREATE TABLE
    IF NOT EXISTS clients (
        client_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        client_firstname TEXT NOT NULL,
        client_lastname TEXT,
        client_email TEXT UNIQUE,
        cleint_phonenumber TEXT UNIQUE,
        client_notes TEXT
    );

CREATE TABLE
    IF NOT EXISTS client_fields (
        field_id INTEGER PRIMARY KEY,
        field_name TEXT NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS client_details (
        client_id INTEGER,
        field_id INTEGER,
        field_value TEXT NOT NULL,
        PRIMARY KEY (client_id, field_id),
        FOREIGN KEY (client_id) REFERENCES clients(client_id),
        FOREIGN KEY (field_id) REFERENCES client_fields(field_id)
    );

CREATE TABLE
    IF NOT EXISTS inventory (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        item_price DECIMAL (10, 2) NOT NULL,
        item_quantity INTEGER NOT NULL CHECK(item_quantity >= 1),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

CREATE TABLE
    IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_name TEXT,
        user_id INTEGER NOT NULL,
        business_id INTEGER NOT NULL,
        client_id INTEGER NOT NULL,
        order_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        due_date DATETIME,
        item_id INTEGER,
        item_amount INTEGER NOT NULL DEFAULT 1,
        order_price DECIMAL (10, 2),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (business_id) REFERENCES businesses(business_id),
        FOREIGN KEY (item_id) REFERENCES inventory(item_id),
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
    );

CREATE TABLE
    IF NOT EXISTS order_fields (
        field_id INTEGER PRIMARY KEY AUTOINCREMENT,
        field_name TEXT NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS order_details (
        order_id INTEGER,
        field_id INTEGER,
        field_value TEXT NOT NULL,
        PRIMARY KEY (order_id, field_id),
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (field_id) REFERENCES order_fields(field_id)
    );

CREATE TABLE
    IF NOT EXISTS invoices (
        invoice_id INTEGER,
        order_id INTEGER REFERENCES orders(order_id),
        PRIMARY KEY (invoice_id, order_id)
    );