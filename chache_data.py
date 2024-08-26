from bs4 import BeautifulSoup
import json
import os
import requests

# Load and parse the HTML file from public directory
with open('public/saved_page.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Create a folder to store images locally in public/assets
if not os.path.exists('public/assets/images'):
    os.makedirs('public/assets/images')

menu_items = []
current_category = None

# Extract menu items with categories
for element in soup.find_all(['h2', 'h3', 'div']):  # Adjust these tags as per your HTML structure
    # Check if this element is a category header
    if element.name in ['h2', 'h3'] and not element.find_all('div'):  # Assuming categories are within h2 or h3 tags
        current_category = element.get_text().strip()  # Capture the current category
    # Check if this element is a menu item
    elif element.has_attr('data-test-id') and element['data-test-id'] == 'horizontal-item-card':
        name = element.select_one('h3').text if element.select_one('h3') else 'No Name'
        description = element.select_one('p').text if element.select_one('p') else 'No Description'
        price = element.select_one('[data-test-id="horizontal-item-card-price"]').text if element.select_one('[data-test-id="horizontal-item-card-price"]') else 'No Price'
        image_tag = element.select_one('img')
        image_url = image_tag['src'] if image_tag else 'No Image'

        # Download the image locally if it exists
        if image_tag and image_url.startswith('http'):
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                if content_type:
                    if 'image/jpeg' in content_type:
                        extension = '.jpg'
                    elif 'image/png' in content_type:
                        extension = '.png'
                    elif 'image/webp' in content_type:
                        extension = '.webp'
                    else:
                        extension = ''  # Handle other image formats or leave blank

                img_filename = os.path.basename(image_url)
                if not img_filename.endswith(extension):
                    img_filename += extension

                img_path = f'public/assets/images/{img_filename}'
                with open(img_path, 'wb') as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
                # Replace remote URL with local path for React usage
                image_url = f'/assets/images/{img_filename}'

        menu_items.append({
            'category': current_category,  # Add the category to the menu item
            'name': name,
            'description': description,
            'price': price,
            'image': image_url
        })

# Save the structured data for React in public/data
if not os.path.exists('public/data'):
    os.makedirs('public/data')

with open('public/data/menu_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(menu_items, json_file, ensure_ascii=False, indent=2)

print("Menu data with categories has been saved to public/data/menu_data.json")

# [
#   {
#     "category": "alkuruoka",
#     "name": "Kevätkääryle vihannes",
#     "description": "No description available",
#     "price": "4,50 €",
#     "image": "/assets/images/some-image.jpg"
#   },
#   {
#     "category": "keitto",
#     "name": "Misokeitto",
#     "description": "Delicious miso soup",
#     "price": "3,00 €",
#     "image": "/assets/images/some-other-image.jpg"
#   }
# ]
