from emp_app.models import Employee

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Define the expected data types for each key
employee_fields = {
    'name': str,
    'email': str,
    'age': int,
    'gender': str,
    'phoneNo': str,
    'addressDetails': dict,
    'workExperience': list,
    'qualifications': list,
    'projects': list
}


class EmployeeCreateAPIView(APIView):
    def post(self, request):
        employee_data = request.data

        # Check for duplicate email
        if Employee.objects.filter(email=employee_data['email']).exists():
            return Response({'error': 'Duplicate email'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for missing or incorrect data types
        for key, data_type in employee_fields.items():
            if key not in employee_data or not isinstance(employee_data[key], data_type):
                return Response({'error': f'Missing or incorrect data type for key: {key}'},
                                status=status.HTTP_400_BAD_REQUEST)

        # Check for missing keys in addressDetails
        address_details_keys = ['hno', 'street', 'city', 'state']
        if any(key not in employee_data['addressDetails'] for key in address_details_keys):
            return Response({'error': 'Missing key(s) in addressDetails'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for missing keys in workExperience
        work_experience_keys = ['companyName', 'fromDate', 'toDate', 'address']
        if any(
                any(key not in experience for key in work_experience_keys) for experience in
                employee_data['workExperience']
        ):
            return Response({'error': 'Missing key(s) in workExperience'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the employee
        employee = Employee.objects.create(**employee_data)

        return Response({'message': 'Employee created successfully'}, status=status.HTTP_201_CREATED)


class EmployeeUpdateAPIView(APIView):
    def put(self, request, regid):
        try:
            employee = Employee.objects.get(id=regid)
        except Employee.DoesNotExist:
            return Response({'message': 'No employee found with this regid', 'success': False},
                            status=status.HTTP_200_OK)

        employee_data = request.data

        # Check for missing or incorrect data types
        for key, data_type in employee_fields.items():
            if key not in employee_data or not isinstance(employee_data[key], data_type):
                return Response({'message': 'Invalid body request', 'success': False},
                                status=status.HTTP_400_BAD_REQUEST)

        # Update the employee
        try:
            for key, value in employee_data.items():
                setattr(employee, key, value)
            employee.save()
            return Response({'message': 'Employee details updated successfully', 'success': True},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Employee updation failed', 'success': False},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeDeleteAPIView(APIView):
    def delete(self, request):
        try:
            regid = request.data['regid']
            employee = Employee.objects.get(id=regid)
            employee.delete()
            return Response({'message': 'Employee deleted successfully', 'success': True}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({'message': 'Invalid body request', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({'message': 'No employee found with this regid', 'success': False},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Employee deletion failed', 'success': False},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeRetrieveAPIView(APIView):
    def get(self, request):
        regid = request.data.get('regid')

        if regid:
            try:
                employee = Employee.objects.get(id=regid)
                employee_data = {
                    'name': employee.name,
                    'age': employee.age,
                    'gender': employee.gender,
                    'phoneNo': employee.phoneNo,
                    'addressDetails': employee.addressDetails,
                    'workExperience': employee.workExperience,
                    'qualifications': employee.qualifications,
                    'projects': employee.projects,
                    'photo': employee.photo
                }
                return Response({'message': 'Employee details found', 'success': True, 'employees': [employee_data]},
                                status=status.HTTP_200_OK)
            except Employee.DoesNotExist:
                return Response({'message': 'Employee details not found', 'success': False, 'employees': []},
                                status=status.HTTP_200_OK)
        else:
            employees = Employee.objects.all()
            employee_list = []
            for employee in employees:
                employee_data = {
                    'name': employee.name,
                    'age': employee.age,
                    'gender': employee.gender,
                    'phoneNo': employee.phoneNo,
                    'addressDetails': employee.addressDetails,
                    'workExperience': employee.workExperience,
                    'qualifications': employee.qualifications,
                    'projects': employee.projects,
                    'photo': employee.photo
                }
                employee_list.append(employee_data)

            return Response({'message': 'Employee details found', 'success': True, 'employees': employee_list},
                            status=status.HTTP_200_OK)









