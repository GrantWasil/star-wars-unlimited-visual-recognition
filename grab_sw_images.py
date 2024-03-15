import os
import requests
from bs4 import BeautifulSoup

url = 'https://swudb.com/sets/SOR/fullset'

print(f"Retrieving HTML response from: {url}")

try:
    response = requests.get(url)
    
    if response.status_code == 200:
        html_response = response.text
        with open('source.html', 'w') as file:
            file.write(html_response)
        print("HTML response saved to source.html")
        print("HTML response retrieved successfully")

        os.makedirs('cards', exist_ok=True)
        os.makedirs('cache', exist_ok=True)

        soup = BeautifulSoup(html_response, 'html.parser')

        with open('labels.txt', 'w') as label_file:
            div_tags = soup.find_all('div', class_='col-12 text-center')
            print(f"Found {len(div_tags)} div tags with class 'col-12 text-center'")

            processed_cards = set()

            for div_tag in div_tags:
                separator_div = div_tag.find('div', class_='separator mt-5 mb-3')

                if separator_div:
                    current_variant = separator_div.text.strip()
                    current_variant = current_variant.split(" ")[0]
                    print(f"Found separator div with text: {current_variant}")

                    card_div_tags = div_tag.find_next_siblings('div', class_='col-6 col-md-4 col-lg-3 card-search-col')

                    print(f"Found {len(card_div_tags)} card div tags")
                    for card_div in card_div_tags:
                        link = card_div.find('a')
                        if link is not None:
                            try:
                                card_name = link['href'].split('/')[-1]
                                card_name = card_name.replace(' ', '_')
                                card_name_variant = card_name + f'_{current_variant}'

                                if card_name_variant not in processed_cards:
                                    processed_cards.add(card_name_variant)

                                    image_tag = link.find('img')
                                    if image_tag is not None:
                                        image_url = image_tag['src']
                                        print(f"Processing card: {card_name}, Image URL: {image_url}")

                                        cache_filename = f"cache/{os.path.basename(image_url)}"

                                        if not os.path.exists(cache_filename):
                                            image_response = requests.get(f"https://swudb.com{image_url}")

                                            if image_response.status_code == 200:
                                                with open(cache_filename, 'wb') as cache_file:
                                                    cache_file.write(image_response.content)
                                                print(f"Image downloaded and cached for card: {card_name}")
                                            else:
                                                print(f"Failed to download image for card: {card_name}")

                                        image_filename = f"cards/{card_name_variant}.jpg"

                                        if not os.path.exists(card_name_variant):
                                            with open(cache_filename, 'rb') as cache_file, open(image_filename, 'wb') as image_file:
                                                image_file.write(cache_file.read())

                                            label_file.write(f"{image_filename}\t{card_name}\t{current_variant}\n")
                                    else:
                                        print(f"No image found for card: {card_name}")

                            except (KeyError, AttributeError) as e:
                                print(f"Error processing card: {card_name}")
                                print(str(e))

    else:
        print(f"Failed to retrieve the HTML response. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print("An error occurred while retrieving the HTML response:")
    print(str(e))