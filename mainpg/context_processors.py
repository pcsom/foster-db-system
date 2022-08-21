from .models import ReqFormSettings, PickupSettings

def formSettings(request):
    return {'formSettings': ReqFormSettings.load()}

    
def pickSettings(request):
    return {'pickSettings': PickupSettings.load()}