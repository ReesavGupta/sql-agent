from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///e-commerce-data/olist.sqlite/olist.sqlite")

print(db.dialect)

# print(db.get_usable_table_names())
print(db.get_table_info())
"""CREATE TABLE customers (
        customer_id TEXT, 
        customer_unique_id TEXT, 
        customer_zip_code_prefix INTEGER, 
        customer_city TEXT, 
        customer_state TEXT
)

/*
3 rows from customers table:
customer_id     customer_unique_id      customer_zip_code_prefix        customer_city   customer_state
06b8999e2fba1a1fbc88172c00ba8bc7        861eff4711a542e4b93843c6dd7febb0        14409   franca  SP
18955e83d337fd6b2def6b18a428ac77        290c77bc529b7ac935b93aa66c333dc3        9790    sao bernardo do campo   SP
4e7b3e00288586ebd08712fdd0374a03        060e732b5b29e8181a18229c7b0b2b5e        1151    sao paulo       SP
*/


CREATE TABLE geolocation (
        geolocation_zip_code_prefix INTEGER,
        geolocation_lat REAL,
        geolocation_lng REAL,
        geolocation_city TEXT,
        geolocation_state TEXT
)

/*
3 rows from geolocation table:
geolocation_zip_code_prefix     geolocation_lat geolocation_lng geolocation_city        geolocation_state
1037    -23.54562128115268      -46.63929204800168      sao paulo       SP
1046    -23.54608112703553      -46.64482029837157      sao paulo       SP
1046    -23.54612896641469      -46.64295148361138      sao paulo       SP
*/


CREATE TABLE leads_closed (
        mql_id TEXT,
        seller_id TEXT,
        sdr_id TEXT,
        sr_id TEXT,
        won_date TEXT,
        business_segment TEXT,
        lead_type TEXT,
        lead_behaviour_profile TEXT,
        has_company INTEGER,
        has_gtin INTEGER,
        average_stock TEXT,
        business_type TEXT,
        declared_product_catalog_size REAL,
        declared_monthly_revenue REAL
)

/*
3 rows from leads_closed table:
mql_id  seller_id       sdr_id  sr_id   won_date        business_segment        lead_type       lead_behaviour_profile  has_company     has_gtin        average_stock   business_type    declared_product_catalog_size   declared_monthly_revenue
5420aad7fec3549a85876ba1c529bd84        2c43fb513632d29b3b58df74816f1b06        a8387c01a09e99ce014107505b92388c        4ef15afb4b2723d8f3d81e51ec7afefe        2018-02-26 19:58:54      pet     online_medium   cat     None    None    None    reseller        None    0.0
a555fb36b9368110ede0f043dfc3b9a0        bbb7d7893a450660432ea6652310ebb7        09285259593c61296eef10c734121d5b        d3d1e91a157ea7f90548eef82f1955e3        2018-05-08 20:17:59      car_accessories industry        eagle   None    None    None    reseller        None    0.0
327174d3648a2d047e8940d7d15204ca        612170e34b97004b3ba37eae81836b4c        b90f87164b5f8c2cfa5c8572834dbe3f        6565aa9ce3178a5caf6171827af3a9ba        2018-06-05 17:27:23      home_appliances online_big      cat     None    None    None    reseller        None    0.0
*/


CREATE TABLE leads_qualified (
        mql_id TEXT,
        first_contact_date TEXT,
        landing_page_id TEXT,
        origin TEXT
)

/*
3 rows from leads_qualified table:
mql_id  first_contact_date      landing_page_id origin
dac32acd4db4c29c230538b72f8dd87d        2018-02-01      88740e65d5d6b056e0cda098e1ea6313        social
8c18d1de7f67e60dbd64e3c07d7e9d5d        2017-10-20      007f9098284a86ee80ddeb25d53e0af8        paid_search
b4bc852d233dfefc5131f593b538befa        2018-03-22      a7982125ff7aa3b2054c6e44f9d28522        organic_search
*/


CREATE TABLE order_items (
        order_id TEXT,
        order_item_id INTEGER,
        product_id TEXT,
        seller_id TEXT,
        shipping_limit_date TEXT,
        price REAL,
        freight_value REAL
)

/*
3 rows from order_items table:
order_id        order_item_id   product_id      seller_id       shipping_limit_date     price   freight_value
00010242fe8c5a6d1ba2dd792cb16214        1       4244733e06e7ecb4970a6e2683c13e61        48436dade18ac8b2bce089ec2a041202        2017-09-19 09:45:35     58.9    13.29    
00018f77f2f0320c557190d7a144bdd3        1       e5f2d52b802189ee658865ca93d83a8f        dd7ddc04e1b6c2c614352b383efe2d36        2017-05-03 11:05:13     239.9   19.93    
000229ec398224ef6ca0657da4fc703e        1       c777355d18b72b67abbeef9df44fd0fd        5b51032eddd242adc84c38acab88f23d        2018-01-18 14:48:30     199.0   17.87    
*/


CREATE TABLE order_payments (
        order_id TEXT,
        payment_sequential INTEGER,
        payment_type TEXT,
        payment_installments INTEGER,
        payment_value REAL
)

/*
3 rows from order_payments table:
order_id        payment_sequential      payment_type    payment_installments    payment_value
b81ef226f3fe1789b1e8b2acac839d17        1       credit_card     8       99.33
a9810da82917af2d9aefd1278f1dcfa0        1       credit_card     1       24.39
25e8ea4e93396b6fa0d3dd708e76c1bd        1       credit_card     1       65.71
*/


CREATE TABLE order_reviews (
        review_id TEXT,
        order_id TEXT,
        review_score INTEGER,
        review_comment_title TEXT,
        review_comment_message TEXT,
        review_creation_date TEXT,
        review_answer_timestamp TEXT
)

/*
3 rows from order_reviews table:
review_id       order_id        review_score    review_comment_title    review_comment_message  review_creation_date    review_answer_timestamp
7bc2406110b926393aa56f80a40eba40        73fc7af87114b39712e6da79b0a377eb        4       None    None    2018-01-18 00:00:00     2018-01-18 21:46:59
80e641a11e56f04c1ad469d5645fdfde        a548910a1c6147796b98fdf73dbeba33        5       None    None    2018-03-10 00:00:00     2018-03-11 03:05:13
228ce5500dc1d8e020d8d1322874b6f0        f9e4b658b201a9f2ecdecbb34bed034b        5       None    None    2018-02-17 00:00:00     2018-02-18 14:36:24
*/


CREATE TABLE orders (
        order_id TEXT,
        customer_id TEXT,
        order_status TEXT,
        order_purchase_timestamp TEXT,
        order_approved_at TEXT,
        order_delivered_carrier_date TEXT,
        order_delivered_customer_date TEXT,
        order_estimated_delivery_date TEXT
)

/*
3 rows from orders table:
order_id        customer_id     order_status    order_purchase_timestamp        order_approved_at       order_delivered_carrier_date    order_delivered_customer_date   order_estimated_delivery_date
e481f51cbdc54678b7cc49136f2d6af7        9ef432eb6251297304e76186b10a928d        delivered       2017-10-02 10:56:33     2017-10-02 11:07:15     2017-10-04 19:55:00     2017-10-10 21:25:13      2017-10-18 00:00:00
53cdb2fc8bc7dce0b6741e2150273451        b0830fb4747a6c6d20dea0b8c802d7ef        delivered       2018-07-24 20:41:37     2018-07-26 03:24:27     2018-07-26 14:31:00     2018-08-07 15:27:45      2018-08-13 00:00:00
47770eb9100c2d0c44946d9cf07ec65d        41ce2a54c0b03bf3443c3d931a367089        delivered       2018-08-08 08:38:49     2018-08-08 08:55:23     2018-08-08 13:50:00     2018-08-17 18:06:29      2018-09-04 00:00:00
*/


CREATE TABLE product_category_name_translation (
        product_category_name TEXT,
        product_category_name_english TEXT
)

/*
3 rows from product_category_name_translation table:
product_category_name   product_category_name_english
beleza_saude    health_beauty
informatica_acessorios  computers_accessories
automotivo      auto
*/


CREATE TABLE products (
        product_id TEXT,
        product_category_name TEXT,
        product_name_lenght REAL,
        product_description_lenght REAL,
        product_photos_qty REAL,
        product_weight_g REAL,
        product_length_cm REAL,
        product_height_cm REAL,
        product_width_cm REAL
)

/*
3 rows from products table:
product_id      product_category_name   product_name_lenght     product_description_lenght      product_photos_qty      product_weight_g        product_length_cm       product_height_cm        product_width_cm
1e9e8ef04dbcff4541ed26657ea517e5        perfumaria      40.0    287.0   1.0     225.0   16.0    10.0    14.0
3aa071139cb16b67ca9e5dea641aaa2f        artes   44.0    276.0   1.0     1000.0  30.0    18.0    20.0
96bd76ec8810374ed1b65e291975717f        esporte_lazer   46.0    250.0   1.0     154.0   18.0    9.0     15.0
*/


CREATE TABLE sellers (
        seller_id TEXT,
        seller_zip_code_prefix INTEGER,
        seller_city TEXT,
        seller_state TEXT
)

/*
3 rows from sellers table:
seller_id       seller_zip_code_prefix  seller_city     seller_state
3442f8959a84dea7ee197c632cb2df15        13023   campinas        SP
d1b65fc7debc3361ea86b5f14c68d2e2        13844   mogi guacu      SP
ce3ad9de960102d0677a81f5d0bb7b2d        20031   rio de janeiro  RJ
*/
"""