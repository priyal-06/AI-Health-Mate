from flask import Flask, request, render_template, jsonify  # Import jsonify
import numpy as np
import pandas as pd
import pickle
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import csv


# flask app
app = Flask(__name__)
app.secret_key = 'Ayush_Gupta'
# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="6124priy@l",  
        database="aihealthmate"   
    )





def load_unique_symptoms():
    # Load the CSV file
    file_path = 'datasets/symtoms.csv'
    df = pd.read_csv(file_path)

    # Combine all symptom columns and extract unique values
    symptom_columns = ['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4']
    
    # Concatenate symptom columns, drop nulls, strip spaces, and get unique symptoms
    all_symptoms = pd.concat([df[col] for col in symptom_columns]).dropna().apply(lambda x: x.strip()).unique()

    # Sort the unique symptoms alphabetically
    unique_symptoms = sorted(all_symptoms)
    
    return unique_symptoms



# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Establish connection to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Query the database for the user
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        # Close the connection
        cursor.close()
        conn.close()

        # Check if user exists and password is correct
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('logging.html')

# Route for registration page
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Establish connection to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already exists', 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for('register'))

        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                       (username, email, hashed_password))
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# load databasedataset===================================
sym_des = pd.read_csv("datasets/symtoms.csv")
precautions = pd.read_csv("datasets/precautions_df2.csv")
medications = pd.read_csv('datasets/medications.csv')


# load model===========================================
svc = pickle.load(open('models/svc.pkl','rb'))


#============================================================
# custome and helping functions
#==========================helper funtions================
def helper(dis):
    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    return pre,med

symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 41: 'viral fever', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}

# Model Prediction function
def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        input_vector[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([input_vector])[0]]




# creating routes========================================


# Home route
@app.route('/')
def index():
    if 'username' in session:
        unique_symptoms = load_unique_symptoms()  # Load the symptoms when rendering the form
        print(unique_symptoms)
        return render_template('index.html', username=session['username'],symptoms=unique_symptoms)
    else:
        return redirect(url_for('login'))



@app.route('/predict', methods=['GET', 'POST'])
def home():
    
    if request.method == 'POST':
        # Get the symptoms from the form
        symptom1 = request.form.get('symptom1')
        symptom2 = request.form.get('symptom2')
        symptom3 = request.form.get('symptom3')
        symptom4 = request.form.get('symptom4')
        symptom5 = request.form.get('symptom5')

        # Combine the symptoms into a list
        user_symptoms = [symptom1, symptom2, symptom3, symptom4, symptom5]

        if not all(user_symptoms):
            message = "Please select all the symptoms."
            return render_template('index.html', message=message)

        predicted_disease = get_predicted_value(user_symptoms)
        precautions, medications= helper(predicted_disease)

        my_precautions = [str(i) for i in precautions[0]]  # Ensure all items are strings
        medications = [str(med) for med in medications]  # Ensure all items are strings

        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO history (username, predicted_disease, precautions, medications, prediction_date ) 
            VALUES (%s, %s, %s, %s, NOW())
        """, (session['username'], predicted_disease, ', '.join(my_precautions), ', '.join(medications)))
        conn.commit()
        cursor.close()
        conn.close()
        unique_symptoms = load_unique_symptoms()
        return render_template('index.html', predicted_disease=predicted_disease,
                               my_precautions=my_precautions, medications=medications,symptoms=unique_symptoms)

    




@app.route('/history')
def history():
    if 'username' in session:
        username = session['username']
        
        # Establish connection to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch the prediction history for the logged-in user
        cursor.execute("SELECT * FROM history WHERE username = %s ORDER BY prediction_date DESC", (username,))
        history = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('history.html', history=history)
    else:
        flash('You need to log in to view your history.', 'danger')
        return redirect(url_for('login'))






if __name__ == '__main__':

    app.run(debug=True)