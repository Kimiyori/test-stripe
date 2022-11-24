# About

Test project with stripe api

# What's done

:white_check_mark: Docker deploy

:white_check_mark: Env variables

:white_check_mark: Database tables in django admin panel

:white_check_mark: Order model with multiple items

:white_check_mark: Tax and discount models

:white_check_mark: Currency field for Item model

:white_check_mark: Implemented both sessions and payment intent for stripe


# How deploy

Create an .env file with the following structure in the root folder

```
POSTGRES_USER=postges
POSTGRES_PASSWORD=postges
POSTGRES_NAME=postges
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=secret_key
STRIPE_SECRET_KEY=your_stripe_test_secret_key
STRIPE_PUBLIC_KEY=your_stripe_test_public_key
```
Run the following command:

```
docker-compose up --build
```
 
# How use 

1. Navigate to the following urls(docker build creates 10 items and 2 order instances for testing):

* /item/id
* /order/id

2. Choose payment method on the page(Session or PaymentIntent)

3. Enter credentials (card 4242 4242 4242 4242)

Also, the docker build creates an admin account with username and password 'test_admin' to use the admin panel.
