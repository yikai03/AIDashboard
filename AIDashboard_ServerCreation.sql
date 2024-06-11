-- select @@servername 

CREATE DATABASE Sales_DB --run once
GO --run once

USE Sales_DB --run once

CREATE TABLE Categories(
CategoryID INT PRIMARY KEY NOT NULL,
Name NVARCHAR(100)
);

INSERT INTO Categories(CategoryID, Name)
VALUES
(1, 'Electronics'),
(2, 'Clothing'),
(3, 'Home & Kitchen'),
(4, 'Books'),
(5, 'Toys'),
(6, 'Sports & Outdoors'),
(7, 'Beauty & Personal Care'),
(8, 'Health & Household'),
(9, 'Automotive'),
(10, 'Grocery');

CREATE TABLE Customers(
CustomerID INT PRIMARY KEY,
Name NVARCHAR(100),
Email NVARCHAR(100)
);

INSERT INTO Customers(CustomerID, Name, Email)
VALUES
(1 , 'John Doe', 'john.doe@example.com'),
(2, 'Jane Smith', 'jane.smith@example.com'),
(3, 'Michael Johnson', 'michael.johnson@example.com'),
(4, 'Emily Brown', 'emily.brown@example.com'),
(5, 'David Wilson', 'david.wilson@example.com'),
(6, 'Sarah Martinez', 'sarah.martinez@example.com'),
(7, 'James Taylor', 'james.taylor@example.com'),
(8, 'Emma Anderson', 'emma.anderson@example.com'),
(9, 'Matthew Thomas', 'matthew.thomas@example.com'),
(10, 'Olivia Jackson', 'olivia.jackson@example.com');

CREATE TABLE Employees(
EmployeeID INT PRIMARY KEY,
Name NVARCHAR(100),
Position NVARCHAR(100)
);

INSERT INTO Employees(EmployeeID, Name, Position)
VALUES
(1, 'Catherine Rayford', 'Sales Associate'),
(2, 'James Hermes', 'Sales Manager'),
(3, 'Irene Will', 'Cashier'), 
(4, 'Patrick Gohem', 'Store Manager'),
(5, 'Qaviar William', 'Inventory Manager'),
(6, 'Obu Obu Obu', 'Customer Service Representative'),
(7, 'Bobby Lee', 'Marketing Coordinator'),
(8, 'Olajide Olatunji', 'Professional Seller'),
(9, 'Simon Brown', 'Entrepreur'),
(10, 'Josh Payne', 'Human Resource Manager');

CREATE TABLE Orders(
OrderID INT PRIMARY KEY,
CustomerID INT FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
OrderDate DATE, 
TotalAmount DECIMAL(10,2)
);

INSERT INTO Orders(OrderID, CustomerID, OrderDate, TotalAmount)
VALUES
(1, 1, '2024-05-01', 100.50),
(2, 1, '2024-05-03', 75.25),
(3, 2, '2024-05-02', 200.00),
(4, 3, '2024-05-01', 50.75),
(5, 4, '2024-05-04', 300.20),
(6, 5, '2024-05-03', 150.00), 
(7, 6, '2024-05-05', 80.50),
(8, 7, '2024-05-02', 90.75),
(9, 8, '2024-05-06', 120.25),
(10, 9, '2024-05-04', 175.00),
(11, 10, '2024-05-05', 250.50),
(12, 1, '2024-05-07', 60.75),
(13, 2, '2024-05-08', 180.25),
(14, 3, '2024-05-07', 110.50),
(15, 4, '2024-05-08', 90.25),
(16, 5, '2024-05-09', 300.00),
(17, 6, '2024-05-09', 150.75),
(18, 7, '2024-05-09', 75.00),
(19, 8, '2024-05-09', 200.50),
(20, 9, '2024-05-09', 125.25),
(21, 10, '2024-05-09', 95.50);

CREATE TABLE Products(
ProductID INT PRIMARY KEY,
Name NVARCHAR(100), 
Price DECIMAL(10,2)
);

INSERT INTO Products(ProductID, Name, Price)
VALUES
(1, 'Americano', 50.00),
(2, 'Latte', 75.00),
(3, 'Flat White', 100.00), 
(4, 'Expresso', 20.00), 
(5, 'Cappuccino', 120.00), 
(6, 'Frappe', 140.00), 
(7, 'Mocha', 80.00), 
(8, 'Caramel Latte', 90.00), 
(9, 'Matcha Green', 110.00), 
(10, 'Orange Juice', 40.00);

CREATE TABLE OrderDetails(
OrderDetailID INT PRIMARY KEY, 
OrderID INT FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
ProductID INT FOREIGN KEY (ProductID) REFERENCES Products(ProductID), 
Quantity INT, 
UnitPrice DECIMAL(10, 2)
);

INSERT INTO OrderDetails(OrderDetailID, OrderID, ProductID, Quantity, UnitPrice)
VALUES
(1, 1, 1, 2, 50.00),
(2, 2, 2, 4, 100.00),
(3, 3, 3, 3, 321.00),
(4, 4, 4, 4, 500.00), 
(5, 5, 5, 5, 900.00), 
(6, 6, 6, 6, 324.00), 
(7, 7, 7, 7, 90.00), 
(8, 8, 8, 1, 20.00), 
(9, 9, 9, 9, 1003.00), 
(10, 10, 10, 8, 800.00),
(11, 11, 1, 7, 350.00), 
(12, 12, 2, 3, 75.00), 
(13, 13, 3, 2, 214.00), 
(14, 14, 4, 1, 125.00), 
(15, 15, 5, 5, 900.00), 
(16, 16, 6, 3, 162.00), 
(17, 17, 7, 6, 83.00), 
(18, 18, 8, 3, 60.00), 
(19, 19, 9, 2, 200.10), 
(20, 20, 10, 7, 700.00), 
(21, 21, 1, 2, 50.00);

CREATE TABLE PaymentMethods(
PaymentMethodID INT PRIMARY KEY, 
Name NVARCHAR(100)
);

INSERT INTO PaymentMethods(PaymentMethodID, Name)
VALUES
(1, 'Credit Card'),
(2, 'Debit Card'), 
(3, 'Cash'), 
(4, 'Check');

CREATE TABLE Shipments(
ShipmentID INT PRIMARY KEY, 
OrderID INT FOREIGN KEY (OrderID) REFERENCES Orders(OrderID), 
ShipmentDate DATE, 
ShippingAddress NVARCHAR(255)
);

INSERT INTO Shipments(ShipmentID, OrderID, ShipmentDate, ShippingAddress)
VALUES
(1, 1, '2024-05-03', '123 Main St, City, Country'), 
(2, 2, '2024-05-04', '456 Elm St, City, Country'),
(3, 3, '2024-05-05', '789 Oak St, City, Country'),
(4, 4, '2024-05-06', '111 Pine St, City, Country'), 
(5, 5, '2024-05-07', '222 Jam St, City, Country'),
(6, 6, '2024-05-08', '333 Cedar St, City, Country'), 
(7, 7, '2024-05-09', '444 Walnut St, City, Country'),
(8, 8, '2024-05-10', '555 Birch St, City, Country'), 
(9, 9, '2024-05-11', '666 Spruce St, City, Country'), 
(10, 10, '2024-05-12', '777 Pine St, City, Country');

CREATE TABLE Locations(
LocationID INT PRIMARY KEY,
CountryName NVARCHAR(255)
);

INSERT INTO Locations(LocationID, CountryName)
VALUES
(1, 'Malaysia'),
(2, 'United Kingdom'),
(3, 'Japan'),
(4, 'United State'),
(5, 'South Korea'),
(6, 'China'),
(7, 'German'),
(8, 'Italy'),
(9, 'Australia'),
(10, 'Thailand')










