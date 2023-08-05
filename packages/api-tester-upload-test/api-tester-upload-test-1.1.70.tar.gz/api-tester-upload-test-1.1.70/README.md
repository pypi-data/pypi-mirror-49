# Getting started

Testing various
 api 
features

## How to Build


You must have Python ```2 >=2.7.9``` or Python ```3 >=3.4``` installed on your system to install and run this SDK. This SDK package depends on other Python packages like nose, jsonpickle etc. 
These dependencies are defined in the ```requirements.txt``` file that comes with the SDK.
To resolve these dependencies, you can use the PIP Dependency manager. Install it by following steps at [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/).

Python and PIP executables should be defined in your PATH. Open command prompt and type ```pip --version```.
This should display the version of the PIP Dependency Manager installed if your installation was successful and the paths are properly defined.

* Using command line, navigate to the directory containing the generated files (including ```requirements.txt```) for the SDK.
* Run the command ```pip install -r requirements.txt```. This should install all the required dependencies.

![Building SDK - Step 1](https://apidocs.io/illustration/python?step=installDependencies&workspaceFolder=Tester-Python)


## How to Use

The following section explains how to use the ApiTesterUploadTest SDK package in a new project.

### 1. Open Project in an IDE

Open up a Python IDE like PyCharm. The basic workflow presented here is also applicable if you prefer using a different editor or IDE.

![Open project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=pyCharm)

Click on ```Open``` in PyCharm to browse to your generated SDK directory and then click ```OK```.

![Open project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=openProject0&workspaceFolder=Tester-Python)     

The project files will be displayed in the side bar as follows:

![Open project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=openProject1&workspaceFolder=Tester-Python&projectName=api_tester_upload_test)     

### 2. Add a new Test Project

Create a new directory by right clicking on the solution name as shown below:

![Add a new project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=createDirectory&workspaceFolder=Tester-Python&projectName=api_tester_upload_test)

Name the directory as "test"

![Add a new project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=nameDirectory)
   
Add a python file to this project with the name "testsdk"

![Add a new project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=createFile&workspaceFolder=Tester-Python&projectName=api_tester_upload_test)

Name it "testsdk"

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=nameFile)

In your python file you will be required to import the generated python library using the following code lines

```Python
from api_tester_upload_test.hello_from_haider import HelloFromHaider
```

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=projectFiles&workspaceFolder=Tester-Python&libraryName=api_tester_upload_test.hello_from_haider&projectName=api_tester_upload_test&className=HelloFromHaider)

After this you can write code to instantiate an API client object, get a controller object and  make API calls. Sample code is given in the subsequent sections.

### 3. Run the Test Project

To run the file within your test project, right click on your Python file inside your Test project and click on ```Run```

![Run Test Project - Step 1](https://apidocs.io/illustration/python?step=runProject&workspaceFolder=Tester-Python&libraryName=api_tester_upload_test.hello_from_haider&projectName=api_tester_upload_test&className=HelloFromHaider)


## How to Test

You can test the generated SDK and the server with automatically generated test
cases. unittest is used as the testing framework and nose is used as the test
runner. You can run the tests as follows:

  1. From terminal/cmd navigate to the root directory of the SDK.
  2. Invoke ```pip install -r test-requirements.txt```
  3. Invoke ```nosetests```

## Initialization

### 
You need the following information for initializing the API client.

| Parameter | Description |
|-----------|-------------|
| square_version | 2019-05-08 |



API client can be initialized as following.

```python
# Configuration parameters
square_version = '2019-05-08' # 2019-05-08

client = HelloFromHaider(square_version)
```



# Class Reference

## <a name="list_of_controllers"></a>List of Controllers

* [FormParamsController](#form_params_controller)
* [QueryParamsController](#query_params_controller)
* [BodyParamsController](#body_params_controller)
* [ErrorCodesController](#error_codes_controller)
* [ResponseTypesController](#response_types_controller)
* [QueryParamController](#query_param_controller)
* [TemplateParamsController](#template_params_controller)
* [HeaderController](#header_controller)
* [EchoController](#echo_controller)

## <a name="form_params_controller"></a>![Class: ](https://apidocs.io/img/class.png ".FormParamsController") FormParamsController

### Get controller instance

An instance of the ``` FormParamsController ``` class can be accessed from the API Client.

```python
 form_params_controller = client.form_params
```

### <a name="date_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.date_as_optional") date_as_optional

> TODO: Add a method description

```python
def date_as_optional(self,
                         body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{ \"date\" : \"1994-02-13\" }"
body = json.loads(body_value)

result = form_params_controller.date_as_optional(body)

```


### <a name="dynamic_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.dynamic_as_optional") dynamic_as_optional

> TODO: Add a method description

```python
def dynamic_as_optional(self,
                            body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{   \"dynamic\" : {     \"dynamic\" : \"test\"   } }"
body = json.loads(body_value)

result = form_params_controller.dynamic_as_optional(body)

```


### <a name="string_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.string_as_optional") string_as_optional

> TODO: Add a method description

```python
def string_as_optional(self,
                           body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"string\" : \"test\"}"
body = json.loads(body_value)

result = form_params_controller.string_as_optional(body)

```


### <a name="precision_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.precision_as_optional") precision_as_optional

> TODO: Add a method description

```python
def precision_as_optional(self,
                              body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"precision\" : 1.23}"
body = json.loads(body_value)

result = form_params_controller.precision_as_optional(body)

```


### <a name="long_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.long_as_optional") long_as_optional

> TODO: Add a method description

```python
def long_as_optional(self,
                         body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"long\" : 123123}"
body = json.loads(body_value)

result = form_params_controller.long_as_optional(body)

```


### <a name="send_number_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_number_as_optional") send_number_as_optional

> TODO: Add a method description

```python
def send_number_as_optional(self,
                                body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"number\" : 1}"
body = json.loads(body_value)

result = form_params_controller.send_number_as_optional(body)

```


### <a name="send_datetime_optional_in_endpoint"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_datetime_optional_in_endpoint") send_datetime_optional_in_endpoint

> TODO: Add a method description

```python
def send_datetime_optional_in_endpoint(self,
                                           body=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Optional ```  | TODO: Add a parameter description |



#### Example Usage

```python
body = datetime.now()

result = form_params_controller.send_datetime_optional_in_endpoint(body)

```


### <a name="send_optional_unix_time_stamp_in_model_body"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_optional_unix_time_stamp_in_model_body") send_optional_unix_time_stamp_in_model_body

> TODO: Add a method description

```python
def send_optional_unix_time_stamp_in_model_body(self,
                                                    date_time)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| dateTime |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
date_time = UnixDateTime()

result = form_params_controller.send_optional_unix_time_stamp_in_model_body(date_time)

```


### <a name="send_optional_unix_time_stamp_in_nested_model_body"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_optional_unix_time_stamp_in_nested_model_body") send_optional_unix_time_stamp_in_nested_model_body

> TODO: Add a method description

```python
def send_optional_unix_time_stamp_in_nested_model_body(self,
                                                           date_time)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| dateTime |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
date_time_value = "{\"dateTime\" : {\"dateTime\":1484719381}}"
date_time = json.loads(date_time_value)

result = form_params_controller.send_optional_unix_time_stamp_in_nested_model_body(date_time)

```


### <a name="send_rfc_1123_date_time_in_nested_model"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_rfc_1123_date_time_in_nested_model") send_rfc_1123_date_time_in_nested_model

> TODO: Add a method description

```python
def send_rfc_1123_date_time_in_nested_model(self,
                                                body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body = SendRfc1123DateTime()

result = form_params_controller.send_rfc_1123_date_time_in_nested_model(body)

```


### <a name="send_rfc_1123_date_time_in_model"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_rfc_1123_date_time_in_model") send_rfc_1123_date_time_in_model

> TODO: Add a method description

```python
def send_rfc_1123_date_time_in_model(self,
                                         date_time)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| dateTime |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
date_time = ModelWithOptionalRfc1123DateTime()

result = form_params_controller.send_rfc_1123_date_time_in_model(date_time)

```


### <a name="send_optional_datetime_in_model"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_optional_datetime_in_model") send_optional_datetime_in_model

> TODO: Add a method description

```python
def send_optional_datetime_in_model(self,
                                        body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body = ModelWithOptionalRfc3339DateTime()

result = form_params_controller.send_optional_datetime_in_model(body)

```


### <a name="send_rfc_339_date_time_in_nested_models"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_rfc_339_date_time_in_nested_models") send_rfc_339_date_time_in_nested_models

> TODO: Add a method description

```python
def send_rfc_339_date_time_in_nested_models(self,
                                                body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body = SendRfc339DateTime()

result = form_params_controller.send_rfc_339_date_time_in_nested_models(body)

```


### <a name="uuid_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.uuid_as_optional") uuid_as_optional

> TODO: Add a method description

```python
def uuid_as_optional(self,
                         body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{   \"uuid\" : \"123e4567-e89b-12d3-a456-426655440000\" }"
body = json.loads(body_value)

result = form_params_controller.uuid_as_optional(body)

```


### <a name="send_optional_unix_date_time_in_body"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_optional_unix_date_time_in_body") send_optional_unix_date_time_in_body

> TODO: Add a method description

```python
def send_optional_unix_date_time_in_body(self,
                                             date_time=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| dateTime |  ``` Optional ```  | TODO: Add a parameter description |



#### Example Usage

```python
date_time = datetime.now()

result = form_params_controller.send_optional_unix_date_time_in_body(date_time)

```


### <a name="send_optional_rfc_1123_in_body"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_optional_rfc_1123_in_body") send_optional_rfc_1123_in_body

> TODO: Add a method description

```python
def send_optional_rfc_1123_in_body(self,
                                       body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body = datetime.now()

result = form_params_controller.send_optional_rfc_1123_in_body(body)

```


### <a name="boolean_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.boolean_as_optional") boolean_as_optional

> TODO: Add a method description

```python
def boolean_as_optional(self,
                            body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"boolean\" : true}"
body = json.loads(body_value)

result = form_params_controller.boolean_as_optional(body)

```


### <a name="send_string_in_form_with_new_line"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_string_in_form_with_new_line") send_string_in_form_with_new_line

> TODO: Add a method description

```python
def send_string_in_form_with_new_line(self,
                                          body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"name\":\"farhan\", \"field\":\"QA\"}"
body = json.loads(body_value)

result = form_params_controller.send_string_in_form_with_new_line(body)

```


### <a name="send_string_in_form_with_r"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_string_in_form_with_r") send_string_in_form_with_r

> TODO: Add a method description

```python
def send_string_in_form_with_r(self,
                                   body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"name\":\"farhan\",\"field\":\"QA\"}"
body = json.loads(body_value)

result = form_params_controller.send_string_in_form_with_r(body)

```


### <a name="send_string_in_form_with_r_n"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_string_in_form_with_r_n") send_string_in_form_with_r_n

> TODO: Add a method description

```python
def send_string_in_form_with_r_n(self,
                                     body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"name\":\"farhan\",\"field\":\"QA\"}"
body = json.loads(body_value)

result = form_params_controller.send_string_in_form_with_r_n(body)

```


### <a name="update_string_array_with_form"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.update_string_array_with_form") update_string_array_with_form

> TODO: Add a method description

```python
def update_string_array_with_form(self,
                                      strings)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| strings |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
strings_value = '["abc", "def"]'
strings = json.loads(strings_value)

result = form_params_controller.update_string_array_with_form(strings)

```


### <a name="send_integer_enum_array"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_integer_enum_array") send_integer_enum_array

> TODO: Add a method description

```python
def send_integer_enum_array(self,
                                suites)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| suites |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
suites = [SuiteCode.HEARTS,SuiteCode.CLUBS,SuiteCode.DIAMONDS,SuiteCode.SPADES,SuiteCode.CLUBS]

result = form_params_controller.send_integer_enum_array(suites)

```


### <a name="send_string_enum_array"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_string_enum_array") send_string_enum_array

> TODO: Add a method description

```python
def send_string_enum_array(self,
                               days)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| days |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
days = [Days.TUESDAY,Days.SATURDAY,Days.MONDAY,Days.SUNDAY]

result = form_params_controller.send_string_enum_array(days)

```


### <a name="send_delete_form_with_model_array"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_delete_form_with_model_array") send_delete_form_with_model_array

> TODO: Add a method description

```python
def send_delete_form_with_model_array(self,
                                          models)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| models |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
models_value = "[{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}, {\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}]"
models = json.loads(models_value)

result = form_params_controller.send_delete_form_with_model_array(models)

```


### <a name="update_model_array_with_form"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.update_model_array_with_form") update_model_array_with_form

> TODO: Add a method description

```python
def update_model_array_with_form(self,
                                     models)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| models |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
models_value = "[{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}, {\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}]"
models = json.loads(models_value)

result = form_params_controller.update_model_array_with_form(models)

```


### <a name="update_string_with_form"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.update_string_with_form") update_string_with_form

> TODO: Add a method description

```python
def update_string_with_form(self,
                                value)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| value |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
value = 'TestString'

result = form_params_controller.update_string_with_form(value)

```


### <a name="send_rfc_3339_date_time_array"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_rfc_3339_date_time_array") send_rfc_3339_date_time_array

> TODO: Add a method description

```python
def send_rfc_3339_date_time_array(self,
                                      datetimes)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetimes |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetimes_value = ["1994-02-13T14:01:54.9571247Z","1994-02-13T14:01:54.9571247Z"]
datetimes = json.loads(datetimes_value)

result = form_params_controller.send_rfc_3339_date_time_array(datetimes)

```


### <a name="send_mixed_array"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_mixed_array") send_mixed_array

> Send a variety for form params. Returns file count and body params

```python
def send_mixed_array(self,
                         options=dict())
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| file |  ``` Required ```  | TODO: Add a parameter description |
| integers |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |
| models |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |
| strings |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
collect = {}

file = open("pathtofile", 'rb')
collect['file'] = file

integers_value = "[1,2,3,4,5]"
integers = json.loads(integers_value)
collect['integers'] = integers

models_value = "[{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"},{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}]"
models = json.loads(models_value)
collect['models'] = models

strings_value = '["abc", "def"]'
strings = json.loads(strings_value)
collect['strings'] = strings


result = form_params_controller.send_mixed_array(collect)

```


### <a name="update_model_with_form"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.update_model_with_form") update_model_with_form

> TODO: Add a method description

```python
def update_model_with_form(self,
                               model)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| model |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
model_value = "{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}"
model = json.loads(model_value)

result = form_params_controller.update_model_with_form(model)

```


### <a name="send_delete_form_1"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_delete_form_1") send_delete_form_1

> TODO: Add a method description

```python
def send_delete_form_1(self,
                           model)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| model |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
model_value = "{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}"
model = json.loads(model_value)

result = form_params_controller.send_delete_form_1(model)

```


### <a name="send_integer_array"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_integer_array") send_integer_array

> TODO: Add a method description

```python
def send_integer_array(self,
                           integers)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| integers |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
integers_value = "[1,2,3,4,5]"
integers = json.loads(integers_value)

result = form_params_controller.send_integer_array(integers)

```


### <a name="send_string_array"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_string_array") send_string_array

> TODO: Add a method description

```python
def send_string_array(self,
                          strings)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| strings |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
strings_value = '["abc", "def"]'
strings = json.loads(strings_value)

result = form_params_controller.send_string_array(strings)

```


### <a name="allow_dynamic_form_fields"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.allow_dynamic_form_fields") allow_dynamic_form_fields

> TODO: Add a method description

```python
def allow_dynamic_form_fields(self,
                                  name,
                                  _optional_form_parameters=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| name |  ``` Required ```  | TODO: Add a parameter description |
| _optional_form_parameters | ``` Optional ``` | Additional optional form parameters are supported by this method |



#### Example Usage

```python
name = 'farhan'
# key-value map for optional form parameters
optional_form_parameters = { }


result = form_params_controller.allow_dynamic_form_fields(name, optional_form_parameters)

```


### <a name="send_model_array"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_model_array") send_model_array

> TODO: Add a method description

```python
def send_model_array(self,
                         models)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| models |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
models_value = "[{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"},{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}]"
models = json.loads(models_value)

result = form_params_controller.send_model_array(models)

```


### <a name="send_file"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_file") send_file

> TODO: Add a method description

```python
def send_file(self,
                  file)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| file |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
file = open("pathtofile", 'rb')

result = form_params_controller.send_file(file)

```


### <a name="send_multiple_files"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_multiple_files") send_multiple_files

> TODO: Add a method description

```python
def send_multiple_files(self,
                            file,
                            file_1)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| file |  ``` Required ```  | TODO: Add a parameter description |
| file1 |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
file = open("pathtofile", 'rb')
file_1 = open("pathtofile", 'rb')

result = form_params_controller.send_multiple_files(file, file_1)

```


### <a name="send_string"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_string") send_string

> TODO: Add a method description

```python
def send_string(self,
                    value)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| value |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
value = 'TestString'

result = form_params_controller.send_string(value)

```


### <a name="send_long"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_long") send_long

> TODO: Add a method description

```python
def send_long(self,
                  value)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| value |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
value = 5147483647

result = form_params_controller.send_long(value)

```


### <a name="send_model"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_model") send_model

> TODO: Add a method description

```python
def send_model(self,
                   model)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| model |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
model_value = "{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}"
model = json.loads(model_value)

result = form_params_controller.send_model(model)

```


### <a name="send_unix_date_time_array"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_unix_date_time_array") send_unix_date_time_array

> TODO: Add a method description

```python
def send_unix_date_time_array(self,
                                  datetimes)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetimes |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetimes_value = [1484719381,1484719381]
datetimes = json.loads(datetimes_value)

result = form_params_controller.send_unix_date_time_array(datetimes)

```


### <a name="send_rfc_1123_date_time_array"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_rfc_1123_date_time_array") send_rfc_1123_date_time_array

> TODO: Add a method description

```python
def send_rfc_1123_date_time_array(self,
                                      datetimes)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetimes |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetimes_value = ["Sun, 06 Nov 1994 08:49:37 GMT","Sun, 06 Nov 1994 08:49:37 GMT"]
datetimes = json.loads(datetimes_value)

result = form_params_controller.send_rfc_1123_date_time_array(datetimes)

```


### <a name="send_rfc_1123_date_time"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_rfc_1123_date_time") send_rfc_1123_date_time

> TODO: Add a method description

```python
def send_rfc_1123_date_time(self,
                                datetime)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetime |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetime = Sun, 06 Nov 1994 08:49:37 GMT

result = form_params_controller.send_rfc_1123_date_time(datetime)

```


### <a name="send_rfc_3339_date_time"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_rfc_3339_date_time") send_rfc_3339_date_time

> TODO: Add a method description

```python
def send_rfc_3339_date_time(self,
                                datetime)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetime |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetime = 1994-02-13T14:01:54.9571247Z

result = form_params_controller.send_rfc_3339_date_time(datetime)

```


### <a name="send_date_array"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_date_array") send_date_array

> TODO: Add a method description

```python
def send_date_array(self,
                        dates)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| dates |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
dates_value = ["1994-02-13","1994-02-13"]
dates = json.loads(dates_value)

result = form_params_controller.send_date_array(dates)

```


### <a name="send_date"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_date") send_date

> TODO: Add a method description

```python
def send_date(self,
                  date)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| date |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
date = 1994-02-13

result = form_params_controller.send_date(date)

```


### <a name="send_unix_date_time"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_unix_date_time") send_unix_date_time

> TODO: Add a method description

```python
def send_unix_date_time(self,
                            datetime)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetime |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetime = 1484719381

result = form_params_controller.send_unix_date_time(datetime)

```


### <a name="send_delete_multipart"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_delete_multipart") send_delete_multipart

> TODO: Add a method description

```python
def send_delete_multipart(self,
                              file)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| file |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
file = open("pathtofile", 'rb')

result = form_params_controller.send_delete_multipart(file)

```


### <a name="send_delete_form"></a>![Method: ](https://apidocs.io/img/method.png ".FormParamsController.send_delete_form") send_delete_form

> TODO: Add a method description

```python
def send_delete_form(self,
                         body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"name\":\"farhan\",\"field\":\"&&&\"}"
body = json.loads(body_value)

result = form_params_controller.send_delete_form(body)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="query_params_controller"></a>![Class: ](https://apidocs.io/img/class.png ".QueryParamsController") QueryParamsController

### Get controller instance

An instance of the ``` QueryParamsController ``` class can be accessed from the API Client.

```python
 query_params_controller = client.query_params
```

### <a name="boolean_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamsController.boolean_as_optional") boolean_as_optional

> TODO: Add a method description

```python
def boolean_as_optional(self,
                            boolean,
                            boolean_1=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| boolean |  ``` Required ```  | TODO: Add a parameter description |
| boolean1 |  ``` Optional ```  | TODO: Add a parameter description |



#### Example Usage

```python
boolean = True
boolean_1 = True

result = query_params_controller.boolean_as_optional(boolean, boolean_1)

```


### <a name="rfc_1123_datetime_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamsController.rfc_1123_datetime_as_optional") rfc_1123_datetime_as_optional

> TODO: Add a method description

```python
def rfc_1123_datetime_as_optional(self,
                                      date_time,
                                      date_time_1=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| dateTime |  ``` Required ```  | TODO: Add a parameter description |
| dateTime1 |  ``` Optional ```  | TODO: Add a parameter description |



#### Example Usage

```python
date_time = Sun, 06 Nov 1994 08:49:37 GMT
date_time_1 = Sun, 06 Nov 1994 08:49:37 GMT

result = query_params_controller.rfc_1123_datetime_as_optional(date_time, date_time_1)

```


### <a name="rfc_3339_datetime_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamsController.rfc_3339_datetime_as_optional") rfc_3339_datetime_as_optional

> TODO: Add a method description

```python
def rfc_3339_datetime_as_optional(self,
                                      date_time,
                                      date_time_1=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| dateTime |  ``` Required ```  | TODO: Add a parameter description |
| dateTime1 |  ``` Optional ```  | TODO: Add a parameter description |



#### Example Usage

```python
date_time = 1994-02-13T14:01:54.9571247Z
date_time_1 = 1994-02-13T14:01:54.9571247Z

result = query_params_controller.rfc_3339_datetime_as_optional(date_time, date_time_1)

```


### <a name="send_date_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamsController.send_date_as_optional") send_date_as_optional

> TODO: Add a method description

```python
def send_date_as_optional(self,
                              date,
                              date_1=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| date |  ``` Required ```  | TODO: Add a parameter description |
| date1 |  ``` Optional ```  | TODO: Add a parameter description |



#### Example Usage

```python
date = 1994-02-13
date_1 = 1994-02-13

result = query_params_controller.send_date_as_optional(date, date_1)

```


### <a name="send_string_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamsController.send_string_as_optional") send_string_as_optional

> TODO: Add a method description

```python
def send_string_as_optional(self,
                                string,
                                string_1=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| string |  ``` Required ```  | TODO: Add a parameter description |
| string1 |  ``` Optional ```  | TODO: Add a parameter description |



#### Example Usage

```python
string = 'test'
string_1 = 'test'

result = query_params_controller.send_string_as_optional(string, string_1)

```


### <a name="unixdatetime_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamsController.unixdatetime_as_optional") unixdatetime_as_optional

> TODO: Add a method description

```python
def unixdatetime_as_optional(self,
                                 date_time,
                                 date_time_1=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| dateTime |  ``` Required ```  | TODO: Add a parameter description |
| dateTime1 |  ``` Optional ```  | TODO: Add a parameter description |



#### Example Usage

```python
date_time = 1484719381
date_time_1 = 1484719381

result = query_params_controller.unixdatetime_as_optional(date_time, date_time_1)

```


### <a name="send_number_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamsController.send_number_as_optional") send_number_as_optional

> TODO: Add a method description

```python
def send_number_as_optional(self,
                                number,
                                number_1=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| number |  ``` Required ```  | TODO: Add a parameter description |
| number1 |  ``` Optional ```  | TODO: Add a parameter description |



#### Example Usage

```python
number = 1
number_1 = 1

result = query_params_controller.send_number_as_optional(number, number_1)

```


### <a name="send_long_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamsController.send_long_as_optional") send_long_as_optional

> TODO: Add a method description

```python
def send_long_as_optional(self,
                              long,
                              long_1=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| long |  ``` Required ```  | TODO: Add a parameter description |
| long1 |  ``` Optional ```  | TODO: Add a parameter description |



#### Example Usage

```python
long = 123123
long_1 = 123123

result = query_params_controller.send_long_as_optional(long, long_1)

```


### <a name="precision_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamsController.precision_as_optional") precision_as_optional

> TODO: Add a method description

```python
def precision_as_optional(self,
                              precision,
                              precision_1=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| precision |  ``` Required ```  | TODO: Add a parameter description |
| precision1 |  ``` Optional ```  | TODO: Add a parameter description |



#### Example Usage

```python
precision = 1.23
precision_1 = 1.23

result = query_params_controller.precision_as_optional(precision, precision_1)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="body_params_controller"></a>![Class: ](https://apidocs.io/img/class.png ".BodyParamsController") BodyParamsController

### Get controller instance

An instance of the ``` BodyParamsController ``` class can be accessed from the API Client.

```python
 body_params_controller = client.body_params
```

### <a name="send_number_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_number_as_optional") send_number_as_optional

> TODO: Add a method description

```python
def send_number_as_optional(self,
                                body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"number\" : 1}"
body = json.loads(body_value)

result = body_params_controller.send_number_as_optional(body)

```


### <a name="send_optional_datetime_in_model"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_optional_datetime_in_model") send_optional_datetime_in_model

> TODO: Add a method description

```python
def send_optional_datetime_in_model(self,
                                        body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body = ModelWithOptionalRfc3339DateTime()

result = body_params_controller.send_optional_datetime_in_model(body)

```


### <a name="send_rfc_339_date_time_in_nested_models"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_rfc_339_date_time_in_nested_models") send_rfc_339_date_time_in_nested_models

> TODO: Add a method description

```python
def send_rfc_339_date_time_in_nested_models(self,
                                                body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body = SendRfc339DateTime()

result = body_params_controller.send_rfc_339_date_time_in_nested_models(body)

```


### <a name="uuid_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.uuid_as_optional") uuid_as_optional

> TODO: Add a method description

```python
def uuid_as_optional(self,
                         body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{   \"uuid\" : \"123e4567-e89b-12d3-a456-426655440000\" }"
body = json.loads(body_value)

result = body_params_controller.uuid_as_optional(body)

```


### <a name="date_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.date_as_optional") date_as_optional

> TODO: Add a method description

```python
def date_as_optional(self,
                         body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{ \"date\" : \"1994-02-13\" }"
body = json.loads(body_value)

result = body_params_controller.date_as_optional(body)

```


### <a name="dynamic_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.dynamic_as_optional") dynamic_as_optional

> TODO: Add a method description

```python
def dynamic_as_optional(self,
                            body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{   \"dynamic\" : {     \"dynamic\" : \"test\"   } }"
body = json.loads(body_value)

result = body_params_controller.dynamic_as_optional(body)

```


### <a name="string_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.string_as_optional") string_as_optional

> TODO: Add a method description

```python
def string_as_optional(self,
                           body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"string\" : \"test\"}"
body = json.loads(body_value)

result = body_params_controller.string_as_optional(body)

```


### <a name="precision_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.precision_as_optional") precision_as_optional

> TODO: Add a method description

```python
def precision_as_optional(self,
                              body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"precision\" : 1.23}"
body = json.loads(body_value)

result = body_params_controller.precision_as_optional(body)

```


### <a name="long_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.long_as_optional") long_as_optional

> TODO: Add a method description

```python
def long_as_optional(self,
                         body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"long\" : 123123}"
body = json.loads(body_value)

result = body_params_controller.long_as_optional(body)

```


### <a name="send_optional_unix_date_time_in_body"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_optional_unix_date_time_in_body") send_optional_unix_date_time_in_body

> TODO: Add a method description

```python
def send_optional_unix_date_time_in_body(self,
                                             date_time=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| dateTime |  ``` Optional ```  | TODO: Add a parameter description |



#### Example Usage

```python
date_time = datetime.now()

result = body_params_controller.send_optional_unix_date_time_in_body(date_time)

```


### <a name="send_optional_rfc_1123_in_body"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_optional_rfc_1123_in_body") send_optional_rfc_1123_in_body

> TODO: Add a method description

```python
def send_optional_rfc_1123_in_body(self,
                                       body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body = datetime.now()

result = body_params_controller.send_optional_rfc_1123_in_body(body)

```


### <a name="send_datetime_optional_in_endpoint"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_datetime_optional_in_endpoint") send_datetime_optional_in_endpoint

> TODO: Add a method description

```python
def send_datetime_optional_in_endpoint(self,
                                           body=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Optional ```  | TODO: Add a parameter description |



#### Example Usage

```python
body = datetime.now()

result = body_params_controller.send_datetime_optional_in_endpoint(body)

```


### <a name="send_optional_unix_time_stamp_in_model_body"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_optional_unix_time_stamp_in_model_body") send_optional_unix_time_stamp_in_model_body

> TODO: Add a method description

```python
def send_optional_unix_time_stamp_in_model_body(self,
                                                    date_time)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| dateTime |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
date_time = UnixDateTime()

result = body_params_controller.send_optional_unix_time_stamp_in_model_body(date_time)

```


### <a name="send_optional_unix_time_stamp_in_nested_model_body"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_optional_unix_time_stamp_in_nested_model_body") send_optional_unix_time_stamp_in_nested_model_body

> TODO: Add a method description

```python
def send_optional_unix_time_stamp_in_nested_model_body(self,
                                                           date_time)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| dateTime |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
date_time_value = "{\"dateTime\" : {\"dateTime\":1484719381}}"
date_time = json.loads(date_time_value)

result = body_params_controller.send_optional_unix_time_stamp_in_nested_model_body(date_time)

```


### <a name="send_rfc_1123_date_time_in_nested_model"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_rfc_1123_date_time_in_nested_model") send_rfc_1123_date_time_in_nested_model

> TODO: Add a method description

```python
def send_rfc_1123_date_time_in_nested_model(self,
                                                body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body = SendRfc1123DateTime()

result = body_params_controller.send_rfc_1123_date_time_in_nested_model(body)

```


### <a name="send_rfc_1123_date_time_in_model"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_rfc_1123_date_time_in_model") send_rfc_1123_date_time_in_model

> TODO: Add a method description

```python
def send_rfc_1123_date_time_in_model(self,
                                         date_time)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| dateTime |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
date_time = ModelWithOptionalRfc1123DateTime()

result = body_params_controller.send_rfc_1123_date_time_in_model(date_time)

```


### <a name="boolean_as_optional"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.boolean_as_optional") boolean_as_optional

> TODO: Add a method description

```python
def boolean_as_optional(self,
                            body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"boolean\" : true}"
body = json.loads(body_value)

result = body_params_controller.boolean_as_optional(body)

```


### <a name="send_string_with_new_line"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_string_with_new_line") send_string_with_new_line

> TODO: Add a method description

```python
def send_string_with_new_line(self,
                                  body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"name\":\"farhan\", \"field\":\"QA\"}"
body = json.loads(body_value)

result = body_params_controller.send_string_with_new_line(body)

```


### <a name="send_string_with_r"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_string_with_r") send_string_with_r

> TODO: Add a method description

```python
def send_string_with_r(self,
                           body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"name\":\"farhan\",\"field\":\"QA\"}"
body = json.loads(body_value)

result = body_params_controller.send_string_with_r(body)

```


### <a name="send_string_in_body_with_r_n"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_string_in_body_with_r_n") send_string_in_body_with_r_n

> TODO: Add a method description

```python
def send_string_in_body_with_r_n(self,
                                     body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"name\":\"farhan\",\"field\":\"QA\"}"
body = json.loads(body_value)

result = body_params_controller.send_string_in_body_with_r_n(body)

```


### <a name="send_delete_body_with_model"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_delete_body_with_model") send_delete_body_with_model

> TODO: Add a method description

```python
def send_delete_body_with_model(self,
                                    model)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| model |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
model_value = "{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}"
model = json.loads(model_value)

result = body_params_controller.send_delete_body_with_model(model)

```


### <a name="send_delete_body_with_model_array"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_delete_body_with_model_array") send_delete_body_with_model_array

> TODO: Add a method description

```python
def send_delete_body_with_model_array(self,
                                          models)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| models |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
models_value = "[{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}, {\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}]"
models = json.loads(models_value)

result = body_params_controller.send_delete_body_with_model_array(models)

```


### <a name="update_model_array"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.update_model_array") update_model_array

> TODO: Add a method description

```python
def update_model_array(self,
                           models)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| models |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
models_value = "[{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}, {\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}]"
models = json.loads(models_value)

result = body_params_controller.update_model_array(models)

```


### <a name="update_string_1"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.update_string_1") update_string_1

> TODO: Add a method description

```python
def update_string_1(self,
                        value)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| value |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
value = 'TestString'

result = body_params_controller.update_string_1(value)

```


### <a name="update_string_array"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.update_string_array") update_string_array

> TODO: Add a method description

```python
def update_string_array(self,
                            strings)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| strings |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
strings_value = '["abc", "def"]'
strings = json.loads(strings_value)

result = body_params_controller.update_string_array(strings)

```


### <a name="send_string_enum_array"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_string_enum_array") send_string_enum_array

> TODO: Add a method description

```python
def send_string_enum_array(self,
                               days)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| days |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
days = [Days.TUESDAY,Days.SATURDAY,Days.MONDAY,Days.SUNDAY]

result = body_params_controller.send_string_enum_array(days)

```


### <a name="send_integer_enum_array"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_integer_enum_array") send_integer_enum_array

> TODO: Add a method description

```python
def send_integer_enum_array(self,
                                suites)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| suites |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
suites = [SuiteCode.HEARTS,SuiteCode.CLUBS,SuiteCode.DIAMONDS,SuiteCode.SPADES,SuiteCode.CLUBS]

result = body_params_controller.send_integer_enum_array(suites)

```


### <a name="update_model"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.update_model") update_model

> TODO: Add a method description

```python
def update_model(self,
                     model)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| model |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
model_value = "{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}"
model = json.loads(model_value)

result = body_params_controller.update_model(model)

```


### <a name="send_string"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_string") send_string

> TODO: Add a method description

```python
def send_string(self,
                    value)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| value |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
value = 'TestString'

result = body_params_controller.send_string(value)

```


### <a name="update_string"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.update_string") update_string

> TODO: Add a method description

```python
def update_string(self,
                      value)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| value |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
value = 'TestString'

result = body_params_controller.update_string(value)

```


### <a name="send_integer_array"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_integer_array") send_integer_array

> TODO: Add a method description

```python
def send_integer_array(self,
                           integers)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| integers |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
integers_value = "[1,2,3,4,5]"
integers = json.loads(integers_value)

result = body_params_controller.send_integer_array(integers)

```


### <a name="wrap_body_in_object"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.wrap_body_in_object") wrap_body_in_object

> TODO: Add a method description

```python
def wrap_body_in_object(self,
                            field,
                            name)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| field |  ``` Required ```  | TODO: Add a parameter description |
| name |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
field = 'QA'
name = 'farhan'

result = body_params_controller.wrap_body_in_object(field, name)

```


### <a name="validate_required_parameter"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.validate_required_parameter") validate_required_parameter

> TODO: Add a method description

```python
def validate_required_parameter(self,
                                    model,
                                    option=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| model |  ``` Required ```  | TODO: Add a parameter description |
| option |  ``` Optional ```  | TODO: Add a parameter description |



#### Example Usage

```python
model_value = "{\"name\":\"farhan\", \"field\": \"QA\"}"
model = json.loads(model_value)
option = '...'

result = body_params_controller.validate_required_parameter(model, option)

```


### <a name="additional_model_parameters_1"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.additional_model_parameters_1") additional_model_parameters_1

> TODO: Add a method description

```python
def additional_model_parameters_1(self,
                                      model)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| model |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
model_value = "{\"name\":\"farhan\", \"field\":\"QA\", \"address\": \"Ghori Town\", \"Job\": {\"company\": \"APIMATIC\", \"location\":\"NUST\"}}"
model = json.loads(model_value)

result = body_params_controller.additional_model_parameters_1(model)

```


### <a name="send_model"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_model") send_model

> TODO: Add a method description

```python
def send_model(self,
                   model)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| model |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
model_value = "{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}"
model = json.loads(model_value)

result = body_params_controller.send_model(model)

```


### <a name="send_model_array"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_model_array") send_model_array

> TODO: Add a method description

```python
def send_model_array(self,
                         models)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| models |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
models_value = "[{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"},{\"name\":\"Shahid Khaliq\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"boss\":{\"personType\":\"Boss\",\"name\":\"Zeeshan Ejaz\",\"age\":5147483645,\"address\":\"H # 531, S # 20\",\"uid\":\"123321\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\",\"salary\":20000,\"department\":\"Software Development\",\"joiningDay\":\"Saturday\",\"workingDays\":[\"Monday\",\"Tuesday\",\"Friday\"],\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\",\"promotedAt\":1484719381},\"dependents\":[{\"name\":\"Future Wife\",\"age\":5147483649,\"address\":\"H # 531, S # 20\",\"uid\":\"123412\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"},{\"name\":\"Future Kid\",\"age\":5147483648,\"address\":\"H # 531, S # 20\",\"uid\":\"312341\",\"birthday\":\"1994-02-13\",\"birthtime\":\"1994-02-13T14:01:54.9571247Z\"}],\"hiredAt\":\"Sun, 06 Nov 1994 08:49:37 GMT\"}]"
models = json.loads(models_value)

result = body_params_controller.send_model_array(models)

```


### <a name="send_dynamic"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_dynamic") send_dynamic

> TODO: Add a method description

```python
def send_dynamic(self,
                     dynamic)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| dynamic |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
dynamic_value = "{\"uid\": \"1123213\", \"name\": \"Shahid\"}"
dynamic = json.loads(dynamic_value)

result = body_params_controller.send_dynamic(dynamic)

```


### <a name="send_rfc_3339_date_time_array"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_rfc_3339_date_time_array") send_rfc_3339_date_time_array

> TODO: Add a method description

```python
def send_rfc_3339_date_time_array(self,
                                      datetimes)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetimes |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetimes_value = ["1994-02-13T14:01:54.9571247Z","1994-02-13T14:01:54.9571247Z"]
datetimes = json.loads(datetimes_value)

result = body_params_controller.send_rfc_3339_date_time_array(datetimes)

```


### <a name="send_string_array"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_string_array") send_string_array

> sends a string body param

```python
def send_string_array(self,
                          sarray)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| sarray |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
sarray_value = '["abc", "def"]'
sarray = json.loads(sarray_value)

result = body_params_controller.send_string_array(sarray)

```


### <a name="additional_model_parameters"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.additional_model_parameters") additional_model_parameters

> TODO: Add a method description

```python
def additional_model_parameters(self,
                                    model)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| model |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
model_value = "{\"name\":\"farhan\", \"field\":\"QA\", \"address\": \"Ghori Town\", \"Job\": {\"company\": \"APIMATIC\", \"location\":\"NUST\"}}"
model = json.loads(model_value)

result = body_params_controller.additional_model_parameters(model)

```


### <a name="send_unix_date_time_array"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_unix_date_time_array") send_unix_date_time_array

> TODO: Add a method description

```python
def send_unix_date_time_array(self,
                                  datetimes)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetimes |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetimes_value = [1484719381,1484719381]
datetimes = json.loads(datetimes_value)

result = body_params_controller.send_unix_date_time_array(datetimes)

```


### <a name="send_rfc_1123_date_time_array"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_rfc_1123_date_time_array") send_rfc_1123_date_time_array

> TODO: Add a method description

```python
def send_rfc_1123_date_time_array(self,
                                      datetimes)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetimes |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetimes_value = ["Sun, 06 Nov 1994 08:49:37 GMT","Sun, 06 Nov 1994 08:49:37 GMT"]
datetimes = json.loads(datetimes_value)

result = body_params_controller.send_rfc_1123_date_time_array(datetimes)

```


### <a name="send_delete_plain_text"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_delete_plain_text") send_delete_plain_text

> TODO: Add a method description

```python
def send_delete_plain_text(self,
                               text_string)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| textString |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
text_string = 'farhan
nouman'

result = body_params_controller.send_delete_plain_text(text_string)

```


### <a name="send_date_array"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_date_array") send_date_array

> TODO: Add a method description

```python
def send_date_array(self,
                        dates)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| dates |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
dates_value = ["1994-02-13", "1994-02-13"]
dates = json.loads(dates_value)

result = body_params_controller.send_date_array(dates)

```


### <a name="send_rfc_3339_date_time"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_rfc_3339_date_time") send_rfc_3339_date_time

> TODO: Add a method description

```python
def send_rfc_3339_date_time(self,
                                datetime)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetime |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetime = 1994-02-13T14:01:54.9571247Z

result = body_params_controller.send_rfc_3339_date_time(datetime)

```


### <a name="send_rfc_1123_date_time"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_rfc_1123_date_time") send_rfc_1123_date_time

> TODO: Add a method description

```python
def send_rfc_1123_date_time(self,
                                datetime)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetime |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetime = Sun, 06 Nov 1994 08:49:37 GMT

result = body_params_controller.send_rfc_1123_date_time(datetime)

```


### <a name="send_unix_date_time"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_unix_date_time") send_unix_date_time

> TODO: Add a method description

```python
def send_unix_date_time(self,
                            datetime)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetime |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetime = 1484719381

result = body_params_controller.send_unix_date_time(datetime)

```


### <a name="send_date"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_date") send_date

> TODO: Add a method description

```python
def send_date(self,
                  date)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| date |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
date = 1994-02-13

result = body_params_controller.send_date(date)

```


### <a name="send_delete_body"></a>![Method: ](https://apidocs.io/img/method.png ".BodyParamsController.send_delete_body") send_delete_body

> TODO: Add a method description

```python
def send_delete_body(self,
                         body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
body_value = "{\"name\": \"farhan\", \"field\": \"QA\"}"
body = json.loads(body_value)

result = body_params_controller.send_delete_body(body)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="error_codes_controller"></a>![Class: ](https://apidocs.io/img/class.png ".ErrorCodesController") ErrorCodesController

### Get controller instance

An instance of the ``` ErrorCodesController ``` class can be accessed from the API Client.

```python
 error_codes_controller = client.error_codes
```

### <a name="date_in_exception"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.date_in_exception") date_in_exception

> TODO: Add a method description

```python
def date_in_exception(self)
```

#### Example Usage

```python

result = error_codes_controller.date_in_exception()

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 444 | date in exception |




### <a name="uuid_in_exception"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.uuid_in_exception") uuid_in_exception

> TODO: Add a method description

```python
def uuid_in_exception(self)
```

#### Example Usage

```python

result = error_codes_controller.uuid_in_exception()

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 444 | uuid in exception |




### <a name="dynamic_in_exception"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.dynamic_in_exception") dynamic_in_exception

> TODO: Add a method description

```python
def dynamic_in_exception(self)
```

#### Example Usage

```python

result = error_codes_controller.dynamic_in_exception()

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 444 | dynamic in Exception |




### <a name="precision_in_exception"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.precision_in_exception") precision_in_exception

> TODO: Add a method description

```python
def precision_in_exception(self)
```

#### Example Usage

```python

result = error_codes_controller.precision_in_exception()

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 444 | precision in Exception |




### <a name="boolean_in_exception"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.boolean_in_exception") boolean_in_exception

> TODO: Add a method description

```python
def boolean_in_exception(self)
```

#### Example Usage

```python

result = error_codes_controller.boolean_in_exception()

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 444 | Boolean in Exception |




### <a name="long_in_exception"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.long_in_exception") long_in_exception

> TODO: Add a method description

```python
def long_in_exception(self)
```

#### Example Usage

```python

result = error_codes_controller.long_in_exception()

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 444 | long in exception |




### <a name="number_in_exception"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.number_in_exception") number_in_exception

> TODO: Add a method description

```python
def number_in_exception(self)
```

#### Example Usage

```python

result = error_codes_controller.number_in_exception()

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 444 | number in exception |




### <a name="get_exception_with_string"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.get_exception_with_string") get_exception_with_string

> TODO: Add a method description

```python
def get_exception_with_string(self)
```

#### Example Usage

```python

result = error_codes_controller.get_exception_with_string()

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 444 | exception with string |




### <a name="receive_endpoint_level_exception"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.receive_endpoint_level_exception") receive_endpoint_level_exception

> TODO: Add a method description

```python
def receive_endpoint_level_exception(self)
```

#### Example Usage

```python

result = error_codes_controller.receive_endpoint_level_exception()

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 451 | caught endpoint exception |




### <a name="receive_global_level_exception"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.receive_global_level_exception") receive_global_level_exception

> TODO: Add a method description

```python
def receive_global_level_exception(self)
```

#### Example Usage

```python

result = error_codes_controller.receive_global_level_exception()

```


### <a name="receive_exception_with_rfc_3339_datetime"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.receive_exception_with_rfc_3339_datetime") receive_exception_with_rfc_3339_datetime

> TODO: Add a method description

```python
def receive_exception_with_rfc_3339_datetime(self)
```

#### Example Usage

```python

result = error_codes_controller.receive_exception_with_rfc_3339_datetime()

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 444 | DateTime Exception |




### <a name="receive_exception_with_unixtimestamp_exception"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.receive_exception_with_unixtimestamp_exception") receive_exception_with_unixtimestamp_exception

> TODO: Add a method description

```python
def receive_exception_with_unixtimestamp_exception(self)
```

#### Example Usage

```python

result = error_codes_controller.receive_exception_with_unixtimestamp_exception()

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 444 | unixtimestamp exception |




### <a name="receive_exception_with_rfc_1123_datetime"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.receive_exception_with_rfc_1123_datetime") receive_exception_with_rfc_1123_datetime

> TODO: Add a method description

```python
def receive_exception_with_rfc_1123_datetime(self)
```

#### Example Usage

```python

result = error_codes_controller.receive_exception_with_rfc_1123_datetime()

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 444 | Rfc1123 Exception |




### <a name="get_401"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.get_401") get_401

> TODO: Add a method description

```python
def get_401(self)
```

#### Example Usage

```python

result = error_codes_controller.get_401()

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 401 | 401 Local |
| 421 | Default |
| 431 | Default |
| 432 | Default |
| 441 | Default |
| 0 | Invalid response. |




### <a name="get_501"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.get_501") get_501

> TODO: Add a method description

```python
def get_501(self)
```

#### Example Usage

```python

result = error_codes_controller.get_501()

```

#### Errors

| Error Code | Error Description |
|------------|-------------------|
| 501 | error 501 |




### <a name="get_400"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.get_400") get_400

> TODO: Add a method description

```python
def get_400(self)
```

#### Example Usage

```python

result = error_codes_controller.get_400()

```


### <a name="get_500"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.get_500") get_500

> TODO: Add a method description

```python
def get_500(self)
```

#### Example Usage

```python

result = error_codes_controller.get_500()

```


### <a name="catch_412_global_error"></a>![Method: ](https://apidocs.io/img/method.png ".ErrorCodesController.catch_412_global_error") catch_412_global_error

> TODO: Add a method description

```python
def catch_412_global_error(self)
```

#### Example Usage

```python

result = error_codes_controller.catch_412_global_error()

```


[Back to List of Controllers](#list_of_controllers)

## <a name="response_types_controller"></a>![Class: ](https://apidocs.io/img/class.png ".ResponseTypesController") ResponseTypesController

### Get controller instance

An instance of the ``` ResponseTypesController ``` class can be accessed from the API Client.

```python
 response_types_controller = client.response_types
```

### <a name="get_content_type_headers"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_content_type_headers") get_content_type_headers

> TODO: Add a method description

```python
def get_content_type_headers(self)
```

#### Example Usage

```python

response_types_controller.get_content_type_headers()

```


### <a name="get_integer_array"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_integer_array") get_integer_array

> Get an array of integers.

```python
def get_integer_array(self)
```

#### Example Usage

```python

result = response_types_controller.get_integer_array()

```


### <a name="get_dynamic"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_dynamic") get_dynamic

> TODO: Add a method description

```python
def get_dynamic(self)
```

#### Example Usage

```python

result = response_types_controller.get_dynamic()

```


### <a name="get_dynamic_array"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_dynamic_array") get_dynamic_array

> TODO: Add a method description

```python
def get_dynamic_array(self)
```

#### Example Usage

```python

result = response_types_controller.get_dynamic_array()

```


### <a name="get_3339_datetime"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_3339_datetime") get_3339_datetime

> TODO: Add a method description

```python
def get_3339_datetime(self)
```

#### Example Usage

```python

result = response_types_controller.get_3339_datetime()

```


### <a name="get_3339_datetime_array"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_3339_datetime_array") get_3339_datetime_array

> TODO: Add a method description

```python
def get_3339_datetime_array(self)
```

#### Example Usage

```python

result = response_types_controller.get_3339_datetime_array()

```


### <a name="get_boolean"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_boolean") get_boolean

> TODO: Add a method description

```python
def get_boolean(self)
```

#### Example Usage

```python

result = response_types_controller.get_boolean()

```


### <a name="get_boolean_array"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_boolean_array") get_boolean_array

> TODO: Add a method description

```python
def get_boolean_array(self)
```

#### Example Usage

```python

result = response_types_controller.get_boolean_array()

```


### <a name="get_headers"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_headers") get_headers

> TODO: Add a method description

```python
def get_headers(self)
```

#### Example Usage

```python

response_types_controller.get_headers()

```


### <a name="get_1123_date_time"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_1123_date_time") get_1123_date_time

> TODO: Add a method description

```python
def get_1123_date_time(self)
```

#### Example Usage

```python

result = response_types_controller.get_1123_date_time()

```


### <a name="get_unix_date_time"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_unix_date_time") get_unix_date_time

> TODO: Add a method description

```python
def get_unix_date_time(self)
```

#### Example Usage

```python

result = response_types_controller.get_unix_date_time()

```


### <a name="get_1123_date_time_array"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_1123_date_time_array") get_1123_date_time_array

> TODO: Add a method description

```python
def get_1123_date_time_array(self)
```

#### Example Usage

```python

result = response_types_controller.get_1123_date_time_array()

```


### <a name="get_unix_date_time_array"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_unix_date_time_array") get_unix_date_time_array

> TODO: Add a method description

```python
def get_unix_date_time_array(self)
```

#### Example Usage

```python

result = response_types_controller.get_unix_date_time_array()

```


### <a name="get_int_enum_array"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_int_enum_array") get_int_enum_array

> TODO: Add a method description

```python
def get_int_enum_array(self)
```

#### Example Usage

```python

result = response_types_controller.get_int_enum_array()

```


### <a name="get_binary"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_binary") get_binary

> gets a binary object

```python
def get_binary(self)
```

#### Example Usage

```python

result = response_types_controller.get_binary()

```


### <a name="get_integer"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_integer") get_integer

> Gets a integer response

```python
def get_integer(self)
```

#### Example Usage

```python

result = response_types_controller.get_integer()

```


### <a name="get_string_enum"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_string_enum") get_string_enum

> TODO: Add a method description

```python
def get_string_enum(self)
```

#### Example Usage

```python

result = response_types_controller.get_string_enum()

```


### <a name="get_model_array"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_model_array") get_model_array

> TODO: Add a method description

```python
def get_model_array(self)
```

#### Example Usage

```python

result = response_types_controller.get_model_array()

```


### <a name="get_long"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_long") get_long

> TODO: Add a method description

```python
def get_long(self)
```

#### Example Usage

```python

result = response_types_controller.get_long()

```


### <a name="get_model"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_model") get_model

> TODO: Add a method description

```python
def get_model(self)
```

#### Example Usage

```python

result = response_types_controller.get_model()

```


### <a name="get_string_enum_array"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_string_enum_array") get_string_enum_array

> TODO: Add a method description

```python
def get_string_enum_array(self)
```

#### Example Usage

```python

result = response_types_controller.get_string_enum_array()

```


### <a name="get_int_enum"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_int_enum") get_int_enum

> TODO: Add a method description

```python
def get_int_enum(self)
```

#### Example Usage

```python

result = response_types_controller.get_int_enum()

```


### <a name="get_precision"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_precision") get_precision

> TODO: Add a method description

```python
def get_precision(self)
```

#### Example Usage

```python

result = response_types_controller.get_precision()

```


### <a name="return_complex_1_object"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.return_complex_1_object") return_complex_1_object

> TODO: Add a method description

```python
def return_complex_1_object(self)
```

#### Example Usage

```python

result = response_types_controller.return_complex_1_object()

```


### <a name="return_complex_3_object"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.return_complex_3_object") return_complex_3_object

> TODO: Add a method description

```python
def return_complex_3_object(self)
```

#### Example Usage

```python

result = response_types_controller.return_complex_3_object()

```


### <a name="return_response_with_enums"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.return_response_with_enums") return_response_with_enums

> TODO: Add a method description

```python
def return_response_with_enums(self)
```

#### Example Usage

```python

result = response_types_controller.return_response_with_enums()

```


### <a name="return_complex_2_object"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.return_complex_2_object") return_complex_2_object

> TODO: Add a method description

```python
def return_complex_2_object(self)
```

#### Example Usage

```python

result = response_types_controller.return_complex_2_object()

```


### <a name="return_tester_model"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.return_tester_model") return_tester_model

> TODO: Add a method description

```python
def return_tester_model(self)
```

#### Example Usage

```python

result = response_types_controller.return_tester_model()

```


### <a name="return_developer_model"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.return_developer_model") return_developer_model

> TODO: Add a method description

```python
def return_developer_model(self)
```

#### Example Usage

```python

result = response_types_controller.return_developer_model()

```


### <a name="return_employee_model"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.return_employee_model") return_employee_model

> TODO: Add a method description

```python
def return_employee_model(self)
```

#### Example Usage

```python

result = response_types_controller.return_employee_model()

```


### <a name="return_boss_model"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.return_boss_model") return_boss_model

> TODO: Add a method description

```python
def return_boss_model(self)
```

#### Example Usage

```python

result = response_types_controller.return_boss_model()

```


### <a name="return_company_model"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.return_company_model") return_company_model

> TODO: Add a method description

```python
def return_company_model(self)
```

#### Example Usage

```python

result = response_types_controller.return_company_model()

```


### <a name="get_date"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_date") get_date

> TODO: Add a method description

```python
def get_date(self)
```

#### Example Usage

```python

result = response_types_controller.get_date()

```


### <a name="get_date_array"></a>![Method: ](https://apidocs.io/img/method.png ".ResponseTypesController.get_date_array") get_date_array

> TODO: Add a method description

```python
def get_date_array(self)
```

#### Example Usage

```python

result = response_types_controller.get_date_array()

```


[Back to List of Controllers](#list_of_controllers)

## <a name="query_param_controller"></a>![Class: ](https://apidocs.io/img/class.png ".QueryParamController") QueryParamController

### Get controller instance

An instance of the ``` QueryParamController ``` class can be accessed from the API Client.

```python
 query_param_controller = client.query_param
```

### <a name="multiple_params"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.multiple_params") multiple_params

> TODO: Add a method description

```python
def multiple_params(self,
                        number,
                        precision,
                        string,
                        url)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| number |  ``` Required ```  | TODO: Add a parameter description |
| precision |  ``` Required ```  | TODO: Add a parameter description |
| string |  ``` Required ```  | TODO: Add a parameter description |
| url |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
number = 123412312
precision = 1112.34
string = '""test./;";12&&3asl"";"qw1&34"///..//.'
url = 'http://www.abc.com/test?a=b&c="http://lolol.com?param=no&another=lol"'

result = query_param_controller.multiple_params(number, precision, string, url)

```


### <a name="number_array"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.number_array") number_array

> TODO: Add a method description

```python
def number_array(self,
                     integers)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| integers |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
integers_value = "[1,2,3,4,5]"
integers = json.loads(integers_value)

result = query_param_controller.number_array(integers)

```


### <a name="string_array"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.string_array") string_array

> TODO: Add a method description

```python
def string_array(self,
                     strings)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| strings |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
strings_value = '["abc", "def"]'
strings = json.loads(strings_value)

result = query_param_controller.string_array(strings)

```


### <a name="simple_query"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.simple_query") simple_query

> TODO: Add a method description

```python
def simple_query(self,
                     boolean,
                     number,
                     string,
                     _optional_query_parameters=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| boolean |  ``` Required ```  | TODO: Add a parameter description |
| number |  ``` Required ```  | TODO: Add a parameter description |
| string |  ``` Required ```  | TODO: Add a parameter description |
| _optional_query_parameters | ``` Optional ``` | Additional optional query parameters are supported by this method |



#### Example Usage

```python
boolean = True
number = 4
string = 'TestString'
# key-value map for optional query parameters
optional_query_parameters = { }


result = query_param_controller.simple_query(boolean, number, string, optional_query_parameters)

```


### <a name="integer_enum_array"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.integer_enum_array") integer_enum_array

> TODO: Add a method description

```python
def integer_enum_array(self,
                           suites)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| suites |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
suites = [SuiteCode.HEARTS,SuiteCode.CLUBS,SuiteCode.DIAMONDS,SuiteCode.SPADES,SuiteCode.CLUBS]

result = query_param_controller.integer_enum_array(suites)

```


### <a name="string_enum_array"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.string_enum_array") string_enum_array

> TODO: Add a method description

```python
def string_enum_array(self,
                          days)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| days |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
days = [Days.TUESDAY,Days.SATURDAY,Days.MONDAY,Days.SUNDAY]

result = query_param_controller.string_enum_array(days)

```


### <a name="url_param"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.url_param") url_param

> TODO: Add a method description

```python
def url_param(self,
                  url)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| url |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
url = 'https://www.shahidisawesome.com/and/also/a/narcissist?thisis=aparameter&another=one'

result = query_param_controller.url_param(url)

```


### <a name="no_params"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.no_params") no_params

> TODO: Add a method description

```python
def no_params(self)
```

#### Example Usage

```python

result = query_param_controller.no_params()

```


### <a name="string_param"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.string_param") string_param

> TODO: Add a method description

```python
def string_param(self,
                     string)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| string |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
string = 'l;asd;asdwe[2304&&;\'.d??\\a\\\\\\;sd//'

result = query_param_controller.string_param(string)

```


### <a name="rfc_1123_date_time"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.rfc_1123_date_time") rfc_1123_date_time

> TODO: Add a method description

```python
def rfc_1123_date_time(self,
                           datetime)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetime |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetime = Sun, 06 Nov 1994 08:49:37 GMT

result = query_param_controller.rfc_1123_date_time(datetime)

```


### <a name="rfc_1123_date_time_array"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.rfc_1123_date_time_array") rfc_1123_date_time_array

> TODO: Add a method description

```python
def rfc_1123_date_time_array(self,
                                 datetimes)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetimes |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetimes_value = ["Sun, 06 Nov 1994 08:49:37 GMT","Sun, 06 Nov 1994 08:49:37 GMT"]
datetimes = json.loads(datetimes_value)

result = query_param_controller.rfc_1123_date_time_array(datetimes)

```


### <a name="rfc_3339_date_time_array"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.rfc_3339_date_time_array") rfc_3339_date_time_array

> TODO: Add a method description

```python
def rfc_3339_date_time_array(self,
                                 datetimes)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetimes |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetimes_value = ["1994-02-13T14:01:54.9571247Z","1994-02-13T14:01:54.9571247Z"]
datetimes = json.loads(datetimes_value)

result = query_param_controller.rfc_3339_date_time_array(datetimes)

```


### <a name="rfc_3339_date_time"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.rfc_3339_date_time") rfc_3339_date_time

> TODO: Add a method description

```python
def rfc_3339_date_time(self,
                           datetime)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetime |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetime = 1994-02-13T14:01:54.9571247Z

result = query_param_controller.rfc_3339_date_time(datetime)

```


### <a name="optional_dynamic_query_param"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.optional_dynamic_query_param") optional_dynamic_query_param

> get optional dynamic query parameter

```python
def optional_dynamic_query_param(self,
                                     name,
                                     _optional_query_parameters=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| name |  ``` Required ```  | TODO: Add a parameter description |
| _optional_query_parameters | ``` Optional ``` | Additional optional query parameters are supported by this method |



#### Example Usage

```python
name = 'farhan'
# key-value map for optional query parameters
optional_query_parameters = { }


result = query_param_controller.optional_dynamic_query_param(name, optional_query_parameters)

```


### <a name="unix_date_time_array"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.unix_date_time_array") unix_date_time_array

> TODO: Add a method description

```python
def unix_date_time_array(self,
                             datetimes)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetimes |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetimes_value = [1484719381,1484719381]
datetimes = json.loads(datetimes_value)

result = query_param_controller.unix_date_time_array(datetimes)

```


### <a name="unix_date_time"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.unix_date_time") unix_date_time

> TODO: Add a method description

```python
def unix_date_time(self,
                       datetime)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datetime |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
datetime = 1484719381

result = query_param_controller.unix_date_time(datetime)

```


### <a name="date_array"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.date_array") date_array

> TODO: Add a method description

```python
def date_array(self,
                   dates)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| dates |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
dates_value = ["1994-02-13","1994-02-13"]
dates = json.loads(dates_value)

result = query_param_controller.date_array(dates)

```


### <a name="date"></a>![Method: ](https://apidocs.io/img/method.png ".QueryParamController.date") date

> TODO: Add a method description

```python
def date(self,
                date)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| date |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
date = 1994-02-13

result = query_param_controller.date(date)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="template_params_controller"></a>![Class: ](https://apidocs.io/img/class.png ".TemplateParamsController") TemplateParamsController

### Get controller instance

An instance of the ``` TemplateParamsController ``` class can be accessed from the API Client.

```python
 template_params_controller = client.template_params
```

### <a name="send_string_array"></a>![Method: ](https://apidocs.io/img/method.png ".TemplateParamsController.send_string_array") send_string_array

> TODO: Add a method description

```python
def send_string_array(self,
                          strings)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| strings |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
strings_value = '["abc", "def"]'
strings = json.loads(strings_value)

result = template_params_controller.send_string_array(strings)

```


### <a name="send_integer_array"></a>![Method: ](https://apidocs.io/img/method.png ".TemplateParamsController.send_integer_array") send_integer_array

> TODO: Add a method description

```python
def send_integer_array(self,
                           integers)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| integers |  ``` Required ```  ``` Collection ```  | TODO: Add a parameter description |



#### Example Usage

```python
integers_value = "[1,2,3,4,5]"
integers = json.loads(integers_value)

result = template_params_controller.send_integer_array(integers)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="header_controller"></a>![Class: ](https://apidocs.io/img/class.png ".HeaderController") HeaderController

### Get controller instance

An instance of the ``` HeaderController ``` class can be accessed from the API Client.

```python
 header_controller = client.header
```

### <a name="send_headers"></a>![Method: ](https://apidocs.io/img/method.png ".HeaderController.send_headers") send_headers

> Sends a single header params

```python
def send_headers(self,
                     custom_header,
                     value)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customHeader |  ``` Required ```  | TODO: Add a parameter description |
| value |  ``` Required ```  | Represents the value of the custom header |



#### Example Usage

```python
custom_header = 'TestString'
value = 'TestString'

result = header_controller.send_headers(custom_header, value)

```


### <a name="get_message"></a>![Method: ](https://apidocs.io/img/method.png ".HeaderController.get_message") get_message

> TODO: Add a method description

```python
def get_message(self,
                    operation)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| operation |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
operation = 'operation'

header_controller.get_message(operation)

```


### <a name="get_message_1"></a>![Method: ](https://apidocs.io/img/method.png ".HeaderController.get_message_1") get_message_1

> TODO: Add a method description

```python
def get_message_1(self,
                      operation)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| operation |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
operation = 'operation'

header_controller.get_message_1(operation)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="echo_controller"></a>![Class: ](https://apidocs.io/img/class.png ".EchoController") EchoController

### Get controller instance

An instance of the ``` EchoController ``` class can be accessed from the API Client.

```python
 echo_controller = client.echo
```

### <a name="query_echo"></a>![Method: ](https://apidocs.io/img/method.png ".EchoController.query_echo") query_echo

> TODO: Add a method description

```python
def query_echo(self,
                   _optional_query_parameters=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| _optional_query_parameters | ``` Optional ``` | Additional optional query parameters are supported by this method |



#### Example Usage

```python
# key-value map for optional query parameters
optional_query_parameters = { }


result = echo_controller.query_echo(optional_query_parameters)

```


### <a name="json_echo"></a>![Method: ](https://apidocs.io/img/method.png ".EchoController.json_echo") json_echo

> Echo's back the request

```python
def json_echo(self,
                  input)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| input |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
input_value = "{\"uid\": \"1123213\", \"name\": \"Shahid\"}"
input = json.loads(input_value)

result = echo_controller.json_echo(input)

```


### <a name="form_echo"></a>![Method: ](https://apidocs.io/img/method.png ".EchoController.form_echo") form_echo

> Sends the request including any form params as JSON

```python
def form_echo(self,
                  input)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| input |  ``` Required ```  | TODO: Add a parameter description |



#### Example Usage

```python
input_value = "{\"uid\": \"1123213\", \"name\": \"Shahid\"}"
input = json.loads(input_value)

result = echo_controller.form_echo(input)

```


[Back to List of Controllers](#list_of_controllers)



