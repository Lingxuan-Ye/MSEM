# Homework 2

## Part 1

### 1

Columns.

### 2

- Each column in a row must be atomic. In other words, the column can contain only one value for any given row.

- Each row in a table must contain the same number of columns. Given that each column can contain only one value, this means that each row must contain the same number of values.

- All rows in a table must be different. Although rows might include the same values, each row, when taken as a whole, must be unique in the table.

### 3

In an one-to-many relationship, a row in the second table cannot be related to one or more rows in the first table, while it can be in a many-to-many relationship.

### 4

Normalizing the data.

### 5

When you add a junction table, the many-to-many relationship is implemented as two one-to-many relationships.

## Part 2

### 1

The current structure of the database is not normalized and can be improved by breaking it down into multiple tables to remove redundant and repeating data.

Table: Book

| Column Name   | Data Type |
| ------------- | --------- |
| BookId        | int       |
| BookTitle     | varchar   |
| ISBN          | varchar   |
| YearPublished | int       |
| PublisherId   | int       |
| BookSellerId  | int       |

Table: Author

| Column Name   | Data Type |
| ------------- | --------- |
| AuthorId      | int       |
| AuthorName    | varchar   |
| AuthorAddress | varchar   |

Table: Publisher

| Column Name      | Data Type |
| ---------------- | --------- |
| PublisherId      | int       |
| PublisherName    | varchar   |
| PublisherAddress | varchar   |

Table: BookAuthor

| Column Name | Data Type |
| ----------- | --------- |
| BookId      | int       |
| AuthorId    | int       |

Table: BookSeller

| Column Name     | Data Type |
| --------------- | --------- |
| BookSellerId    | int       |
| BookSellerName  | varchar   |
| BookSellerTelNo | varchar   |

### 2

```sql
ALTER TABLE FavCategory
ADD FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
ADD FOREIGN KEY (MemberId) REFERENCES MemberDetails(MemberId);
```

## Part 3

### 1

This stipulates that a salesperson's compensation can only be either a salary greater than zero and no commission, or a commission greater than zero and no salary.

### 2

Attribute -- Column -- Field
Relation -- Foreign Key -- File
Foreign Key -- Table -- Relationship
Tuple -- Row -- Record
View -- Query Result -- Virtual Table

### 3

Yes. Each state has a unique abbreviation and title, so this combination of columns is guaranteed to be unique.

### 4

No. Not unique.

### 5

State and Abbr.

### 6

State: string
Abbr: string
Title: string
Engraver: string
Year: integer
Got: boolean

### 7

(Room, Phone, CellPhone)

### 8

(Room, FirstName, LastName)

### 9

FirstName and LastName cannot have numeric characters.

### 10

Phone and CellPhone cannot both be Null for a given room.

## Part 4

### Review

#### 1

a. determinant: the attribute on the left side of the arrow in a functional dependency.

b. functional dependency: a constraint between two attributes in which the value of one attribute is determined by the value of another attribute.

c. transitive dependency: a functional dependency between the primary key and one or more nonkey attributes that are dependent on the primary key via another nonkey attribute.

d. recursive foreign key: a foreign key in a relation that references the primary key values of the same relation.

e. normalization: the process of decomposing relations with anomalies to produce smaller, well-structured relations.

f. composite key: a primary key that consists of more than one attribute.

g. relation: A named two-dimensional table of data.

h. normal form: a state of a relation that requires that certain rules regarding relationships between attributes (or functional dependencies) are satisfied.

i. partial functional dependency: a functional dependency in which one or more nonkey attributes are functionally dependent on part (but not all) of the primary key.

j. enterprise key: A primary key whose value is unique across all relations.

k. surrogate primary key: a serial number or other system-assigned primary key for a relation.

#### 2

Match the following terms to the appropriate definitions:

f. well-structuredrelation
e. anomaly
a. functional dependency
j. determinant
g. composite key
d. 1NF
h. 2NF
i. 3NF
c. recursive foreign key
k. relation
b. transitive dependency

#### 3

a. Normal form refers to the degree of freedom from redundancy and modification anomalies, while normalization is the process of achieving it.

b. A candidate key uniquely identifies each row, while a primary key is a chosen candidate key used for identification.

c. Partial dependency occurs when a nonkey attribute is dependent on only a part of a primary key, while a transitive dependency occurs when a nonkey attribute is dependent on another nonkey attribute via the primary key.

d. A composite key is a primary key made up of multiple attributes, while a recursive foreign key is a foreign key that references the primary key of the same table.

e. A determinant determines the value of another attribute, while a candidate key uniquely identifies each row.

f. A foreign key refers to a primary key of another table, while a primary key is a chosen candidate key for identification.

g. An enterprise key is a meaningful unique identifier, while a surrogate key is a unique identifier generated solely for identification.

#### 8

a. 2nd

b. 3rd

c. 1st

#### 14

1. the relation is in 1NF;

2. every non-key attribute is fully functionally dependent on the primary key;

3. there are no transitive dependencies.

### Exercise

#### 3

a. in 2NF and 3NF.

b. in 2NF, but not in 3NF.

    Decompose:

    - CLASS(CourseNo, SectionNo, Room)

    - RoomCapacity(Room, Capacity)

c. in 2NF, but not in 3NF.

    Decompose:

    - CLASS(CourseNo, SectionNo, Room)

    - RoomCapacity(Room, Capacity)

d. not in 3NF.

    Decompose:

    - CLASS(CourseNo, SectionNo, CourseName, Room)

    - Room(Room, Capacity)

    - Course(CourseNo, CourseName)

#### 5

- Course (CourseKey, CourseNo, CourseTitle)

- Instructor (InstructorKey, InstructorName, InstructorLocation)

- Student (StudentKey, StudentNo, StudentName, Major)

- Enrollment (EnrollmentKey, StudentKey, CourseKey, Grade)

#### 6.c

...

#### 7.f

PARTS table:

| Part No | Description |
| ------- | ----------- |
| 1234    | Logic chip  |
| 5678    | Memory chip |

VENDORS table:

| Vendor Name   | Address   |
| ------------- | --------- |
| Fast Chips    | Cupertino |
| Smart Chips   | Phoenix   |
| Quality Chips | Austin    |

SUPPLY table:

| Part No | Vendor Name   | Unit Cost |
| ------- | ------------- | --------- |
| 1234    | Fast Chips    | 10.00     |
| 1234    | Smart Chips   | 8.00      |
| 5678    | Fast Chips    | 3.00      |
| 5678    | Quality Chips | 2.00      |
| 5678    | Smart Chips   | 5.00      |

#### 8.d

STUDENTS table:

- StudentID (PK)

- StudentName

- CampusAddress

- Major

COURSES table:

- CourseID (PK)

- CourseTitle

INSTRUCTORS table:

- InstructorName (PK)

- InstructorLocation

GRADES table:

- GradeID (PK)

- StudentID (FK)

- CourseID (FK)

- InstructorName (FK)

- Grade

The referential integrity constraints are as follows:

- The StudentID in the GRADES table references the StudentID in the STUDENTS table.

- The CourseID in the GRADES table references the CourseID in the COURSES table.

- The InstructorName in the GRADES table references the InstructorName in the INSTRUCTORS table.

#### 9.d

SHIPMENTS table:

- ShipmentID (PK)
- ShipmentDate
- Origin
- ExpectedArrival
- Destination
- ShipNumber (FK)
- Captain

SHIPPING_ITEMS table:

- ItemNumber (PK)
- Type
- Description
- Weight
- Quantity
- ShipmentID (FK)

The referential integrity constraints:

- The ShipNumber in the SHIPMENTS table references the primary key of the SHIPS table.
- The ShipmentID in the SHIPPING_ITEMS table references the ShipmentID in the SHIPMENTS table.

#### 21

##### a

Functional Dependencies:

- StoreName -> PetName, Pet Description, Price, Cost, SupplierName, ShippingTime

- SupplierName -> Cost, ShippingTime

- PetName -> Pet Description, Price, Cost

##### b

1NF

##### c

STORES table:

- StoreID (PK)
- StoreName

PETS table:

- PetID (PK)
- PetName
- PetDescription
- Price
- Cost
- SupplierID (FK)

SUPPLIERS table:

- SupplierID (PK)
- SupplierName
- ShippingTime

INVENTORY table:

- InventoryID (PK)
- PetID (FK)
- StoreID (FK)
- QuantityOnHand
- DateOfLastDelivery
- DateOfLastPurchase

DELIVERY_DATES table:

- DeliveryDateID (PK)
- InventoryID (FK)
- DeliveryDate

PURCHASE_DATES table:

- PurchaseDateID (PK)
- InventoryID (FK)
- PurchaseDate

CUSTOMERS table:

- CustomerID (PK)
- CustomerName

PURCHASES table:

- PurchaseID (PK)
- InventoryID (FK)
- CustomerID (FK)
- PurchaseDateID (FK)

referential integrity constraints:

- The SupplierID in the PETS table references the SupplierID in the SUPPLIERS table.
- The PetID in the INVENTORY table references the PetID in the PETS table.
- The StoreID in the INVENTORY table references the StoreID in the STORES table.
- The InventoryID in the DELIVERY_DATES and PURCHASE_DATES tables references the InventoryID in the INVENTORY table.
- The CustomerID in the PURCHASES table references the CustomerID in the CUSTOMERS table.
- The PurchaseDateID in the PURCHASES table references the PurchaseDateID in the PURCHASE_DATES table.

#### 25

##### a

Functional Dependencies:

- ComputerSerialNbr -> VendorID, PurchasePrice
- VendorID -> VendorName, VendorPhone, VendorSupportID
- VendorSupportID -> VendorSupportName, VendorSupportExtension
- SoftwareID -> SoftwareName, SoftwareVendor, SoftwareLicenceExpires, SoftwareLicencePrice
- UserID -> UserName
- (ComputerSerialNbr, SoftwareID, UserID) -> UserAuthorizationStarts, UserAuthorizationEnds, UserAuthorizationPassword

##### b

not in 3NF because of the SoftwareID and UserID attributes are not part of any candidate key, but they are dependent on the ComputerSerialNbr attribute.

##### c

COMPUTERS table:

- ComputerSerialNbr (PK)
- VendorID (FK)
- PurchasePrice

VENDORS table:

- VendorID (PK)
- VendorName
- VendorPhone

VENDOR_SUPPORT table:

- VendorSupportID (PK)
- VendorID (FK)
- VendorSupportName
- VendorSupportExtension

SOFTWARE table:

- SoftwareID (PK)
- SoftwareName
- SoftwareVendor
- SoftwareLicenceExpires
- SoftwareLicencePrice

USERS table:

- UserID (PK)
- UserName

USER_AUTHORIZATIONS table:

- UserAuthorizationID (PK)
- ComputerSerialNbr (FK)
- SoftwareID (FK)
- UserID (FK)
- UserAuthorizationStarts
- UserAuthorizationEnds
- UserAuthorizationPassword

referential integrity constraints:

- The VendorID in the COMPUTERS table references the VendorID in the VENDORS table.
- The VendorID in the VENDOR_SUPPORT table references the VendorID in the VENDORS table.
- The ComputerSerialNbr in the USER_AUTHORIZATIONS table references the ComputerSerialNbr in the COMPUTERS table.
- The SoftwareID in the USER_AUTHORIZATIONS table references the SoftwareID in the SOFTWARE table.
- The UserID in the USER_AUTHORIZATIONS table references the UserID in the USERS table.

#### 26

##### a

Functional Dependencies:

- Movie Nbr -> Title, Director ID, Studio ID
- Director ID -> Director Name
- Studio ID -> Studio Name, Studio Location, Studio CEO
- Movie Nbr, Character -> Actor ID
- Actor ID -> Actor Name
- Movie Nbr, Movie Copy Nbr -> Movie Copy Type, Movie Rental Price, - Copy Rental Status, Copy Return Date

##### b

not in 3NF. The Movie Nbr, Character, and Actor ID attributes are not part of any candidate key, but they determine the Movie Copy Type, Movie Rental Price, Copy Rental Status, and Copy Return Date.

##### c

MOVIES table:

- Movie Nbr (PK)
- Title
- Director ID (FK)
- Studio ID (FK)

DIRECTORS table:

- Director ID (PK)
- Director Name

STUDIOS table:

- Studio ID (PK)
- Studio Name
- Studio Location
- Studio CEO

ACTORS table:

- Actor ID (PK)
- Actor Name

CHARACTERS table:

- Character ID (PK)
- Movie Nbr (FK)
- Character
- Actor ID (FK)

MOVIE_COPIES table:

- Movie Copy Nbr (PK)
- Movie Nbr (FK)
- Movie Copy Type
- Movie Rental Price

RENTALS table:

- Rental ID (PK)
- Movie Copy Nbr (FK)
- Copy Rental Status
- Copy Return Date

referential integrity constraints:

- The Director ID in the MOVIES table references the Director ID in the DIRECTORS table.
- The Studio ID in the MOVIES table references the Studio ID in the STUDIOS table.
- The Actor ID in the CHARACTERS table references the Actor ID in the ACTORS table.
- The Movie Nbr in the CHARACTERS table references the Movie Nbr in the MOVIES table.
- The Movie Copy Nbr in the MOVIE_COPIES table references the Movie Copy Nbr in the RENTALS table.
- The Movie Nbr in the MOVIE_COPIES table references the Movie Nbr in the MOVIES table.
