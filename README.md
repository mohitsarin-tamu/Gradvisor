# Gradvisor
This is a part of the CSCE 670 (Information Storage and Retrieval) project.

##### Motivation
- Choosing the right university is a significant decision that can have a profound impact on a student's academic and professional future. 

- With Gradvisor, students have access to comprehensive tools and resources that empower them to make informed decisions aligned with their academic profile, career goals, and personal preferences. 

- Create meaningful connections with like-minded people to improve your interactions and enrich your experiences.

##### Model Information

###### Similar Users Identification:
- Utilizing K-Nearest Neighbours (KNN) and Pearson Correlation Coefficient to calculate similarity scores of profiles. KNN is chosen for its effectiveness in finding similar user profiles. You can take a look at it [here](https://github.com/mohitsarin-tamu/Gradvisor/blob/main/User-User-K-nearest-neighbour.ipynb)

###### Prediction Process:
- Multiple machine learning algorithms were assessed for prediction, including Random Forest, AdaBoost, and Artificial Neural Networks. 

###### Final Recommendations:
- Applying the AdaBoost algorithm for university recommendation and utilizing KNN to identify similar user profiles. You can take a look at it [here](https://github.com/mohitsarin-tamu/Gradvisor/blob/main/AdaBoost.ipynb)

##### Data Preprocessing: 

- You can download the dataset [here](https://github.com/mohitsarin-tamu/Gradvisor/blob/main/updated_preprocessed.csv).


- This preprocessed data contains information about several applicants who have applied to the 54 universities that we have considered. 

- Each row represents an individual applicant and includes various attributes such as their username, research experience, industry experience, internship experience, GRE scores (Verbal and Quantitative), publications in journals and conferences, CGPA, the name of the university they applied to, their admission status (admitted or not), and their GRE score. 

##### Deploying this project locally:

Clone the Repository: Open a terminal or command prompt and use the git clone command to clone the repository to your local machine. 

```sh
git clone https://github.com/mohitsarin-tamu/Gradvisor.git
```
Navigate to the Project Directory: Use the cd command to navigate into the directory of the cloned repository:

```sh
cd Gradvisor
```

Install Dependencies
```sh
pip install -r requirements.txt
```

Navigate to the djangoApp directory
```sh
cd djangoApp
```

Now to run the server locally: 
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

The server usually runs on this url: http://127.0.0.1:8000 