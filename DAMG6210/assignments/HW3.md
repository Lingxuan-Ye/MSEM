# Homework 3

## 1

![](./assets/1.svg)

## 2

### a

![2a](./assets/2a.svg)

### b

![2b](./assets/2b.svg)

### c

```mermaid
erDiagram
          Case ||..|| Case_Plaintiff : "brings"
          Case ||..|| Case_Defendant : "involved in"
          LegalEntity ||--|{ Plaintiff : "inherits"
          LegalEntity ||--|{ Defendant : "inherits"
          Plaintiff ||..|| Case_Plaintiff : "brings"
          Defendant ||..|| Case_Defendant : "involved in"

          Case {
            o case_number PK
            o date_opened
            o date_closed
            o judgment_description
          }

          LegalEntity {
            o entity_number PK
            o name
            o net_worth
          }

          Plaintiff {
            o requested_judgment
          }

          Defendant {
          }

          Case_Plaintiff {
            o case_number FK
            o entity_number FK
          }

          Case_Defendant {
            o case_number FK
            o entity_number FK
          }

```

### d

```mermaid
erDiagram
          Publisher ||--|{ Book : "publishes"
          Author ||--|{ Book_Author : "writes"
          Book ||..|| Book_Author : "is written by"
          Book ||--|| Publisher : "is published by"
          Author ||--|{ Royalty_Check : "receives"

          Publisher {
            o publisher_name PK
            o mailing_address
            o telephone_number
          }

          Book {
            o ISBN PK
            o title
            o price
            o number_of_pages
            o publisher_name FK
          }

          Author {
            o author_id PK
            o name
            o address
          }

          Book_Author {
            o ISBN FK
            o author_id FK
            o royalty_rate
          }

          Royalty_Check {
            o check_number PK
            o date
            o amount
            o author_id FK
          }

```

## 3

```mermaid
erDiagram
          Customer ||--|{ Location : "has"
          Location ||--|{ Location_Rate : "assigned"
          Rate ||..|| Location_Rate : "applies to"

          Customer {
            o ustomer_id PK
            o ame
            o treet
            o ity
            o tate
            o ip_code
            o elephone
          }

          Location {
            o ocation_id PK
            o treet
            o ity
            o tate
            o ip_code
            o ype
            o ustomer_id FK
          }

          Rate {
            o ate_class PK
            o ate_per_kwh
          }

          Location_Rate {
            o ocation_id FK
            o ate_class FK
          }

```

- A Customer can have multiple locations, so we create a one-to-many relationship between Customer and Location.
- Each location can have one or more rates, depending on the time of day. To represent this, we create a many-to-many relationship between Location and Rate using an associative entity called Location_Rate.
- Rate Class is used as a primary key for the Rate entity, assuming it uniquely identifies each rate.

## 4

```mermaid
erDiagram
          Student ||--o{ Assigned_Adviser : "assigned to"
          Student ||--o{ Registration : "registered with"
          Adviser ||..o{ Assigned_Adviser : "advises"
          Adviser ||..o{ Registration : "assists"

          Student {
            o student_id PK
            o name
          }

          Adviser {
            o adviser_id PK
            o name
          }

          Assigned_Adviser {
            o student_id FK
            o adviser_id FK
          }

          Registration {
            o student_id FK
            o adviser_id FK
            o term
          }

```

## 5

```mermaid
erDiagram
          SalesOffice ||--|{ Employee : "has"
          Employee ||--|| Manager : "manages"
          SalesOffice ||--|{ Property : "lists"
          Property ||..|| Property_Owner : "owned by"
          Owner ||..|| Property_Owner : "owns"

          SalesOffice {
            o office_number PK
            o location
          }

          Employee {
            o employee_id PK
            o name
            o office_number FK
          }

          Manager {
            o employee_id PK
          }

          Property {
            o property_id PK
            o address
            o city
            o state
            o zip_code
            o office_number FK
          }

          Owner {
            o owner_id PK
            o name
          }

          Property_Owner {
            o property_id FK
            o owner_id FK
            o percent_owned
          }

```

## 6

```mermaid
erDiagram
          ConcertSeason ||--|{ Concert : "schedules"
          Concert ||--|{ Concert_Composition : "includes"
          Composition ||..|| Concert_Composition : "performed at"
          Conductor ||..o{ Concert : "conducts"
          Soloist ||--|{ Soloist_Composition : "performs"
          Composition ||..|| Soloist_Composition : "requires"

          ConcertSeason {
            o opening_date PK
          }

          Concert {
            o concert_number PK
            o concert_date
            o opening_date FK
            o conductor_id FK
          }

          Composition {
            o composition_id PK
            o composer_name
            o composition_name
            o movement_id
          }

          Conductor {
            o conductor_id PK
            o name
          }

          Soloist {
            o soloist_id PK
            o name
          }

          Concert_Composition {
            o concert_number FK
            o composition_id FK
          }

          Soloist_Composition {
            o soloist_id FK
            o composition_id FK
            o date_last_performed
          }
```

## 7

```mermaid
erDiagram
          Employee ||--o{ Marriage : "married to"
          Employee ||--|{ JobTitle : "has"
          Employee ||--o{ Department : "reports to"
          Department ||--o{ VendorDepartment : "deals with"
          Vendor ||..|| VendorDepartment : "supplies"
          Employee ||--|{ EmployeeProject : "works on"
          Project ||..|| EmployeeProject : "assigned to"
          City ||..o{ Project : "located in"
          Employee ||--|{ EmployeeSkill : "possesses"
          Skill ||..|| EmployeeSkill : "used in"
          EmployeeProject ||--|{ ProjectSkill : "uses"
          Skill ||..|| ProjectSkill : "applied to"

          Employee {
            o employee_number PK
            o name
            o dob
          }

          Marriage {
            o spouse1 FK
            o spouse2 FK
            o marriage_date
          }

          JobTitle {
            o employee_number FK
            o title
          }

          Department {
            o department_name PK
            o phone_number
          }

          Vendor {
            o vendor_name PK
            o address
          }

          VendorDepartment {
            o department_name FK
            o vendor_name FK
            o last_meeting_date
          }

          Project {
            o project_number PK
            o estimated_cost
            o city_name FK
          }

          City {
            o city_name PK
            o state
            o population
          }

          EmployeeProject {
            o employee_number FK
            o project_number FK
          }

          Skill {
            o skill_number PK
            o description
          }

          EmployeeSkill {
            o employee_number FK
            o skill_number FK
          }

          ProjectSkill {
            o employee_project_id FK
            o skill_number FK
          }

```

## 8

```mermaid
erDiagram
          Item ||--o{ Purchase : "purchased"
          Client ||..|| Purchase : "sells"
          Item ||--o{ Sale : "sold"
          Client ||..|| Sale : "buys"

          Item {
            o item_number PK
            o description
            o asking_price
            o condition
            o comments
          }

          Client {
            o client_number PK
            o name
            o address
          }

          Purchase {
            o item_number FK
            o client_number FK
            o purchase_cost
            o date_purchased
            o purchase_condition
          }

          Sale {
            o item_number FK
            o client_number FK
            o commission_paid
            o selling_price
            o sales_tax
            o date_sold
          }

```

## 9

```mermaid
erDiagram
          Graduate ||--o{ Major : "completed"
          Graduate ||--o{ Attendance : "attended"
          Event ||..|| Attendance : "held for"
          Graduate ||--o{ Interaction : "contacted"
          InteractionType ||..|| Interaction : "has type"

          Graduate {
            o student_number PK
            o name_when_student
            o country_of_birth
            o current_country_of_citizenship
            o current_name
            o current_address
          }

          Major {
            o student_number FK
            o major_name
          }

          Event {
            o event_id PK
            o title
            o date
            o location
            o type
          }

          Attendance {
            o student_number FK
            o event_id FK
            o comments
          }

          Interaction {
            o interaction_id PK
            o student_number FK
            o interaction_type_id FK
            o date
            o comments
          }

          InteractionType {
            o interaction_type_id PK
            o type
          }
```

## 10

```mermaid
erDiagram
          ATTORNEY ||--o{ CASE_ATTORNEY : "retained"
          CLIENT ||--o{ CASE_CLIENT : "retained"
          CASE ||..|| CASE_ATTORNEY : "involves"
          CASE ||..|| CASE_CLIENT : "involves"
          ATTORNEY ||--o{ Attorney_Specialty : "has"
          ATTORNEY ||--o{ Attorney_Bar : "belongs to"
          CASE ||--|| COURT : "assigned to"
          JUDGE ||--|| COURT : "assigned to"

          ATTORNEY {
            o Attorney_ID PK
            o Name
            o Address
            o City
            o State
            o Zip_Code
          }

          CLIENT {
            o Client_ID PK
            o Name
            o Address
            o City
            o State
            o Zip_Code
            o Telephone
            o Date_of_Birth
          }

          CASE {
            o Case_ID PK
            o Case_Description
            o Case_Type
          }

          CASE_ATTORNEY {
            o Attorney_ID FK
            o Case_ID FK
          }

          CASE_CLIENT {
            o Client_ID FK
            o Case_ID FK
          }

          COURT {
            o Court_ID PK
            o Court_Name
            o City
            o State
            o Zip_Code
          }

          JUDGE {
            o Judge_ID PK
            o Name
            o Years_In_Practice
            o Court_ID FK
          }

          Attorney_Specialty {
            o Attorney_ID FK
            o Specialty
          }

          Attorney_Bar {
            o Attorney_ID FK
            o Bar
          }

```

