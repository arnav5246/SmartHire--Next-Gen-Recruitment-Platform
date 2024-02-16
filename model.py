import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess(JD):
  resume_data = pd.read_csv('data.csv')
  resume_data.replace('[]', ' ', inplace=True)
  resume_data = resume_data.drop_duplicates(subset='Name', keep='first',ignore_index=True)
  resume_data.fillna(' ', inplace=True)
  selected_features = ['Name','Skills','Work Experience','Projects','Certifications','Education' ]

  combined_features = resume_data['Name']+ ' ' +resume_data['Skills']+ ' ' +resume_data['Work Experience']+ ' ' +resume_data['Projects']+ ' ' +resume_data['Certifications']+ ' ' +resume_data['Education']
  vectorizer = TfidfVectorizer()
  num_elements = len(combined_features)
  combined_features[num_elements]=JD
  feature_vectors = vectorizer.fit_transform(combined_features)
  similarity = cosine_similarity(feature_vectors)

  similarity_score = list(enumerate(similarity[num_elements]))
  sorted_similar_resume = sorted(similarity_score, key= lambda x:x[1], reverse = True)

  output_string = 'Resumes suggested for you: \n\n'

  i = 1
  for movie in sorted_similar_resume:
    if movie[0] >= resume_data.shape[0]:
        continue
    index = movie[0]
    title_from_index = resume_data[resume_data.index == index]['Name'].values[0]
    if i < 30:
        output_string += f"{i} - {title_from_index} - {movie[1]}\n\n"
        i += 1

  return output_string

# if __name__=="__main__":
#     JD = "Job Title: Front-end Web Developer Skills Required: HTML CSS JavaScript PHP WordPress WooCommerce UI/UX design Graphic design REST API development Relational databases (e.g., MySQL) Agile and test-driven development best practices Eligibility Criteria: Bachelor's degree in computer science, web development, software development, or related field Web development fundamentals including HTML, CSS, and JavaScript Front-end JavaScript frameworks such as Vue, React, and Angular Back-end frameworks such as Ruby on Rails, Node.js, and ASP.NET Content management systems (CMSs) such as WordPress, Joomla, and Squarespace"
#     print(preprocess(JD))