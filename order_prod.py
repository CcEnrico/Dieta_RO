def read_products(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    products = content.strip().split('\n\n')
    return products

def parse_product(product_str):
    product_lines = product_str.split('\n')
    product_dict = {}
    for line in product_lines:
        key, value = line.split(': ', 1)
        product_dict[key] = value
    return product_dict

def remove_duplicates(products):
    seen = set()
    unique_products = []
    for product in products:
        product_tuple = tuple(product.items())
        if product_tuple not in seen:
            seen.add(product_tuple)
            unique_products.append(product)
    return unique_products

def sort_products(products):
    return sorted(products, key=lambda x: x['Brand'])

def write_products(file_path, products):
    with open(file_path, 'w') as file:
        for product in products:
            for key, value in product.items():
                file.write(f"{key}: {value}\n")
            file.write('\n')

def main():
    input_file = 'prod.txt'
    output_file = 'prod_sorted.txt'
    
    products_str = read_products(input_file)
    # for product_str in products_str:
    #     print(product_str + '\n')
    products = [parse_product(product_str) for product_str in products_str]
    unique_products = remove_duplicates(products)
    sorted_products = sort_products(unique_products)
    write_products(output_file, sorted_products)

if __name__ == "__main__":
    main()