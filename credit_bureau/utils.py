from .models import UserResponse

def calculate_credit_score(user):
    print(user)
    responses = UserResponse.objects.filter(user=user)
    total_score = sum(response.get_score() for response in responses)
    print('total score',total_score,responses )
    return total_score