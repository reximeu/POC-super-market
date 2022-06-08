import pandas
import requests
from datetime import datetime


def mercadona_scrape():
    current_date = datetime.now().strftime("%Y-%m-%d")
    records = []

    try:
        categories_url = f"https://tienda.mercadona.es/api/v1_1/categories/"
        categories = requests.request('get', categories_url).json()
        

        for category in categories.get('results', []):
            category_id = category.get('id')
            category_url = f"https://tienda.mercadona.es/api/v1_1/categories/{category_id}"

            category = requests.request('get', category_url).json()
            category_name = category.get('name')

            for subcategory in category.get('categories'):
                subcategory_id = subcategory.get('id')
                subcategory_name = subcategory.get('name')

                for product in subcategory.get('products'):
                    product_id = product.get('id')
                    product_name = product.get('display_name')
                    product_price_ins = product.get('price_instructions')
                    price_unit = product_price_ins.get('unit_price')
                    price_bulk = product_price_ins.get('bulk_price')
                    price_iva = product_price_ins.get('iva')

                    print(f"{category_name} {subcategory_name} {product_name}")

                    new_row = {
                        'current_date': current_date,
                        'category_id': category_id,
                        'category_name': category_name,
                        'subcategory_id': subcategory_id,
                        'subcategory_name': subcategory_name,
                        'product_id': product_id,
                        'product_name': product_name,
                        'price_unit': price_unit,
                        'price_bulk': price_bulk,
                        'price_iva': price_iva
                    }

                    records.append(new_row)

        df = pandas.DataFrame.from_records(records)
        df.columns = [
            'current_date',
            'category_id', 
            'category_name',
            'subcategory_id',
            'subcategory_name',
            'product_id',
            'product_name',
            'price_unit',
            'price_bulk',
            'price_iva',
        ]

        df.to_csv(f'datasets/{current_date}.csv')
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == '__main__':
    mercadona_scrape()

