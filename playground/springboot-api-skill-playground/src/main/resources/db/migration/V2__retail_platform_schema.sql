CREATE TABLE customer_accounts (
  id UUID PRIMARY KEY,
  external_customer_id VARCHAR(64) NOT NULL UNIQUE,
  segment VARCHAR(32) NOT NULL,
  status VARCHAR(32) NOT NULL,
  default_currency VARCHAR(3) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE customer_addresses (
  id UUID PRIMARY KEY,
  customer_account_id UUID NOT NULL REFERENCES customer_accounts (id),
  address_type VARCHAR(32) NOT NULL,
  line1 VARCHAR(128) NOT NULL,
  city VARCHAR(64) NOT NULL,
  region VARCHAR(64) NOT NULL,
  postal_code VARCHAR(32) NOT NULL,
  country VARCHAR(2) NOT NULL
);

CREATE TABLE customer_contact_preferences (
  id UUID PRIMARY KEY,
  customer_account_id UUID NOT NULL REFERENCES customer_accounts (id),
  channel VARCHAR(32) NOT NULL,
  enabled BOOLEAN NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE loyalty_accounts (
  id UUID PRIMARY KEY,
  customer_account_id UUID NOT NULL REFERENCES customer_accounts (id),
  points_balance INTEGER NOT NULL,
  tier VARCHAR(32) NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE product_categories (
  id UUID PRIMARY KEY,
  code VARCHAR(64) NOT NULL UNIQUE,
  parent_code VARCHAR(64),
  name VARCHAR(128) NOT NULL
);

CREATE TABLE products (
  id UUID PRIMARY KEY,
  sku VARCHAR(64) NOT NULL UNIQUE,
  category_code VARCHAR(64) NOT NULL,
  name VARCHAR(128) NOT NULL,
  status VARCHAR(32) NOT NULL,
  hazardous BOOLEAN NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE product_variants (
  id UUID PRIMARY KEY,
  product_id UUID NOT NULL REFERENCES products (id),
  variant_code VARCHAR(64) NOT NULL,
  color VARCHAR(64),
  size_code VARCHAR(32),
  UNIQUE (product_id, variant_code)
);

CREATE TABLE suppliers (
  id UUID PRIMARY KEY,
  supplier_code VARCHAR(64) NOT NULL UNIQUE,
  display_name VARCHAR(128) NOT NULL,
  status VARCHAR(32) NOT NULL
);

CREATE TABLE product_supplier_contracts (
  id UUID PRIMARY KEY,
  product_id UUID NOT NULL REFERENCES products (id),
  supplier_id UUID NOT NULL REFERENCES suppliers (id),
  lead_time_days INTEGER NOT NULL,
  minimum_order_quantity INTEGER NOT NULL
);

CREATE TABLE inventory_locations (
  id UUID PRIMARY KEY,
  location_code VARCHAR(64) NOT NULL UNIQUE,
  region VARCHAR(64) NOT NULL,
  supports_hazardous BOOLEAN NOT NULL
);

CREATE TABLE inventory_stocks (
  id UUID PRIMARY KEY,
  product_id UUID NOT NULL REFERENCES products (id),
  location_id UUID NOT NULL REFERENCES inventory_locations (id),
  on_hand INTEGER NOT NULL,
  reserved INTEGER NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL,
  UNIQUE (product_id, location_id)
);

CREATE TABLE inventory_reservations (
  id UUID PRIMARY KEY,
  order_id UUID NOT NULL,
  product_id UUID NOT NULL REFERENCES products (id),
  location_id UUID NOT NULL REFERENCES inventory_locations (id),
  quantity INTEGER NOT NULL,
  status VARCHAR(32) NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE warehouse_transfers (
  id UUID PRIMARY KEY,
  source_location_id UUID NOT NULL REFERENCES inventory_locations (id),
  target_location_id UUID NOT NULL REFERENCES inventory_locations (id),
  status VARCHAR(32) NOT NULL,
  requested_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE warehouse_transfer_lines (
  id UUID PRIMARY KEY,
  transfer_id UUID NOT NULL REFERENCES warehouse_transfers (id),
  product_id UUID NOT NULL REFERENCES products (id),
  quantity INTEGER NOT NULL
);

CREATE TABLE price_lists (
  id UUID PRIMARY KEY,
  code VARCHAR(64) NOT NULL UNIQUE,
  currency VARCHAR(3) NOT NULL,
  status VARCHAR(32) NOT NULL,
  effective_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE price_list_items (
  id UUID PRIMARY KEY,
  price_list_id UUID NOT NULL REFERENCES price_lists (id),
  product_id UUID NOT NULL REFERENCES products (id),
  unit_price NUMERIC(12, 2) NOT NULL,
  UNIQUE (price_list_id, product_id)
);

CREATE TABLE tax_rates (
  id UUID PRIMARY KEY,
  country VARCHAR(2) NOT NULL,
  region VARCHAR(64) NOT NULL,
  rate NUMERIC(8, 6) NOT NULL,
  effective_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE promotion_campaigns (
  id UUID PRIMARY KEY,
  code VARCHAR(64) NOT NULL UNIQUE,
  status VARCHAR(32) NOT NULL,
  starts_at TIMESTAMPTZ NOT NULL,
  ends_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE coupons (
  id UUID PRIMARY KEY,
  campaign_id UUID NOT NULL REFERENCES promotion_campaigns (id),
  coupon_code VARCHAR(64) NOT NULL UNIQUE,
  discount_type VARCHAR(32) NOT NULL,
  discount_value NUMERIC(12, 2) NOT NULL,
  max_redemptions INTEGER NOT NULL
);

CREATE TABLE coupon_redemptions (
  id UUID PRIMARY KEY,
  coupon_id UUID NOT NULL REFERENCES coupons (id),
  customer_account_id UUID NOT NULL REFERENCES customer_accounts (id),
  order_id UUID NOT NULL,
  redeemed_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE sales_orders (
  id UUID PRIMARY KEY,
  public_order_id UUID NOT NULL UNIQUE,
  customer_account_id UUID NOT NULL REFERENCES customer_accounts (id),
  status VARCHAR(32) NOT NULL,
  subtotal NUMERIC(12, 2) NOT NULL,
  tax NUMERIC(12, 2) NOT NULL,
  total NUMERIC(12, 2) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE order_lines (
  id UUID PRIMARY KEY,
  sales_order_id UUID NOT NULL REFERENCES sales_orders (id),
  product_id UUID NOT NULL REFERENCES products (id),
  quantity INTEGER NOT NULL,
  unit_price NUMERIC(12, 2) NOT NULL,
  line_total NUMERIC(12, 2) NOT NULL
);

CREATE TABLE order_status_history (
  id UUID PRIMARY KEY,
  sales_order_id UUID NOT NULL REFERENCES sales_orders (id),
  from_status VARCHAR(32),
  to_status VARCHAR(32) NOT NULL,
  changed_by VARCHAR(128) NOT NULL,
  changed_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE idempotency_keys (
  id UUID PRIMARY KEY,
  operation_key VARCHAR(128) NOT NULL UNIQUE,
  request_hash VARCHAR(128) NOT NULL,
  response_status INTEGER NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE payment_methods (
  id UUID PRIMARY KEY,
  customer_account_id UUID NOT NULL REFERENCES customer_accounts (id),
  token_reference VARCHAR(128) NOT NULL,
  brand VARCHAR(32) NOT NULL,
  last_four VARCHAR(4) NOT NULL,
  status VARCHAR(32) NOT NULL
);

CREATE TABLE payments (
  id UUID PRIMARY KEY,
  sales_order_id UUID NOT NULL REFERENCES sales_orders (id),
  amount NUMERIC(12, 2) NOT NULL,
  currency VARCHAR(3) NOT NULL,
  status VARCHAR(32) NOT NULL,
  authorized_at TIMESTAMPTZ
);

CREATE TABLE payment_attempts (
  id UUID PRIMARY KEY,
  payment_id UUID NOT NULL REFERENCES payments (id),
  processor VARCHAR(64) NOT NULL,
  processor_reference VARCHAR(128),
  status VARCHAR(32) NOT NULL,
  attempted_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE shipments (
  id UUID PRIMARY KEY,
  sales_order_id UUID NOT NULL REFERENCES sales_orders (id),
  location_id UUID NOT NULL REFERENCES inventory_locations (id),
  carrier VARCHAR(64) NOT NULL,
  service_level VARCHAR(64) NOT NULL,
  status VARCHAR(32) NOT NULL,
  estimated_ship_date DATE NOT NULL
);

CREATE TABLE shipment_items (
  id UUID PRIMARY KEY,
  shipment_id UUID NOT NULL REFERENCES shipments (id),
  order_line_id UUID NOT NULL REFERENCES order_lines (id),
  quantity INTEGER NOT NULL
);

CREATE TABLE return_requests (
  id UUID PRIMARY KEY,
  sales_order_id UUID NOT NULL REFERENCES sales_orders (id),
  status VARCHAR(32) NOT NULL,
  reason_code VARCHAR(64) NOT NULL,
  requested_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE return_items (
  id UUID PRIMARY KEY,
  return_request_id UUID NOT NULL REFERENCES return_requests (id),
  order_line_id UUID NOT NULL REFERENCES order_lines (id),
  quantity INTEGER NOT NULL,
  disposition VARCHAR(64) NOT NULL
);

CREATE TABLE support_tickets (
  id UUID PRIMARY KEY,
  customer_account_id UUID NOT NULL REFERENCES customer_accounts (id),
  order_id UUID,
  status VARCHAR(32) NOT NULL,
  priority VARCHAR(32) NOT NULL,
  subject VARCHAR(256) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE ticket_messages (
  id UUID PRIMARY KEY,
  ticket_id UUID NOT NULL REFERENCES support_tickets (id),
  author_type VARCHAR(32) NOT NULL,
  body TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE audit_logs (
  id UUID PRIMARY KEY,
  subject_type VARCHAR(64) NOT NULL,
  subject_id UUID NOT NULL,
  event_type VARCHAR(64) NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE outbox_events (
  id UUID PRIMARY KEY,
  aggregate_type VARCHAR(64) NOT NULL,
  aggregate_id UUID NOT NULL,
  topic VARCHAR(128) NOT NULL,
  payload JSONB NOT NULL,
  status VARCHAR(32) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE feature_flags (
  id UUID PRIMARY KEY,
  flag_key VARCHAR(128) NOT NULL UNIQUE,
  enabled BOOLEAN NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_sales_orders_customer ON sales_orders (customer_account_id);
CREATE INDEX idx_order_lines_order ON order_lines (sales_order_id);
CREATE INDEX idx_inventory_stocks_product ON inventory_stocks (product_id);
CREATE INDEX idx_outbox_events_status ON outbox_events (status);
CREATE INDEX idx_audit_logs_subject ON audit_logs (subject_type, subject_id);
