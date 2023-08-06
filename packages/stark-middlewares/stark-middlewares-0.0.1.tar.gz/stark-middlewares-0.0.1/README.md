# stark_middlewares


## Install
  ```
  pip install stark_middlewares
  ```

## Usage
1. Add the below lines to trim request body middleware
  ```
  MIDDLEWARE += [
    from stark_middlewares.middlewares import TrimMiddleware
  ]
  ```
2. Add the below lines to add MAINTENANCE MODE middleware
  ```
  MIDDLEWARE += [
    from stark_middlewares.middlewares import MaintenanceModeMiddleware
  ]

  i. If you want to add the site under maintenance mode set IS_MAINTENANCE_MODE=True in settings

  ii. You can whitelist the IP using MAINTENANCE_IPS=[] in settings

  iii. You can able to check the invalid IP using SHOW_MAINTANCE_INVALID_IP=True in settings.
  ```

3. Add the below lines to add REST API Permission middleware
  ```
  MIDDLEWARE += [
    from stark_middlewares.middlewares import UserRolePermission
  ]

  i. DEFAULT ALLOWED_METHOD_PERMISSIONS:
    ALLOWED_METHOD_PERMISSIONS = {
        "list": "view_",
        "retrieve": "view_",
        "create": "add_",
        "partial_update": "change_",
        "delete": "delete_",
        "change_status": "change_",
        "bulk_delete": "add_",
    }

  ii. If you want to add more permission you can just add ALLOWED_METHOD_PERMISSIONS in settings.
  e.g. ALLOWED_METHOD_PERMISSIONS = {
    'get_list': 'add_'
  }

  iii. If you want to check the permission error then add SHOW_PERMISSION_ERROR=True in settings.


  ```