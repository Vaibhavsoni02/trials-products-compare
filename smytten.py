import streamlit as st
import requests
import pandas as pd
import json

# List of keys to exclude from the DataFrame
exclude_keys = [
    'notify', 'status', 'bucks', 'redirect', 'header_text', 'video', 'cta', 
    'rating', 'basicFeedbackCash', 'basicFeedback', 'trending', 'fullSize', 
    'detailFeedback', 'favorite', 'price_drop_text', 'question2', 'question_title', 
    'units_left_text', 'no_rate_icon', 'no_rate_text', 'is_favorite', 'offer_text', 
    'discover_text', 'subtitle', 'badge_icon', 'featured_icon', 'product_count', 
    'summary', 'gift_text', 'free_gift_icon', 'placeholder_color', 'question', 
    'line_key', 'discount', 'line_value'
]

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
        #st.write(f"Fetching page {page_id}...")
        data = fetch_data(page_id)

        # Check if the 'content' and 'products' keys exist in the response
        if 'content' in data and 'products' in data['content']:
            all_products.extend(data['content']['products'])
        else:
            st.write(f"No products found on page {page_id}.")

    # Convert the products list into a DataFrame
    if all_products:
        df = pd.DataFrame(all_products)

        # Drop the unwanted columns based on the exclude_keys list
        df_filtered = df.drop(columns=[key for key in exclude_keys if key in df.columns])

        st.write("Filtered Products Data", df_filtered)
        # Title
        st.title("Product grid")

        # Display products in a horizontal grid
        cols = st.columns(4)  # Create columns dynamically based on the number of items
        
        for i, col in enumerate(cols):
            with col:
                # Access each row with .iloc[i]
                product = df_filtered.iloc[i]
                
                # Display Image
                st.image(product["image"], use_container_width=True)
                
                # Display Name
                st.markdown(f"### {product['name']}")
                
                # Display Author
                st.markdown(f"👤 {product['brand']}")
                
                

    else:
        st.write("No products data found.")



