# Gradvisor
This is a part of the CSCE 670 (Information Storage and Retrieval) project.

Here is our introductory video: [Gradvisor](https://www.youtube.com/watch?v=rUaBuhE28ns)

Our Github repository: [Github](https://github.com/mohitsarin-tamu/Gradvisor)

---

## Summary
As graduate students, we all have been through a tough time selecting good universities based on our profile. We have to research several universities, check their cutoffs, acceptance rates etc. and gauge our profile against their requirements as we make limited applications because the application process is itself expensive. With the aim to reduce all this friction and make the application process easy, less expensive and more confident, Gradvisor provides university recommendations to the students. 

Any aspiring graduate student can sign-up and log-in to our website and fill out a nominal form with details such as CGPA, GRE score(Quantitative + Verbal), Research and Industrial experiences and publications. Based on these details an academic profile of the user is generated. This profile is matched against our database where we have a list of candidates with varied profiles and their respective admits. We then predict the top 5 universities for our current users. We also understand that as the next step, we are all eager to get some information about the first-hand experience of these universities where any aspirants apply to and the admission process as a whole. So we also recommend the top three most similar users based on the similarity score of the profiles of the aspirant/current user and the users in our database. We also provide a feature to connect with them over LinkedIn. (This functionality is added but as gathering LinkedIn profiles was difficult, we left an “Arriving Soon” message on our website when trying to contact the user). Also by connecting the users over Linkedin and not using any personal contacts, we ensure to maintain the privacy and safety of our users.

The implementation of this overall project involved a lot of challenges starting from getting the dataset to choosing the right model for implementation. The dataset was gathered by scraping similar websites. We had a total of 53 unique universities and then we added noise and performed oversampling and under-sampling to ensure that we have kind of enough information for our model to learn from for each university. We experimented with multiple machine learning models to make the top 5 university predictions including Random Forest, ANN and Adaboost. And as we had the best metrics for AdaBoost we finalised this. Also, we experimented with KNN and Pearson coefficient to calculate the closest/most similar users. As KNN was faster with better metrics, we implemented user-user collaborative filtering with KNN to recommend the most similar user profiles that can be contacted. 

Overall, with the motivation to make the process of choosing the universities and sending applications an easy, more informed and less tedious process we built this project.

---

## Model Information

### Similar Users Identification:
- Utilizing K-Nearest Neighbours (KNN) and Pearson Correlation Coefficient to calculate similarity scores of profiles. KNN is chosen for its effectiveness in finding similar user profiles. You can take a look at it [here](https://github.com/mohitsarin-tamu/Gradvisor/blob/main/User-User-K-nearest-neighbour.ipynb)

#### Prediction Process:
- Multiple machine learning algorithms were assessed for prediction, including Random Forest, AdaBoost, and Artificial Neural Networks. 

#### Final Recommendations:
- Applying the AdaBoost algorithm for university recommendation and utilizing KNN to identify similar user profiles. You can take a look at it [here](https://github.com/mohitsarin-tamu/Gradvisor/blob/main/AdaBoost.ipynb)

---

## Data Preprocessing: 

- You can download the dataset [here](https://github.com/mohitsarin-tamu/Gradvisor/blob/main/updated_preprocessed.csv).


- This preprocessed data contains information about several applicants who have applied to the 54 universities that we have considered. 

- Each row represents an individual applicant and includes various attributes such as their username, research experience, industry experience, internship experience, GRE scores (Verbal and Quantitative), publications in journals and conferences, CGPA, the name of the university they applied to, their admission status (admitted or not), and their GRE score. 

---

## Project Presentation

For a more detailed overview of the Gradvisor project, you can view our presentation slides [here](https://github.com/mohitsarin-tamu/Gradvisor/blob/main/Gradvisor.pptx).

---

## Structure of this repository:
1. **djangoApp/**: Contains the Django web application code for Gradvisor.

    - **gradvisorWebSite/**: Main Django project directory.
        - **settings.py**: Configuration settings for the Django project.
        - **urls.py**: URL configuration for the Django project.

    - **gradvisor/**: Main Django application directory.
        - **migrations/**: Database migration files.
        - **static/**: Static files (CSS, JavaScript, images).
        - **templates/**: HTML templates.
        - **admin.py, apps.py, models.py, views.py**: Django application components.
        - **forms.py**: Form definitions for user input.

2. **User-User-K-nearest-neighbour.ipynb**: Jupyter Notebook for K-Nearest Neighbors algorithm.

3. **AdaBoost.ipynb**: Jupyter Notebook for AdaBoost algorithm.

4. **updated_preprocessed.csv**: Preprocessed dataset.

5. **requirements.txt**: Python dependencies.

6. **Gradvisor.pptx**: PowerPoint presentation.

---

## Deploying this project locally:

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


## Gradvisor glimpses:

Home Page: 

![Home Page](Assets/Screenshot%202024-05-01%20at%2010.04.26.png)

Login/Signup:

![Login](Assets/Screenshot%202024-05-01%20at%2010.05.06.png)

Form:

![Form](Assets/Screenshot%202024-05-01%20at%2010.05.36.png)

Recommendation and Similar Users:

![Recommendation](Assets/Screenshot%202024-05-01%20at%2010.05.58.png)
