Pydantic is to use for validation, using Python type hints.

- If we don’t specify a default value in a pydantic model, the fields will be required.  
- The subclass of config can adjust the schema’s behaviour. [Here](https://pydantic.dev/docs/validation/1.10/usage/model_config/) are its options.  
- If you use “orm\_mode” for the pydantic schema, you need to instanciate it with “from\_orm”.  
- Pydantic doesn’t just validate. It also parses and converts. It makes sure about the output state of the model’s instance.  
- The configdict is for validation configuration (like, how long can a string be?). The options are [here](https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict).  
- We have model validators: after, before and something else. After validators will be run after the model instantiation.