# drchrono Check-in Kiosk
## Description
Picture going to the doctor's office and replacing the receptionist and paper forms with a kiosk similar to checking in for a flight.

This project brings up the following benefits:
- All doctors can install this application on their drchrono account.
- Doctors can lock the device to the patient mode when patients check-in.
- Provides average waiting time and real-time patient waiting time for doctors.
- All actions on patients and appointments are directly reflected on drchrono account.


### Requirements
- [pip](https://pip.pypa.io/en/stable/)
- [python virtual env](https://packaging.python.org/installing/#creating-and-using-virtual-environments)

### Setup
``` bash
$ pip install -r requirements.txt
$ python manage.py runserver
```
## Screenshots of the system


#### Doctor
home page: can lock device to patient check-in mode.
![doctor_home](https://github.com/xujingyapatrick/drchrono_check_in_kiosk/blob/master/readme_figures/doctor_mode/home.PNG)  

appointment page: before sync.
![appointment](https://github.com/xujingyapatrick/drchrono_check_in_kiosk/blob/master/readme_figures/doctor_mode/appointments.PNG) 
appointment page: after sync. Different color cards stands for status in: `before arrive`, `arrived`, `in session`, `complete` 
![appointment](https://github.com/xujingyapatrick/drchrono_check_in_kiosk/blob/master/readme_figures/doctor_mode/appointments_working.PNG) 

oauth page:do  `authenticate`or `refresh auth token`.
![oauth](https://github.com/xujingyapatrick/drchrono_check_in_kiosk/blob/master/readme_figures/doctor_mode/oauth.PNG)

#### Patient
check-in page: patient check-in.
![patients_check-in](https://github.com/xujingyapatrick/drchrono_check_in_kiosk/blob/master/readme_figures/patient_mode/checkin.PNG)  
demographic information page: use this form to update patient information or skip updating.
![patients_demographic information](https://github.com/xujingyapatrick/drchrono_check_in_kiosk/blob/master/readme_figures/patient_mode/information.PNG)  
![patients_demographic information__1](https://github.com/xujingyapatrick/drchrono_check_in_kiosk/blob/master/readme_figures/doctor_mode/information_1.PNG)  
exit page: exit patient mode.
![patients_exit](https://github.com/xujingyapatrick/drchrono_check_in_kiosk/blob/master/readme_figures/patient_mode/exit.PNG)  

#### Register and login
register page: will do oauth on registration.
![register](https://github.com/xujingyapatrick/drchrono_check_in_kiosk/blob/master/readme_figures/reg_login/register.PNG)  

login page:
![login](https://github.com/xujingyapatrick/drchrono_check_in_kiosk/blob/master/readme_figures/reg_login/login.PNG)



