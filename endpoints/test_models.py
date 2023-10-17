def test_ryan(customer):
    customer.name = "new name"
    customer.save()
    assert customer.name == "new name"
