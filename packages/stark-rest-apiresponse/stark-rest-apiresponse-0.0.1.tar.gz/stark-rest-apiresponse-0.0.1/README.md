# starkrestresponse
Standard way to get the REST api response.

## Install
  ```
  pip install starkrestresponse
  ```

## Usage
1. Import starkrestresponse
  ```
  from starkrestresponse.starkrestresponse import ApiResponse
  ```
  
2. To get the response
  ```
  ApiResponse.response_created(self)
  ApiResponse.response_ok(self)
  ApiResponse.response_internal_server_error(self)
  ApiResponse.response_bad_request(self)
  ApiResponse.response_unauthenticate(self)
  ApiResponse.response_unauthorized(self)
  ApiResponse.response_not_found(self)
  ApiResponse.response_not_acceptable(self)
  ApiResponse.response_not_acceptable(self)
  ```

3. If you to change the default message:
  ```
  ApiResponse.response_created(self, message='User created successfully.')
  ```

3. Pass the data to response
  ```
  data = {
  	"id": 1,
  	"name": "test"
  }
  ApiResponse.response_created(self, data=data, paginator=pagination_obj)
  ``` 