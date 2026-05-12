from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Employee
from .forms import UserForm, EmployeeForm
from django.shortcuts import render
from .models import Department, Policy, Contact     


# Home Page
def home(request):
    return render(request, 'employees/home.html')


# Register Employee
def register(request):

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        emp_form = EmployeeForm(request.POST, request.FILES)

        if user_form.is_valid() and emp_form.is_valid():

            user = user_form.save()
            employee = emp_form.save(commit=False)

            employee.user = user
            employee.save()

            return redirect('login')

    else:
        user_form = UserForm()
        emp_form = EmployeeForm()

    return render(request, 'employees/register.html', {
        'user_form': user_form,
        'emp_form': emp_form
    })


# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'employees/login.html', {
                'error': 'Invalid username or password'
            })
    return render(request, 'employees/login.html')


# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# User Dashboard
@login_required
@login_required
def dashboard(request):
    employee = Employee.objects.filter(user=request.user).first()

    return render(request, 'employees/dashboard.html', {
        'employee': employee
    })


# Employee List
@login_required
def employee_list(request):

    employees = Employee.objects.all()

    return render(request, 'employees/employee_list.html', {
        'employees': employees
    })


# Admin Dashboard
def admin_dashboard(request):

    employees = Employee.objects.all()

    context = {
        'employees': employees,
        'total_employees': employees.count(),
        'approved': employees.filter(status='Approved').count(),
        'pending': employees.filter(status='Pending').count(),
    }

    return render(request, 'employees/admin_dashboard.html', context)
# Approve Employee
@login_required
def approve_employee(request, id):

    employee = get_object_or_404(Employee, id=id)

    employee.status = 'Approved'
    employee.save()

    return redirect('admin_dashboard')


# Reject Employee
@login_required
def reject_employee(request, id):

    employee = get_object_or_404(Employee, id=id)

    employee.status = 'Rejected'
    employee.save()

    return redirect('admin_dashboard')
#policies 
def policies(request):
    return render(request, 'employees/policies.html')

#instructions

def hr_instructions(request):
    return render(request, 'employees/hr_instructions.html')

# Upload Documents
def upload_documents(request):
    # Yahan example ke liye employee ko hardcode kiya hai
    employee = Employee.objects.first()  # aap real user session se fetch kar sakte ho

    if request.method == 'POST':
        if 'aadhar' in request.FILES:
            employee.aadhar = request.FILES['aadhar']
        if 'resume' in request.FILES:
            employee.resume = request.FILES['resume']
        employee.save()
        return redirect('upload_documents')  # page reload karke files dikhaye

    return render(request, 'employees/upload_documents.html', {'employee': employee})

# Joining Process
def joining_process(request):
    return render(request, 'employees/joining_process.html')


# Dashboard Access
def dashboard_access(request):
    return render(request, 'employees/dashboard_access.html')


# Approval Status
def approval_status(request):
    # currently logged-in employee fetch karo
    employee = Employee.objects.first()  # real project me request.user se fetch karein
    return render(request, 'employees/approval_status.html', {
        'employee': employee
    })

# Company Details
def company_details(request):
    departments = Department.objects.all()
    policies = Policy.objects.all()
    contacts = Contact.objects.all()
    context = {
        'departments': departments,
        'policies': policies,
        'contacts': contacts,
    }
    return render(request, 'employees/company_details.html', context)


def add_employee(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        emp_form = EmployeeForm(request.POST, request.FILES)

        if user_form.is_valid() and emp_form.is_valid():
            user = user_form.save()
            employee = emp_form.save(commit=False)
            employee.user = user
            employee.save()
            return redirect('employee_list')
    else:
        user_form = UserForm()
        emp_form = EmployeeForm()

    return render(request, 'employees/add_employee.html', {
        'user_form': user_form,
        'emp_form': emp_form
    })  




