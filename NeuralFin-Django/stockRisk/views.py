from django.http import JsonResponse
from .stock_risk_calculator import calculate_entire_score

def stock_risk(request, symbol):
    try:
        score = calculate_entire_score(symbol)
        return JsonResponse({"symbol": symbol, "risk_score": score})
    except Exception as e:
        return JsonResponse({"error": str(e)})
