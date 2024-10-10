from django.shortcuts import render
from django.views.generic import ListView

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .utils import scraping_request
from .forms import ScrapingForm
from .utils import make_request
from django.contrib import messages

# Create your views here.
scraping_result = {}

def index_scraping_view(request):
    queryset = make_request('')    
    if request.method == 'GET':
        query_form = ScrapingForm()
    elif request.method == 'POST':
        query_form = ScrapingForm(request.POST)
        if query_form.is_valid():
            queryset = make_request(query_form.cleaned_data['quey_parameter'])
        else:
            messages.error(request=request,message='Your filter has some issues, please fix and try again.')
    return render(
        request=request,
        template_name='web_scraping/index_scraping.html',
        context = {
            'query_form':query_form,
            'request_body':queryset.get('request_body'),
            'etl_result':queryset.get('etl_result')
        }
    )
            
@api_view(['GET'])
def search(request):
    query = request.query_params.get('query',None)
    if query:
        products = scraping_request(query)
        if products.get('request_result'):
            scraping_result['body'] = products.get('request_body')
            return Response(
                data = {
                    'request_status':True,
                    'total_results':products.get('total_results'),
                    'request_body': products.get('request_body')
                },
                status=status.HTTP_200_OK
            )
        else:#Web scraping failed
            return Response(
                data = {
                    'request_result':False,
                    "error_code": "Request body unavailable."
                },
                status=status.HTTP_200_OK
            )
    else:#Query parameter unavailable
        return Response(
            data = {
                'request_result':False,
                "error_code": "Query parameter is mandatory."
            },
            status=status.HTTP_200_OK
        )
        
@api_view(['GET'])
def get_etl(request):
    if 'body' in scraping_result:
        request_body = scraping_result['body']
        price_sum = 0
        max_price = 0
        min_price = 10*1000000
        max_discount = 0
        max_rating = 0
        etl_result = {
            'max_price_item':'',
            'min_price_item':'',
            'max_discount_item':'',
            'max_rating_item':'',
        }
        for pos,body in enumerate(request_body):
            price_sum += body['discounted_price']
            
            #Prices analysis
            if body['discounted_price']:
                #highest price
                if body['discounted_price'] > max_price:
                    max_price = body['discounted_price']
                    etl_result['max_price_item'] = pos
                    
                #Lowest price
                if body['discounted_price'] < min_price:
                    min_price = body['discounted_price']
                    etl_result['min_price_item'] = pos
            
            #Discount analysis
            if body['discount_percentage']:
                if body['discount_percentage'] > max_discount:
                    max_discount = body['discount_percentage']
                    etl_result['max_discount_item'] = pos
                    
            #Rating analysis
            if body['rating']:
                if body['rating'] > max_rating:
                    max_rating = body['rating']
                    etl_result['max_rating_item'] = pos
            
            
        average_price = round(price_sum/len(request_body),2)
        
        '''
        print(etl_result)
        print(f'average_price: {average_price}')
        print(f'Item more expensive: {request_body[etl_result['max_price_item']]['discounted_price']}')
        print(f'Item more cheap: {request_body[etl_result['min_price_item']]['discounted_price']}')
        print(f'Item with more discount: {request_body[etl_result['max_discount_item']]['discount_percentage']}')
        print(f'Item with better rating: {request_body[etl_result['max_rating_item']]['rating']}')        
        '''
        
        return Response(
            data = {
                'request_result':True,
                'request_body':request_body,
                'etl_result':{
                    'average_price':average_price,
                    'max_price_item':request_body[etl_result['max_price_item']],
                    'min_price_item':request_body[etl_result['min_price_item']],
                    'max_discount_item':request_body[etl_result['max_discount_item']],
                    'max_rating_item':request_body[etl_result['max_rating_item']]
                }
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            data = {
                'request_result':False,
                "error_code": "Result not available"
            },
            status=status.HTTP_200_OK
        ) 
