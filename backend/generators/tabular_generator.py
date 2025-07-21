import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from config import Config

class TabularDataGenerator:
    """Generator class for creating synthetic tabular data using trained models"""
    
    def __init__(self):
        """Initialize the generator with model paths"""
        self.models_dir = Config.MODELS_DIR
        print(f"TabularDataGenerator: models_dir = {self.models_dir}")
        print(f"TabularDataGenerator: models_dir exists = {self.models_dir.exists()}")
        print(f"TabularDataGenerator: models_dir is_dir = {self.models_dir.is_dir()}")
        
        if self.models_dir.exists():
            print(f"TabularDataGenerator: models_dir contents = {list(self.models_dir.iterdir())}")
        
        self.available_models = self._get_available_models()
        print(f"TabularDataGenerator: available_models = {self.available_models}")
    
    def _get_available_models(self) -> List[str]:
        """Get list of available trained models"""
        print(f"_get_available_models: checking {self.models_dir}")
        if not self.models_dir.exists():
            print(f"_get_available_models: models_dir does not exist")
            return []
        
        models = []
        for model_dir in self.models_dir.iterdir():
            print(f"_get_available_models: checking {model_dir}")
            if model_dir.is_dir():
                # Check for both naming conventions
                model_file1 = model_dir / "model.pkl"
                model_file2 = model_dir / f"{model_dir.name.lower()}_model.pkl"
                print(f"_get_available_models: model.pkl exists = {model_file1.exists()}")
                print(f"_get_available_models: {model_dir.name.lower()}_model.pkl exists = {model_file2.exists()}")
                
                if model_file1.exists() or model_file2.exists():
                    models.append(model_dir.name)
        
        print(f"_get_available_models: found models = {models}")
        return models
    
    def get_available_domains(self) -> List[str]:
        """Get list of available domains for data generation"""
        return [model.lower() for model in self.available_models]
    
    def _get_model_directory(self, domain: str) -> str:
        """Get the actual model directory name (handling case sensitivity)"""
        domain_lower = domain.lower()
        for model_dir in self.models_dir.iterdir():
            if model_dir.is_dir() and model_dir.name.lower() == domain_lower:
                return model_dir.name
        return None
    
    def generate_tabular_data(self, domain: str, num_samples: int, 
                             topic: str = None, custom_fields: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate synthetic tabular data for a specific domain"""
        available_domains = self.get_available_domains()
        if domain not in available_domains:
            raise ValueError(f"Domain '{domain}' not available. Available domains: {available_domains}")
        
        if num_samples > Config.MAX_NUM_SAMPLES:
            raise ValueError(f"Maximum number of samples allowed is {Config.MAX_NUM_SAMPLES}")
        
        try:
            print(f"Generating {num_samples} samples for domain: {domain}")
            
            # Get the actual model directory name
            model_dir_name = self._get_model_directory(domain)
            if model_dir_name:
                print(f"Found model directory: {model_dir_name}")
                # Check for model files
                model_path1 = self.models_dir / model_dir_name / "model.pkl"
                model_path2 = self.models_dir / model_dir_name / f"{model_dir_name.lower()}_model.pkl"
                
                if model_path1.exists():
                    print(f"Found model file: {model_path1}")
                elif model_path2.exists():
                    print(f"Found model file: {model_path2}")
                else:
                    print("No model file found, using placeholder generation")
            
            # Skip model loading for now and just generate placeholder data
            # This avoids potential hanging on model file access
            synthetic_data = self._generate_placeholder_data(domain, num_samples, topic, custom_fields)
            
            print(f"Generated {len(synthetic_data)} records successfully")
            
            return {
                'domain': domain,
                'topic': topic,
                'data': synthetic_data,
                'num_samples': num_samples,
                'generated_at': datetime.now().isoformat(),
                'model_type': 'placeholder'
            }
            
        except Exception as e:
            print(f"Error in generate_tabular_data: {str(e)}")
            raise Exception(f"Error generating tabular data: {str(e)}")
    
    def _generate_placeholder_data(self, domain: str, num_samples: int, 
                                 topic: str = None, custom_fields: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate placeholder data based on domain (replace with actual model inference)"""
        
        if domain == "ecommerce":
            return self._generate_ecommerce_data(num_samples, topic, custom_fields)
        elif domain == "education":
            return self._generate_education_data(num_samples, topic, custom_fields)
        elif domain == "finance":
            return self._generate_finance_data(num_samples, topic, custom_fields)
        elif domain == "medical":
            return self._generate_medical_data(num_samples, topic, custom_fields)
        else:
            return self._generate_generic_data(domain, num_samples, topic, custom_fields)
    
    def _generate_ecommerce_data(self, num_samples: int, topic: str = None, 
                               custom_fields: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate synthetic ecommerce data"""
        data = []
        
        products = ["Laptop", "Smartphone", "Headphones", "Tablet", "Camera", "Watch", "Speaker", "Keyboard"]
        categories = ["Electronics", "Computers", "Mobile", "Accessories", "Gaming"]
        payment_methods = ["Credit Card", "PayPal", "Bank Transfer", "Cash on Delivery"]
        
        for i in range(num_samples):
            product = np.random.choice(products)
            category = np.random.choice(categories)
            price = round(np.random.uniform(50, 2000), 2)
            quantity = np.random.randint(1, 10)
            
            record = {
                'order_id': f"ORD-{datetime.now().strftime('%Y%m%d')}-{i+1:04d}",
                'customer_id': f"CUST-{np.random.randint(1000, 9999)}",
                'product_name': product,
                'category': category,
                'price': price,
                'quantity': quantity,
                'total_amount': round(price * quantity, 2),
                'payment_method': np.random.choice(payment_methods),
                'order_date': (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d'),
                'shipping_address': f"Address {np.random.randint(1, 1000)}",
                'order_status': np.random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled'])
            }
            
            if custom_fields:
                record.update(custom_fields)
            
            data.append(record)
        
        return data
    
    def _generate_education_data(self, num_samples: int, topic: str = None, 
                               custom_fields: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate synthetic education data"""
        data = []
        
        subjects = ["Mathematics", "Science", "English", "History", "Geography", "Art", "Music", "Physical Education"]
        grades = ["A", "B", "C", "D", "F"]
        attendance_percentages = list(range(60, 101))
        
        for i in range(num_samples):
            subject = np.random.choice(subjects)
            grade = np.random.choice(grades)
            attendance = np.random.choice(attendance_percentages)
            score = np.random.randint(0, 101)
            
            record = {
                'student_id': f"STU-{np.random.randint(1000, 9999)}",
                'student_name': f"Student {i+1}",
                'subject': subject,
                'grade': grade,
                'score': score,
                'attendance_percentage': attendance,
                'semester': np.random.choice(['Fall', 'Spring', 'Summer']),
                'year': np.random.randint(2020, 2025),
                'teacher_id': f"TCH-{np.random.randint(100, 999)}",
                'class_size': np.random.randint(15, 35)
            }
            
            if custom_fields:
                record.update(custom_fields)
            
            data.append(record)
        
        return data
    
    def _generate_finance_data(self, num_samples: int, topic: str = None, 
                             custom_fields: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate synthetic finance data"""
        data = []
        
        transaction_types = ["Deposit", "Withdrawal", "Transfer", "Payment", "Investment"]
        account_types = ["Savings", "Checking", "Investment", "Credit"]
        
        for i in range(num_samples):
            transaction_type = np.random.choice(transaction_types)
            amount = round(np.random.uniform(10, 10000), 2)
            account_type = np.random.choice(account_types)
            
            record = {
                'transaction_id': f"TXN-{datetime.now().strftime('%Y%m%d')}-{i+1:04d}",
                'account_id': f"ACC-{np.random.randint(10000, 99999)}",
                'account_type': account_type,
                'transaction_type': transaction_type,
                'amount': amount,
                'balance': round(np.random.uniform(1000, 50000), 2),
                'transaction_date': (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d'),
                'merchant': f"Merchant {np.random.randint(1, 100)}",
                'location': f"City {np.random.randint(1, 50)}",
                'status': np.random.choice(['Completed', 'Pending', 'Failed'])
            }
            
            if custom_fields:
                record.update(custom_fields)
            
            data.append(record)
        
        return data
    
    def _generate_medical_data(self, num_samples: int, topic: str = None, 
                             custom_fields: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate synthetic medical data"""
        data = []
        
        conditions = ["Hypertension", "Diabetes", "Asthma", "Arthritis", "Heart Disease", "Depression"]
        medications = ["Aspirin", "Ibuprofen", "Metformin", "Lisinopril", "Atorvastatin", "Omeprazole"]
        
        for i in range(num_samples):
            condition = np.random.choice(conditions)
            medication = np.random.choice(medications)
            age = np.random.randint(18, 85)
            weight = round(np.random.uniform(50, 120), 1)
            height = round(np.random.uniform(150, 200), 1)
            
            record = {
                'patient_id': f"PAT-{np.random.randint(10000, 99999)}",
                'patient_name': f"Patient {i+1}",
                'age': age,
                'gender': np.random.choice(['Male', 'Female']),
                'weight_kg': weight,
                'height_cm': height,
                'bmi': round(weight / ((height/100) ** 2), 1),
                'condition': condition,
                'medication': medication,
                'visit_date': (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d'),
                'doctor_id': f"DOC-{np.random.randint(100, 999)}",
                'blood_pressure': f"{np.random.randint(110, 140)}/{np.random.randint(70, 90)}"
            }
            
            if custom_fields:
                record.update(custom_fields)
            
            data.append(record)
        
        return data
    
    def _generate_generic_data(self, domain: str, num_samples: int, topic: str = None, 
                             custom_fields: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate generic synthetic data for unknown domains"""
        data = []
        
        for i in range(num_samples):
            record = {
                'id': f"{domain.upper()}-{i+1:04d}",
                'name': f"{domain.title()} Item {i+1}",
                'value': round(np.random.uniform(1, 1000), 2),
                'category': f"Category {np.random.randint(1, 10)}",
                'status': np.random.choice(['Active', 'Inactive', 'Pending']),
                'created_date': (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d'),
                'description': f"Description for {domain} item {i+1}"
            }
            
            if custom_fields:
                record.update(custom_fields)
            
            data.append(record)
        
        return data
    
    def save_to_file(self, data: List[Dict[str, Any]], filename: str, 
                    format: str = "json", user_id: str = None) -> str:
        """Save generated data to file"""
        try:
            print(f"Saving {len(data)} records to file with format: {format}")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename}_{timestamp}.{format}"
            
            if user_id:
                user_dir = Config.TABULAR_DATA_DIR / user_id
                user_dir.mkdir(exist_ok=True, parents=True)
                filepath = user_dir / filename
            else:
                filepath = Config.TABULAR_DATA_DIR / filename
            
            print(f"File will be saved to: {filepath}")
            
            if format == "json":
                print("Saving as JSON...")
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            elif format == "csv":
                print("Saving as CSV...")
                df = pd.DataFrame(data)
                df.to_csv(filepath, index=False, encoding='utf-8')
            else:
                raise ValueError("Format must be 'json' or 'csv'")
            
            print(f"File saved successfully to: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"Error in save_to_file: {str(e)}")
            raise e 