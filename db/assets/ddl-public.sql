-- Tabla tenants
CREATE TABLE tenants (
    tenant_id SERIAL PRIMARY KEY,
    tenant_name VARCHAR(255) NOT NULL,
    schema_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla customers
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    phone VARCHAR NOT NULL,
    address VARCHAR,
    credit_limit FLOAT DEFAULT 0.0 NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Tabla orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    delivery_date TIMESTAMP,
    status VARCHAR NOT NULL DEFAULT 'pending',
    payment_method VARCHAR NOT NULL,
    id_customer INTEGER NOT NULL,
    FOREIGN KEY (id_customer) REFERENCES customers(id) ON DELETE CASCADE
);

-- Tabla products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    price FLOAT NOT NULL,
    stock INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Tabla inventory
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    stock_quantity INTEGER NOT NULL,
    restock_date TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Tabla credit_accounts
CREATE TABLE credit_accounts (
    id SERIAL PRIMARY KEY,
    credit_balance FLOAT NOT NULL,
    due_date TIMESTAMP NOT NULL,
    id_customer INTEGER NOT NULL,
    FOREIGN KEY (id_customer) REFERENCES customers(id) ON DELETE CASCADE
);

-- Tabla order_items
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    quantity INTEGER NOT NULL,
    price FLOAT NOT NULL,
    id_order INTEGER NOT NULL,
    id_product INTEGER NOT NULL,
    FOREIGN KEY (id_order) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (id_product) REFERENCES products(id) ON DELETE CASCADE
);

-- Tabla sales
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    total_amount FLOAT NOT NULL,
    id_customer INTEGER NOT NULL,
    id_order INTEGER,
    FOREIGN KEY (id_customer) REFERENCES customers(id) ON DELETE CASCADE,
    FOREIGN KEY (id_order) REFERENCES orders(id) ON DELETE SET NULL
);

-- Tabla sales_reports
CREATE TABLE sales_reports (
    id SERIAL PRIMARY KEY,
    report_type VARCHAR NOT NULL,
    report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    total_sales FLOAT NOT NULL,
    most_sold_product VARCHAR,
    least_sold_product VARCHAR,
    pending_collections FLOAT,
    id_customer INTEGER NOT NULL,
    FOREIGN KEY (id_customer) REFERENCES customers(id) ON DELETE CASCADE
);
