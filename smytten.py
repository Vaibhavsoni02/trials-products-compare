import streamlit as st
import requests
import pandas as pd

# Function to make the API call
def fetch_data(page_id):
    url = "https://route.smytten.com/discover_item/app/products/list"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://smytten.com',
        'Referer': 'https://smytten.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
        'content-type': 'application/json',
        'request_type': 'web',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'uuid': 'fbe884cd-6e12-434b-907d-ce532fc27876',
        'web_version': '1'
    }

    data = {
        "type": "1_Trial_Point",
        "page": {
            "pageId": page_id
        },
        "brand_id": "",
        "trialfront_id": "",
        "id": "6780c6a76fdcec00011eb458",
        "timestamp": 0,
        "category_id": "",
        "subcategory_id": "",
        "collection_id": "",
        "search": "",
        "filters": {}
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Streamlit App
st.title('Product Data Fetcher')

# Button to fetch the data
if st.button('Fetch Products Data'):
    all_products = []

    # Loop over pages from 0 to 12
    for page_id in range(13):
        st.write(f"Fetching page {page_id}...")
        data = fetch_data(page_id)
        
        if 'products' in data:
            all_products.extend(data['products'])
        else:
            st.write(f"No products found on page {page_id}.")
        
    # Convert the products list into a DataFrame
    if all_products:
        df = pd.DataFrame(all_products)
        st.write("Products Data", df)
    else:
        st.write("No products data found.")

