from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import os

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for the classification section
@app.route('/classification')
def classification():
    return render_template('classification.html')

# Route for house rent prediction
@app.route('/house_rent_prediction', methods=['GET', 'POST'])
def house_rent_prediction():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            # Save the uploaded file
            filepath = os.path.join('uploads', file.filename)
            file.save(filepath)
            
            # Read the CSV file
            data = pd.read_csv(filepath)
            
            # Preprocess data
            data['Total_Floors'] = data['Floor'].apply(lambda x: int(x.split(' out of ')[1]) if 'out of' in str(x) else 0)
            data['Floor'] = data['Floor'].apply(lambda x: int(x.split(' out of ')[0].replace('Ground', '0')) if 'out of' in str(x) else 0)
            
            # Drop non-useful columns
            data = data.drop(columns=['Point of Contact', 'Area Locality'])
            
            # One-hot encode categorical variables
            categorical_cols = ['Area Type', 'City', 'Furnishing Status', 'Tenant Preferred']
            data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)
            
            # Handle missing values
            data = data.fillna(data.median())
            
            # Features and target
            X = data.drop(columns=['Rent'])
            y = data['Rent']
            
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train a simple model
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            # Make predictions
            predictions = model.predict(X_test)
            
            # Calculate the difference between predictions and actual values
            results = pd.DataFrame({
                'Actual': y_test,
                'Predicted': predictions
            })
            
            # Highlight cells where predictions are close to actual values
            results['Difference'] = abs(results['Actual'] - results['Predicted'])
            results_html = results.style.applymap(lambda x: 'background-color: lightgreen' if x < 500 else '').to_html()
            
            return render_template('house_rent_prediction.html', tables=[results_html])
    
    return render_template('house_rent_prediction.html')


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
