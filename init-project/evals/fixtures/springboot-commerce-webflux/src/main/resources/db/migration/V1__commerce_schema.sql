create table customers (
  id varchar(64) primary key,
  email varchar(255) not null,
  loyalty_tier varchar(32) not null,
  risk_score int not null
);

create table orders (
  id varchar(64) primary key,
  customer_id varchar(64) not null,
  status varchar(32) not null,
  total_amount numeric(12,2) not null,
  currency varchar(3) not null,
  created_at timestamp not null
);

create table payments (
  id varchar(64) primary key,
  order_id varchar(64) not null,
  status varchar(32) not null,
  amount numeric(12,2) not null,
  provider_ref varchar(128)
);

create table inventory_reservations (
  id varchar(64) primary key,
  order_id varchar(64) not null,
  sku varchar(64) not null,
  quantity int not null,
  status varchar(32) not null
);

