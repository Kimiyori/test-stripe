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
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_NAME
POSTGRES_HOST
POSTGRES_PORT
SECRET_KE
STRIPE_SECRET_KEY
STRIPE_PUBLIC_KEY
```
Run the following command

```
docker-compose up --build
```
 
# How use 

1. Navigate to the following urls:

* /item/id
* order/id

2. Choose payment method (Session or PaymentIntent)

3. Enter credentials (card 4242 4242 4242 4242)