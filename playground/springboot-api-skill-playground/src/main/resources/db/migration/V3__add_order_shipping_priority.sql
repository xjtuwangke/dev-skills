ALTER TABLE orders
  ADD COLUMN shipping_priority VARCHAR(32) NOT NULL DEFAULT 'STANDARD',
  ADD COLUMN requested_ship_date DATE,
  ADD COLUMN manual_review_required BOOLEAN NOT NULL DEFAULT FALSE;
