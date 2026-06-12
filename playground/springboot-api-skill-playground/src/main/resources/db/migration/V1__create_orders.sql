CREATE TABLE orders (
  id UUID PRIMARY KEY,
  customer_id VARCHAR(64) NOT NULL,
  sku VARCHAR(64) NOT NULL,
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  status VARCHAR(32) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_orders_customer_id ON orders (customer_id);
