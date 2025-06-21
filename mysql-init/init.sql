CREATE DATABASE IF NOT EXISTS ragdb;
USE ragdb;

CREATE TABLE IF NOT EXISTS customers (
  customerID VARCHAR(50) PRIMARY KEY,
  gender VARCHAR(10),
  SeniorCitizen TINYINT(1),             -- 0 or 1
  Partner VARCHAR(3),                   -- 'Yes' or 'No'
  Dependents VARCHAR(3),                -- 'Yes' or 'No'
  tenure INT,
  PhoneService VARCHAR(3),
  MultipleLines VARCHAR(20),
  InternetService VARCHAR(20),
  OnlineSecurity VARCHAR(20),
  OnlineBackup VARCHAR(20),
  DeviceProtection VARCHAR(20),
  TechSupport VARCHAR(20),
  StreamingTV VARCHAR(20),
  StreamingMovies VARCHAR(20),
  Contract VARCHAR(20),
  PaperlessBilling VARCHAR(3),
  PaymentMethod VARCHAR(50),
  MonthlyCharges DECIMAL(10,2),
  TotalCharges DECIMAL(10,2),
  Churn VARCHAR(3)                      -- 'Yes' or 'No'
);