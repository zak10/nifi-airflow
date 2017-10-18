CREATE TABLE public.test_data
(
    product_id VARCHAR(255),
    orders int,
    revenue DECIMAL,
    unit_sales int,
    views int,
    price DECIMAL
);

CREATE TABLE public.test_data_2
(
    site_id int,
    product_id VARCHAR(255),
    date DATE,
    orders int,
    revenue DECIMAL,
    unit_sales int,
    views int,
    price DECIMAL
);