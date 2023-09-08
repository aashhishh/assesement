# Advisor-Client Management System API

This Flask API provides endpoints for advisors and users to manage clients, products, and purchases. It also includes authentication using JWT tokens and OTP verification.

## Getting Started

To run this API locally, follow these steps:

1. Clone this repository.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Set up your database configurations in `.env` file.
4. Initiate db Migrations with-
     i. flask db init
     ii. flask db migrate
     iii. flask db upgrade
5. Run the Flask application using `python app.py`.

## Endpoints

### Advisor Registration

- **Endpoint:** `/advisor/signup`
- **Method:** POST
- **Description:** Allows advisors to register using their mobile number and OTP verification.
- **Request Body:**
  - `mobile`: The advisor's mobile number (10 digits).
  - `otp`: OTP for verification (fixed value for testing: '123456').
- **Response:** Returns a JWT token upon successful registration.

### Adding a Client

- **Endpoint:** `/advisor/add-client`
- **Method:** POST
- **Description:** Advisors can add clients with a name and mobile number.
- **Request Body:**
  - `name`: Name of the client.
  - `mobile`: Mobile number of the client (10 digits).
- **Response:** Returns a success message upon client addition.

### Viewing Advisor's Clients

- **Endpoint:** `/advisor/clients`
- **Method:** GET
- **Description:** Advisors can view the list of all their clients.
- **Response:** Returns a list of client details.

### User Signup

- **Endpoint:** `/user/signup`
- **Method:** POST
- **Description:** Allows users to register using their mobile number and OTP verification.
- **Request Body:**
  - `name`: Name of the user.
  - `mobile`: Mobile number of the user (10 digits).
  - `otp`: OTP for verification (fixed value for testing: '123456').
- **Response:** Returns a success message upon user registration.

### Adding a Product

- **Endpoint:** `/admin/add-product`
- **Method:** POST
- **Description:** Admins can add products with a name, description, and category.
- **Request Body:**
  - `product_name`: Name of the product.
  - `product_description`: Description of the product.
  - `category`: Category of the product.
- **Response:** Returns a success message upon product addition.

### Viewing Products

- **Endpoint:** `/advisor/products`
- **Method:** GET
- **Description:** Advisors can view the list of all available products.
- **Response:** Returns a list of product details.

### Purchasing a Product

- **Endpoint:** `/advisor/purchase-product`
- **Method:** POST
- **Description:** Advisors can purchase products for users and receive a unique product link.
- **Request Body:**
  - `user_id`: ID of the user for whom the product is purchased.
  - `product_id`: ID of the product being purchased.
- **Response:** Returns a unique product link.

## Authentication

- JWT (JSON Web Tokens) are used for authentication.
- Advisors and users are authenticated using JWT tokens.
- OTP (One-Time Password) verification is used during registration.

## Error Handling

- The API handles various errors such as invalid input, duplicate entries, and server errors gracefully.
- Appropriate error messages and status codes are returned in the responses.

## Running the API

To run the API locally, execute the following command:

```bash
python app.py

