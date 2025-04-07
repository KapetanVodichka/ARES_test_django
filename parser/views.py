from django.shortcuts import render
from django.http import JsonResponse
from .services.api_service import ApiService
from .services.parsers import OnuDataParser, OnuStatsParser
from .services.data_processor import DataProcessor

# Create your views here.
def index(request):
    return render(request, 'parser/index.html')

def fetch_onu_data(request):
    try:
        api_service = ApiService()
        onu_data_parser = OnuDataParser()
        onu_stats_parser = OnuStatsParser()
        data_processor = DataProcessor(api_service, onu_data_parser, onu_stats_parser)
        data = data_processor.process(request.GET)
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)