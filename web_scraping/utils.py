import requests
from bs4 import BeautifulSoup

def format_prices(price):
    price_str = price.replace('.','').replace('$','')
    price_fix = float(price_str)
    return round(price_fix,1)

def format_percentage(percentage):
    simbol = percentage.find('%')
    percentage_new = percentage[:simbol]
    return int(percentage_new)

def format_seller(seller):
    return seller[4:]

def format_rating(rating):
    new_rating = rating[13:16]
    if 'd' in new_rating:
        rating_fix = new_rating[0:1]
        return float(rating_fix)
    else:
        return float(new_rating)
    
def check_tags(value,tags,type):
    for tag in tags:
        element = value.find('span',class_=tag)
        if element:
            value2return = ''
            match type:
                case 'percentage':
                    value2return = format_percentage(element.text.strip())
                case 'seller':
                    value2return = format_seller(element.text.strip())
                case 'rating':
                    value2return = format_rating(element.text.strip())
            return value2return
        else:
            return ''
        
def check_img_url(item):
    img = item.find('img',class_='poly-component__picture')
    if img and ('data-src' in img.attrs):
        return img['data-src']
    elif img and ('src' in img.attrs):
        return img['src']
        
def prepare_data(content):
    items = []
    for item in content.find_all('li',class_='ui-search-layout__item shops__layout-item'):
        name = item.find('h2', class_='poly-box poly-component__title').text.strip()
        original_price =  format_prices(item.find('span', class_='andes-money-amount__fraction').text.strip())
        discounted_price = format_prices(item.find('span', class_='andes-money-amount andes-money-amount--cents-superscript').text.strip())
        discount_percentage = check_tags(item,['andes-money-amount__discount'],'percentage')
        seller = check_tags(item,['poly-component__seller'],'seller')
        rating = check_tags(item,['andes-visually-hidden'],'rating')
        img_url = check_img_url(item)
        product_url = item.find('a')['href']
        
        items.append({
            "name": name,
            "original_price": original_price,
            "discounted_price": discounted_price,
            "discount_percentage": discount_percentage,
            "seller":{
                "name":seller
            },
            "rating":rating,
            "img_url":img_url,
            "product_url":product_url
        })
        
    return items

def scraping_request(query_param):
    url = f"https://listado.mercadolibre.com.co/{query_param}"
    headers = {
        'User-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url,headers=headers)
        
    if response.status_code != 200:
        return {
            'request_result':False,
            'error_code':'Request failed.'
        }
    
    response_content = BeautifulSoup(response.content,'html.parser')
    if  response_content:
        request_body = prepare_data(response_content)
        return {
            'request_result':True,
            'total_results':len(request_body),
            'request_body':request_body
        }
    else:
        return {
            'request_result':False,
            'error_code':'No body request available.'
        }
    
def make_request(query_parameter):
    url = f'http://127.0.0.1:8000/web_scraping/search/?query={query_parameter}'
    try:
        response = requests.get(url)
    except Exception as e:
        raise e
    else:
        url = f'http://127.0.0.1:8000/web_scraping/get_etl/'
        response = requests.get(url)
        result = response.json()
        return result
        
    '''
    response = {
        "etl_result": {
            "average_price": 2704435.46,
            "max_price_item": {
                "name": "LG Oled Flex Curvo Flexible 4k Uhd Hdr 120 Hz Smart Tv 42-in",
                "original_price": 13183900.0,
                "discounted_price": 13183900.0,
                "discount_percentage": "",
                "seller": {
                    "name": ""
                },
                "rating": "",
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_695297-MCO69773922524_062023-V.webp",
                "product_url": "https://articulo.mercadolibre.com.co/MCO-1039425753-lg-oled-flex-curvo-flexible-4k-uhd-hdr-120-hz-smart-tv-42-in-_JM#polycard_client=search-nordic&position=52&search_layout=stack&type=item&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e"
            },
            "min_price_item": {
                "name": "Tv Caixun 32  Led Hd Smart Tv Cx32f1sm Wifi Android 7.1",
                "original_price": 1538167.0,
                "discounted_price": 922900.0,
                "discount_percentage": 40,
                "seller": {
                    "name": ""
                },
                "rating": "",
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_821321-MCO41746077930_052020-V.webp",
                "product_url": "https://www.mercadolibre.com.co/tv-caixun-32-led-hd-smart-tv-cx32f1sm-wifi-android-71/p/MCO20538778#polycard_client=search-nordic&searchVariation=MCO20538778&position=10&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO1178535382&sid=search"
            },
            "max_discount_item": {
                "name": "Televisor LG 50'' 4k- Uhd Ai Thinq - Smart Tv Webos 23 Ai",
                "original_price": 4299900.0,
                "discounted_price": 1679900.0,
                "discount_percentage": 60,
                "seller": {
                    "name": "LG Electronics Colombia"
                },
                "rating": 5.0,
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_727964-MLU78780266068_092024-V.webp",
                "product_url": "https://www.mercadolibre.com.co/televisor-lg-50-4k-uhd-ai-thinq-smart-tv-webos-23-ai/p/MCO37195942#polycard_client=search-nordic&searchVariation=MCO37195942&position=19&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO1440776985&sid=search"
            },
            "max_rating_item": {
                "name": "Televisor LG Led 43 Pulgadas 4k Uhd 43ut7300psa",
                "original_price": 2500000.0,
                "discounted_price": 1309900.0,
                "discount_percentage": 47,
                "seller": {
                    "name": "Electro Online"
                },
                "rating": 5.0,
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_749334-MLU77107778694_062024-V.webp",
                "product_url": "https://www.mercadolibre.com.co/televisor-lg-led-43-pulgadas-4k-uhd-43ut7300psa/p/MCO37925935#polycard_client=search-nordic&searchVariation=MCO37925935&position=17&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO2583991770&sid=search"
            }
        },
        'response_body':
            [
        
                {
                    "name": "Televisor LG 43 Pulgadas 108 Cm 43lm6370pdb Fhd Led Plano Smart Tv",
                    "original_price": 1499900.0,
                    "discounted_price": 1099900.0,
                    "discount_percentage": 26,
                    "seller": {
                        "name": "Electro Online"
                    },
                    "rating": 4.8,
                    "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_975043-MLU77517187669_072024-V.webp",
                    "product_url": "https://www.mercadolibre.com.co/televisor-lg-43-pulgadas-108-cm-43lm6370pdb-fhd-led-plano-smart-tv/p/MCO18453148#polycard_client=search-nordic&searchVariation=MCO18453148&position=6&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO1324419115&sid=search"
                },
            {
                "name": "Televisor LG 65 Uhd 4k Ia 5 Smart Tv Magic Remote",
                "original_price": 2599900.0,
                "discounted_price": 2391900.0,
                "discount_percentage": 8,
                "seller": {
                    "name": "Electro Online"
                },
                "rating": 4.9,
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_958892-MLA79462481799_092024-V.webp",
                "product_url": "https://www.mercadolibre.com.co/televisor-lg-65-uhd-4k-ia-5-smart-tv-magic-remote/p/MCO36214829#polycard_client=search-nordic&searchVariation=MCO36214829&position=9&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO1480374911&sid=search"
            },
            {
                "name": "Televisor LG 50 4k-uhd Led Smart Tv",
                "original_price": 1539096.0,
                "discounted_price": 1499900.0,
                "discount_percentage": 2,
                "seller": {
                    "name": ""
                },
                "rating": "",
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_612503-MLU78682801053_082024-V.webp",
                "product_url": "https://www.mercadolibre.com.co/televisor-lg-50-4k-uhd-led-smart-tv/p/MCO39765651#polycard_client=search-nordic&searchVariation=MCO39765651&position=12&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO2665595184&sid=search"
            },
            {
                "name": "Televisor LG Led 43 Pulgadas 4k Uhd 43ut7300psa",
                "original_price": 2500000.0,
                "discounted_price": 1309900.0,
                "discount_percentage": 47,
                "seller": {
                    "name": "Electro Online"
                },
                "rating": 5.0,
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_749334-MLU77107778694_062024-V.webp",
                "product_url": "https://www.mercadolibre.com.co/televisor-lg-led-43-pulgadas-4k-uhd-43ut7300psa/p/MCO37925935#polycard_client=search-nordic&searchVariation=MCO37925935&position=17&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO2583991770&sid=search"
            },
            {
                "name": "Televisor 55 LG 55ur7300psa Smart Tv 4k Uhd Bluetooth",
                "original_price": 1840000.0,
                "discounted_price": 1759900.0,
                "discount_percentage": 4,
                "seller": {
                    "name": ""
                },
                "rating": 4.9,
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_833139-MLU79106359271_092024-V.webp",
                "product_url": "https://www.mercadolibre.com.co/televisor-55-lg-55ur7300psa-smart-tv-4k-uhd-bluetooth/p/MCO26515255#polycard_client=search-nordic&searchVariation=MCO26515255&position=20&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO1940234348&sid=search"
            },
            {
                "name": "Pantalla LG Oled 55 Pulgadas 4k Smart Tv 2024 Oled55b4psa",
                "original_price": 4750000.0,
                "discounted_price": 4750000.0,
                "discount_percentage": "",
                "seller": {
                    "name": ""
                },
                "rating": "",
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_770267-MLU79266661671_092024-V.webp",
                "product_url": "https://www.mercadolibre.com.co/pantalla-lg-oled-55-pulgadas-4k-smart-tv-2024-oled55b4psa/p/MCO40794498#polycard_client=search-nordic&searchVariation=MCO40794498&position=16&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO1488256921&sid=search"
            },
            {
                "name": "LG Pantalla 65 Pulgadas Led 4k Uhd Ai Smart Tv Modelo 2024",
                "original_price": 2339900.0,
                "discounted_price": 2339900.0,
                "discount_percentage": "",
                "seller": {
                    "name": ""
                },
                "rating": "",
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_701241-MLA79331637240_092024-V.webp",
                "product_url": "https://www.mercadolibre.com.co/lg-pantalla-65-pulgadas-led-4k-uhd-ai-smart-tv-modelo-2024/p/MCO41212092#polycard_client=search-nordic&searchVariation=MCO41212092&position=18&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO1485557819&sid=search"
            }, {
                "name": "Televisor Led Smart Tv LG 65'' 4k Uhd Tv 65ur7300psa 2023",
                "original_price": 2339900.0,
                "discounted_price": 2339900.0,
                "discount_percentage": "",
                "seller": {
                    "name": ""
                },
                "rating": "",
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_833060-MLU79125009834_092024-V.webp",
                "product_url": "https://www.mercadolibre.com.co/televisor-led-smart-tv-lg-65-4k-uhd-tv-65ur7300psa-2023/p/MCO27129040#polycard_client=search-nordic&searchVariation=MCO27129040&position=21&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO1940299634&sid=search"
            },
            {
                "name": "Televisor LG 55 pulgadas 55UR7800PSB.AWC Uhd Ai Thinq 55  4k Smart Tv Negro",
                "original_price": 1799900.0,
                "discounted_price": 1799900.0,
                "discount_percentage": "",
                "seller": {
                    "name": ""
                },
                "rating": "",
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_907876-MLU77624462751_072024-V.webp",
                "product_url": "https://www.mercadolibre.com.co/televisor-lg-55-pulgadas-55ur7800psbawc-uhd-ai-thinq-55-4k-smart-tv-negro/p/MCO25684999#polycard_client=search-nordic&searchVariation=MCO25684999&position=15&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO1764769254&sid=search"
            },
            {
                "name": "Televisor LG 50'' 4k- Uhd Ai Thinq - Smart Tv Webos 23 Ai",
                "original_price": 4299900.0,
                "discounted_price": 1679900.0,
                "discount_percentage": 60,
                "seller": {
                    "name": "LG Electronics Colombia"
                },
                "rating": 5.0,
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_727964-MLU78780266068_092024-V.webp",
                "product_url": "https://www.mercadolibre.com.co/televisor-lg-50-4k-uhd-ai-thinq-smart-tv-webos-23-ai/p/MCO37195942#polycard_client=search-nordic&searchVariation=MCO37195942&position=19&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO1440776985&sid=search"
            },
            {
                "name": "Televisor LG 65 pulgadas 65UR7800PSB.AWC Uhd Ai Thinq 4k Smart Tv",
                "original_price": 2399900.0,
                "discounted_price": 2399900.0,
                "discount_percentage": "",
                "seller": {
                    "name": "LG Electronics Colombia"
                },
                "rating": 5.0,
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_957865-MLA79464417627_092024-V.webp",
                "product_url": "https://www.mercadolibre.com.co/televisor-lg-65-pulgadas-65ur7800psbawc-uhd-ai-thinq-4k-smart-tv/p/MCO25578427#polycard_client=search-nordic&searchVariation=MCO25578427&position=22&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO1466355667&sid=search"
            },
            {
                "name": "Smart TV de 55\" LG AI ThinQ 55UN7100 con pantalla LED 4K 110/220V",
                "original_price": 1789900.0,
                "discounted_price": 1789900.0,
                "discount_percentage": "",
                "seller": {
                    "name": ""
                },
                "rating": 4.9,
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_934254-MLA44405781838_122020-V.webp",
                "product_url": "https://www.mercadolibre.com.co/smart-tv-de-55-lg-ai-thinq-55un7100-con-pantalla-led-4k-110220v/p/MCO16233430#polycard_client=search-nordic&searchVariation=MCO16233430&position=25&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO613318228&sid=search"
            },
            {
                "name": "Televisor LG 65 Uhd 4k Procesador Ia A5 Smart Tv",
                "original_price": 2399900.0,
                "discounted_price": 2399900.0,
                "discount_percentage": "",
                "seller": {
                    "name": "LG Electronics Colombia"
                },
                "rating": 4.7,
                "img_url": "https://http2.mlstatic.com/D_Q_NP_2X_888297-MLU72566244256_112023-V.webp",
                "product_url": "https://www.mercadolibre.com.co/televisor-lg-65-uhd-4k-procesador-ia-a5-smart-tv/p/MCO27094729#polycard_client=search-nordic&searchVariation=MCO27094729&position=4&search_layout=stack&type=product&tracking_id=9c27fde0-0959-4e91-9b06-42881d76ab8e&wid=MCO2471585874&sid=search"
            }
        ]
    }
    return response
    '''
 
        