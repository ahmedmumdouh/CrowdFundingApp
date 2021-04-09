![forthebadge](https://forthebadge.com/images/badges/built-by-developers.svg)
![forthebadge](https://forthebadge.com/images/badges/uses-brains.svg)
![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)
![forthebadge](https://forthebadge.com/images/badges/powered-by-black-magic.svg)
![forthebadge](https://forthebadge.com/images/badges/makes-people-smile.svg)
#
# CrowdFundingApp
  
## Table Of Content

+ [About](#about)
+ [Getting Started](#getting_started)
+ [Project Structure](#project_structure)
+ [contributors](#contributors)
#
# About <a name = "about"></a>
A website developed in Django that allows you to have a fund for all your dream projects.
## website features:
 + Signup using Facebook
 + Create Project
 + Categorize Your Project
 + Add Images To Your Project
 + Add Tags To Your Project
 + Add Comments On the Projects
 + Report Inappropriate Projects
 + Report Inappropriate Comments
 + Rate the Projects
 + Donate to the total target Of Project
 + Search Projects By Title or Tags

#

 # Getting Started <a name = "getting_started"></a>

### Prerequisites

```
mysql
python
Django
```

### Installing
note: change the credentials in ```settings.py``` with your credentials

```
git clone https://github.com/ahmedmumdouh/CrowdFundingApp.git
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
#

# Project structure <a name = "project_structure"></a>

## Project components
### User Profile
+ User Can View His Profile
+ User Can View His Projects
+ User Can View His Donations
### Home Page
+ Highest Five Rated Running Projects
+ List of The Latest 5 Projects
+ List of Latest 5 Featured Projects
+ List of the Categories

### Projects​
+ User Can Create a Project
+ User Can View any Project
+ User Can Donate to The Total Target 
+ User can cancel the project if the donations are less than 25% of   
       the target
#
 # Contributors <a name = "contributors"></a>
 + [Abdelrahman Montser]
 + [Ahmed Mamdouh AbdelWahab](https://www.linkedin.com/in/ahmedmamdouh94/)	
 + [Eman Reda Soliman Ahmed](https://www.linkedin.com/mwlite/in/eman-soliman)
 + [Mohamed Mahmoud Kaoud](https://www.linkedin.com/in/mohamedkaoud)


