import requests
from behave import given
from compare import expect


@given('the following products')
def step_impl(context):
    """ Delete all Products and load new ones """
    # List all of the products and delete them one by one
    rest_endpoint = f"{context.BASE_URL}/api/products"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    for product in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{product['id']}")
        expect(context.resp.status_code).to_equal(204)

    # load the database with new products
    for row in context.table:
        payload = {
            "name": row['name'],
            "price": int(row['price']),
            "description": row['description'],
        }
        print(payload)
        context.resp = requests.post(rest_endpoint, json=payload)
        expect(context.resp.status_code).to_equal(201)
