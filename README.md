# Repo progetto RO

## Initialisation python venv
```bash
python -m venv dieta
source dieta/bin/activate
pip install -r Requirements.txt
```

## Run the project
To get the Coop products from a list of links of the site  https://padova.easycoop.com , make shure there link ins ref.txt are updated (do webscraping if you need) then run the following command:

```bash
python product_getter.py
```

This will get you a list of product in the file products.json in the format:
```json
{
    "Brand": "",
    "Name": "",
    "Price per quantity": "",
    "Price": "",
    "Nutritional values": {},
    "Url": "https://padova.easycoop.com/..."
}
``` 

