from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from .forms import CompanyForm, CompanyFormUpdate, CompanyAddressForm, CompanyAddressFormHelper
from .models import Company, CompanyAddress


# Home page
def home(request):
    return render(request, 'company/home.html')


# Show page with company list
def company(request):
    return render(request, 'company/company_list.html')


# Function to be used by ajax to generate company list
def getCompanyList(request):
    if request.method == "GET" and request.is_ajax():
        try:
            companies = list(Company.objects.all().values())
            data = dict()
            data['data'] = companies
        except:
            return JsonResponse({"success": False}, status=400)

        return JsonResponse(data, status=200)

    return JsonResponse({"success": False}, status=400)


# Shows each company information.
# Company details can be edited at this page (yet to implement this function)
def getCompanyDetails(request, pk):
    company = get_object_or_404(Company, pk=pk)
    addresses = CompanyAddress.objects.filter(
        company=company).order_by('zipCode')
    form_address = CompanyAddressForm()
    context = {
        'company': company,
        'addresses': addresses,
        'addressForm': form_address,
    }
    return render(request, 'company/company_details.html', context)


# Update company details
def updateCompanyDetails(request, pk):
    company = get_object_or_404(Company, pk=pk)
    form_company = CompanyFormUpdate(request.POST or None, instance=company)

    CompanyAddressFormSet = inlineformset_factory(
        Company, CompanyAddress, fields=('__all__')
    )
    data = dict()
    if request.method == "POST" and request.is_ajax():
        adressesFormSet = CompanyAddressFormSet(
            request.POST, request.FILES, instance=company)
        if form_company.is_valid():
            form_company.save()

        if adressesFormSet.is_valid():
            adressesFormSet.save()
            data['message'] = 'Company created successfully'
            data['success'] = True
            return JsonResponse(data, status=200)
    else:
        adressesFormSet = CompanyAddressFormSet(instance=company)
        helper = CompanyAddressFormHelper()

    context = {
        'companyForm': form_company,
        'addresses': adressesFormSet,
        'helper': helper,
    }

    return render(request, 'company/company_update.html', context)


# View with form to Create a new company
def newCompanytPage(request):
    form_company = CompanyForm()

    context = {
        'companyForm': form_company,
    }
    return render(request, 'company/company_create.html', context)


# Function to be used by ajax to register the new company
def postNewCompany(request):
    data = dict()
    if request.method == "POST" and request.is_ajax():
        form_company = CompanyForm(request.POST)
        form_company.save()
        data['message'] = 'Company created successfully'
        data['success'] = True
        return JsonResponse(data, status=200)

    data['message'] = 'Error creating company. Contact system administrator'
    data['success'] = False
    return JsonResponse(data, status=400)


@csrf_protect
def deleteCompany(request, pk):
    if request.method == "POST" and request.is_ajax():
        data = dict()
        company = Company.objects.get(pk=pk)
        if company:
            company.delete()
            data['message'] = "Company deleted!"
        else:
            data['message'] = "Error!"
        return JsonResponse(data)


def newAddressPage(request):
    # company = get_object_or_404(Company, pk=pk)
    form_address = CompanyAddressForm()
    context = {
        'company': company,
        'addressForm': form_address
    }
    return render(request, 'company/address_create.html', context)


def postNewAddress(request):
    data = dict()
    if request.method == "POST" and request.is_ajax():
        form_address = CompanyAddressForm(request.POST)
        form_address.save()
        data['message'] = 'Company created successfully'
        data['success'] = True
        return JsonResponse(data, status=200)

    data['message'] = 'Error creating company. Contact system administrator'
    data['success'] = False
    return JsonResponse(data, status=400)
