""" Views for income. """
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from src.python.db.income import Income



def income_list(request, income_id):
    income_user = request.user
    inc_list = Income.get_income(income_user.id, income_id)
    print(inc_list, income_user.id)
    context = {'income_info': inc_list}
    print("Post", request.POST.get("name"))
    if request.POST:
        income_name = request.POST["name"]
        income_cur = request.POST["currency"]
        income_amount = request.POST["amount"]
        print(income_name, income_cur, income_amount)
        return HttpResponse(status=200)
        # return render(request, 'income/edit_income.html')
    return render(request, 'income/income_list.html', context)

@login_required
def edit_income(request):
    """View in a case of success request."""
    income_user = request.user
    inc_list = Income.get_income_list_by_user_id(income_user.id)
    print(inc_list, income_user.id)
    context = {'income_list': inc_list}
    if request.POST:
        income_id = request.POST["income_id"]
        print(income_id)
        #income_list(income_id)
        #return render_to_response('income/income_list.html', {'income_id': income_id},context_instance=RequestContext(request))
        return render(request, 'income/income_list.html', {'income_id': income_id})
    return render(request, 'income/edit_income.html', context)



# @login_required
# def income_list(request):
#     """View for a income list."""
#     if request.method == 'POST':
#         income_name = request.POST['result']
#         print(income_name)
#         return render(request, 'income/edit_income.html')
#     return HttpResponse('')



# @login_required
# def edit_income(request):
#     """View in a case of success request."""
#     if request.method == 'POST':
#         #income_name = request.POST['name']
#         return render(request, 'income/edit_income.html')
#     return render(request, 'income/edit_income.html')