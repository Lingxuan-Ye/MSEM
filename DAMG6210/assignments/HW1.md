# Homework 1

## Part 1

### String

- CHAR(3): `'foo'`, `'a  '`
- VARCHAR(3): `'bar'`, `'b'`
- TEXT: `'foo\nbar\nbaz'`
- ...

### Numeric

- INT: `0`, `1`
- FLOAT(2,1): `0.0`, `0.1`
- ...

### Datetime

- DATE: `'2023-02-06'`, `'1970-01-01'`
- DATETIME: `'2023-02-06 01:02:03'`, `'1970-01-01 00:00:00'`
- TIMESTAMP: `'20230206010203'`, `'19700101000000'`
- TIME: `'01:02:03'`, `'00:00:00'`

### MISC

- ENUM: `ENUM('foo', 'bar', 'baz')`, `ENUM('a', 'b')`
- SET: `SET('a', 'b')`, `SET('c', 'd')`

## Part 2

### Bitwise AND

```sql
SELECT 1 & 2;
-- 0 (0b01 & 0b10 == 0b00)
```

### Greater than operator

```sql
SELECT 1 > 2;
-- 0 (False)
```

### Right shift

```sql
SELECT 3 >> 1;
-- 1 (0b11 >> 1 == 0b01)
```

### Greater than or equal operator

```sql
SELECT 3 >= 1;
-- 1 (True)
```

### Modulo operator

```sql
SELECT 3 % 2;
-- 1
```

## Part 3

### Flow Control Functions

```sql
SELECT
    CASE 1 + 1
        WHEN 1 THEN 'foo'
        WHEN 2 THEN 'bar'
        ELSE 'baz'
    END;
-- 'bar'

SELECT
    IF(
        1 > 0,
        '1 is greater than 0',
        '1 is equal to or less than 0'
    );
-- '1 is greater than 0'
```

### Numeric Functions

```sql
SELECT ABS(-1.0);
-- 1.0

SELECT FLOOR(1.2);
-- 1
```

### Date and Time Functions

```sql
SELECT DATE_SUB('1970-01-01', INTERVAL 1 DAY);
-- '1969-12-31'

SELECT NOW();
-- '2023-02-08 18:24:30'
```

### String Functions

```sql
SELECT CONCAT('1', '+', '1', '=', '10');
-- '1+1=10'

SELECT UPPER('abc');
-- 'ABC'
```

### Aggregate Functions

```sql
-- assume we have a table with column named 'age'

SELECT AVG(age);

SELECT MAX(age);
```

### Window Functions

```sql
SELECT ROW_NUMBER();

SELECT NTH_VALUE(ROW_NUMBER(), 10);
```

## Part 4

### Review Qustions

1. - **data**: Stored representations of objects and events that have meaning and importance in the user’s environment.
    - **information**: Data that have been processed in such a way as to increase the knowledge of the person who uses the data.
    - **metadata**: Data that describe the properties or characteristics of end-user data and the context of those data.
    - **database application**: An application program (or set of related programs) that is used to perform a series of database activities (create, read, update, and delete) on behalf of database users.
    - **data warehouse**: An integrated decision support database whose content is derived from the various operational databases.
    - **constraint**: A rule that cannot be violated by database users.
    - **database**: An organized collection of logically related data.
    - **entity**: A person, a place, an object, an event, or a concept in the user environment about which the organization wishes to maintain data.
    - **database management system**:  Software system that is used to create, maintain, and provide controlled access to user databases.
    - **client/server architecture**: Each member of the work-group has a computer, and the computers are linked by means of network (wired or wireless LAN). In most cases, each computer has a copy of a specialized application (client) which provides the user interface as well as the business logic through which the data is manipulated. The database itself and the DBMS are stored on a central device called the “database server,” which is also connected to the network.
    - **systems development life cycle (SDLC)**: The traditional methodology used to develop, maintain, and replace information systems.
    - **agile software development**: An approach to database and software development that emphasizes “individuals and interactions over processes and tools, working software over comprehensive documentation, customer collaboration over contract negotiation, and response to change over following a plan.”
    - **enterprise data model**: The first step in database development, in which the scope and general contents of organizational databases are specified.
    - **conceptual data model**: A detailed, technology-independent specification of the overall structure of organizational data.
    - **logical data model**: The representation of a database for a particular data management technology.
    - **physical data model**: Specifications for how data from a logical schema are stored in a computer’s secondary memory by a database management system.
2. - c - data
   - b - database application
   - l - constraint
   - g - repository
   - q - metadata
   - m - data warehouse
   - a - information
   - j - user view
   - k - database management system
   - h - data independence
   - e - database
   - i - enterprise resource planning (ERP)
   - r - systems development life cycle (SDLC)
   - o - prototyping
   - f - enterprise data model
   - d - conceptual schema
   - p - internal schema
   - n - external schema
3. - data independence helps decoupling data descriptions and programs while data dependence may cause serious trouble when refactoring.
   - unstructured data refers to those multimedia data which has no fixed structure like structured data does.
   - information is a kind of data that have been processed in such a way as to increase the knowledge of the person who uses the data.
   - repository is a special database that stores data descriptions.
   - enterprise data model describes which kinds of entities to be stored.
   - data warehouse is an integrated decision support database while the ERP system integrates all functions of the enterprise.
   - multitier databases provide a middleware for the interaction of client and server which protect the data and lower the operation complexity for users.
   - prototyping convert requirements to a working system that is continually revised through close work between analysts and users, SDLC is fixed step-by-step approach.
   - enterprise data model provides the scope and general content while conceptual data model provides the details.
   - agile software development emphasizes customer collaboration and response to change.
4. - program-data dependence
   - duplication of data
   - limited data sharing
   - lengthy development times
   - excessive program maintenance
5. - Computer-aided software engineering (CASE) tools
   - Repository
   - DBMS
   - Database
   - Application programs
   - User interface
   - Data and database administrators
   - System developers
   - End users

### Problems and Exercises

1. - many-to-many

        ```mermaid
        erDiagram
            STUDENT }|--|{ COURSE : "register for"
        ```

   - one-to-many
   
        ```mermaid
        erDiagram
            BOOK ||--o{ COPY : "have"
        ```
        
   - one-to-many
   
        ```mermaid
        erDiagram
            COURSE ||--|{ SECTION : "have"
        ```
   
   - one-to-many
   
        ```mermaid
        erDiagram
            SECTION ||--|{ ROOM : "are scheduled in"
        ```
        
   - one-to-many
   
        ```mermaid
        erDiagram
            INSTRUCTOR ||--|{ COURSE : "teach"
        ```

2. need larger memory

2.  

2. multiple databases can prune unnecessary query by predetermine the content to retreive;

    developing several applications simultaneously.

2. members, departments, managers

    ```mermaid
    erDiagram
        MEMBER }|--|| DEPARTMENT : "consist"
        DEPARTMENT ||--|| MANAGER : "is managed by"
    ```
    
## Part 5

All problems solved in [MySQL Shell for VS Code](https://marketplace.visualstudio.com/items?itemName=Oracle.mysql-shell-for-vs-code)

### 1

```sql
SELECT ProdName, InStock + OnOrder as Total
FROM produce
ORDER BY ProdName;
```

### 2

```sql
SELECT ProdName, Variety, InStock, OnOrder
FROM produce
WHERE InStock + OnOrder >= 5000
ORDER BY ProdName;
```

### 3

```sql
SELECT ProdName, Variety, InStock
FROM produce
WHERE InStock >= 1000 AND (ProdName = 'Apples' OR ProdName = 'Oranges')
ORDER BY ProdName;
```

#### 4

```sql
UPDATE produce
SET SeasonAttr = SeasonAttr | 0b00000100
-- if index starts from 0, else change it to 0b00000010
WHERE ProdName = 'Grapes'
ORDER BY ProdName;
```

### 5

```sql
SELECT ProdName, Variety, InStock
FROM produce
WHERE INSTR(LOWER(ProdName), LOWER('Ch')) != 0
ORDER BY ProdName;
```

