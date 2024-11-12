# Repo progetto RO

## Getting Data from Coop website
Navigate to the data folder:
```bash
cd data
```

### Initialisation python venv
```bash
python -m venv dieta
source dieta/bin/activate
pip install -r Requirements.txt
```

### link sources
The links to the products are stored in the file ref.txt. This links are the links of all the products page of the site https://padova.easycoop.com, i got this by webscraping the site catalog (https://padova.easycoop.com/catalogsearch/result?q=&page=1 from page 1 to 320) with a python script using a docker container whit fireforx drivers and selenium similar to product_getter.py. searching for links in href of tag "a" with class "nuxt-link-prefetched product-tile__link". links are stored in tag format:
```
<a href=" Link to product " class="nuxt-link-prefetched product-tile__link"></a>
```
this way i got a list of 9570 links to the products of the site.

### Run the driver container
To run the driver container you need to have docker installed on your machine, navigate to the docker-selenium dir in the root file, then run the following command:
```bash
docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-firefox:4.26.0-20241101
```

### Run the data getter
To get the Coop products from a list of links of the site  https://padova.easycoop.com , make sure there are links in ref.txt updated (do webscraping if you need) then run the following command:

```bash
python product_getter.py
```
to run this you have to run the docker container.

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

