# Employee Parking System

All the best Bob!

## Endpoints

### Client

The client endpoint at `base-url/api/client` lets you register a client. 
It expects a JSON payload with the client name in the format `{"name":"Cresta Mall"}`. 
Upon a successful registration, it returns a response in the below format

```py
{
    "data": {
        "message": "Client registered successfully. Store your api key securely and don't share it.",
        "client_id": 1,
        "api_key": "<CLIENT-API-KEY>"
    }
}
```

### Employee

The employee endpoint at `base-url/api/employee` lets you:

- Load employees in a csv or excel file via a `POST` request. The file should be attached to a key named `file`.
- Fetch all employees that belong to a client via a `GET` request.
- Delete an employee that belongs to a client via a `DELETE` request. To delete an employee, attach their email as an identifier in the `DELETE` request e.g `{"email": "name@example.com"}`.

All requests sent to the Employee endpoint should have the API Key issued to the respective client added as an Authorization header in the format `Bearer <CLIENT-API-KEY>`.
