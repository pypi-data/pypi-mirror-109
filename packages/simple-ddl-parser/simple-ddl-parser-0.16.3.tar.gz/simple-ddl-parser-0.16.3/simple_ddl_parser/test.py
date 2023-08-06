from simple_ddl_parser import DDLParser

ddl = """
CREATE TABLE Persons (
    ID int NOT NULL,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int,
    City varchar(255),
    CONSTRAINT CHK_Person CHECK (Age>=18 AND City='Sandnes'),
    CHECK (LastName != FirstName)
    );
"""
result = DDLParser(ddl).run(group_by_type=True)

print(result)
