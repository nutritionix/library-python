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
You can execute all methods in 3 ways.
####  Standard Search
```py
"""
This will perform a search. The object passed into this function
can contain all the perameters the API accepts in the `POST /v2/search` endpoint
"""
nutritionix.search({
    'q':'salad',
    # use these for paging
    'limit': 10,
    'offset': 0,
    # controls the basic nutrient returned in search
    'search_nutrient': 'calories'
})
```
###### or
```py
nutritionix.search(q='salad', limit=10, offset=0, search_nutrient='calories')
```
###### also
```py
nutritionix.search('salad', limit=10, offset=0)
```

#### Get Item By `id` or search `resource_id`
```py
# this will locate an item by its id or by a search `resource_id`
nutritionix.item(id='zgcjnYV')
```

#### Get Brand By `id`
```py
# this will locate a brand by its id
nutritionix.brand(id='bV')
```

#### Brand Search
```py
"""
This will perform a search. The object passed into this function
can contain all the perameters the API accepts in the `GET /v2/search/brands` endpoint

type: (1:restaurant, 2:cpg, 3:usda/nutritionix) defaults to undefined
"""
nutritionix.brand_search('just salad', limit=10, offset=0, type=1)
```
