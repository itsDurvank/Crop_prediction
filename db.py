import sqlite3 as sql
import pandas as pd  
from datetime import date


class CropDatabase:
    def __init__(self, db_path="crop_prediction.db"):
        self.db_path = db_path
        self.initialize()
    def initialize(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS soil_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nitrogen REAL,
            phosphorus REAL,
            potassium REAL,
            ph REAL,
            temperature REAL,
            humidity REAL,
            rainfall REAL,
            recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
            ''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS crop_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            soil_data_id INTEGER,
            predicted_crop TEXT,
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (soil_data_id) REFERENCES soil_data (id))
            ''')
        conn.commit()
        conn.close()

        
        
    def get_connection(self):
        return sql.connect(self.db_path)
    
    def add_data(self,nitrogen,phosphorus,potassium,ph,temperature,humidity ,rainfall):
        conn = self.get_connection()
        cursor = conn.cursor()
        conn.execute('''
                    INSERT INTO soil_data 
        (nitrogen, phosphorus, potassium, ph, temperature, humidity, rainfall)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',(nitrogen, phosphorus, potassium, ph, temperature, humidity, rainfall))
        soil_data_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return soil_data_id
    
    def add_prediction(self, soil_data_id, predicted_crop):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO crop_predictions 
        (soil_data_id, predicted_crop)
        VALUES (?, ?)
        ''', (soil_data_id, predicted_crop))
        
        conn.commit()
        conn.close()
    def get_historical_data(self, limit=100):
        conn = self.get_connection()
        
        query = '''
        SELECT s.id, s.nitrogen, s.phosphorus, s.potassium, s.ph, s.temperature, s.humidity, s.rainfall, 
        s.recorded_date, p.predicted_crop FROM soil_data s LEFT JOIN crop_predictions p ON s.id = p.soil_data_id
        ORDER BY s.recorded_date DESC
        LIMIT ?
        '''
        
        df = pd.read_sql_query(query, conn, params=(limit,))
        conn.close()
        
        return df    