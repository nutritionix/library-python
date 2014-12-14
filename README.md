Official Nutritionix Python Client
==================================
 
### Installation

```shell
pip install nutritionix
```
 
```py
# import inside your project
from nutritionix import NutritionixClient
 
 nutritionix = NutritionixClient(
	    application_id='YOUR_APP_ID',
	    api_key='YOUR_API_KEY',
	    # debug=True, # defaults to False
)
```

### Usage

#### Get Item By `id` or search `resource_id`
You can execute methods in 3 ways
```py
# this will locate an item by its id or by a search `resource_id`
nutritionix.item({'id': 'bV'})
```
###### or
```py
nutritionix.item(id='bV')
```
###### also
```py
nutritionix.item('bV')
```
