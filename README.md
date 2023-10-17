# drf_endpoint_examples

Prrovides an example DRF app from which an OpenAPI schema may be generated in order to try out client code generation.
Examples are of models that might represent a commerce site.

## Installation

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

## Usage

```bash
python manage.py runserver
``` 

Then visit:

- http://localhost:8000/openapi/ to see the OpenAPI schema.
- http://localhost:8000/admin/ to see the admin site.
- http://localhost:8000/api/ to see the browsable API.
- http://localhost:8000/swagger-ui/ to see the Swagger UI.

To access the API from a python client that you might generate from the openapi schema, you will need to authenticate.
DRF's TokenAuthentication is enabled, so you will need to create a token for the superuser you created above. This is
done by visiting http://localhost:8000/admin/authtoken/tokenproxy/ and creating a token for the superuser.
Then you can use the generated client to access the API.

## License

[MIT](https://choosealicense.com/licenses/mit/)

