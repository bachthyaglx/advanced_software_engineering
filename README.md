# 1. Git
  ![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/1fb97edd-7604-410f-8e1d-38a122849718)

# 2. UML
* Usecases - The usecase diagram illustrates the interactions between actors including users and administrators, and the functionality of system. The diagram also depict relationships in how actors use the system's features to achieve specific goals. Customers and administrators have certain rights to interact with the system to perform actions such as logging in, booking tickets, managing movies, and managing customer bookings, ect...
  
  ![Cinema_Usecases](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/3aec3fb2-627d-48a0-9e72-0c8992fc279d)

* Class - The class diagram represents the static structure of system, showing classes, attributes, methods, and their relationships. The classes within the system include entities such as users, movies, rooms, seats, tickets, and the system itself. Each entity is defined by its respective attributes and methods. Relationships also show associations between classes. For example, users book tickets, movies have rooms, etc.. and their multiplicities.
  
  ![Cinema_Class](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/51b8fa94-a359-449d-9704-6ed2f91d5356)

* Activity - The activity diagram shows the flow of activities and actions performed by users and administrators. Activities include logging in, booking tickets, managing movies, and managing customer bookings, each represented by activity nodes. Control flow arrows depict the sequence of actions, decisions, and loops involved in each activity, providing insight into the system's workflow and user interactions.
  
  ![Cinema_Activity](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/fe6bec53-9358-4e4c-9c4a-742d46454b0f)

# 3. DDD 

The DDD shows bounded contexts of system that are defined around key domain entities, including users, movies, rooms, seats, bookings, tickets, payment. Each bounded context is customized to handle operations and rules related to that specific entity. For instance, the user bounded context manages user authentication, registration, and customer-related functionalities, while the movie bounded context handles tasks like retrieving movie information, managing directors, and maintaining release dates, etc...

![Cinema_DDD](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/bd506c19-1724-4145-a1b3-887c02103031)

# 4. Metrics

SonarQube is used to evaluate code quality, including metrics for code complexity, duplication, maintainability, and security vulnerabilities. From the following picture, these metrics are meet to ensure the improvement and maintain high-quality code standards for the progam. 

![311001368-08129a62-14a9-4cc2-8534-a5725ce5c5e6](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/06613a0b-58d7-4c35-b77c-bcea4e619cd7)

# 5. Clean Code Development

The code from system.py demonstrates several aspects of clean code development such as readability, modularity, simplicity, error handling and consistency. Following examples are extracted from the system.py file to qualify whether these aspects are meet.

![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/667c1f88-c4e8-4840-ae27-318d25e86979)

![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/ec4ffe81-d760-417f-9a97-794f39b5425b)

# 6. Build Management

PyBuilder is used for enhances development efficiency, testing, and dependency management. This extended tools is specifically for project configurations using Python language. 

![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/ad226445-b19b-4b9e-908e-d731d6fe4d76)

# 7. Unit Tests

* Test logging with a valid user account

  ![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/df5a3938-2a49-4ff9-b1e8-1a7c65c60d35)

* Test logging with a valid admin account

  ![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/be75d07a-db18-4045-918c-aa1637d84726)
  
* Result for both unit tests

  ![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/f91dd942-0313-46d3-832a-4c3ed82dd220)
  ![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/9f737928-1ed9-477c-a61e-3961d4e7c7bb)


# 8. Continuous Delivery

The following Jenkins pipeline automates various stages of the continuous delivery process.

pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: 'main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/bachthyaglx/advanced_software_engineering.git']])
            }
        }
        stage('Build') {
            steps {
                git branch: 'main', url: 'https://github.com/bachthyaglx/advanced_software_engineering.git'
                bat 'python -m py_compile src/main/python/main.py'
                stash(name: 'compiled-results', includes: 'src/main/python/*.py*')
            }
        }
        stage('Test') {
            steps {
                bat 'python -m py_compile src/unittest/python/tests.py' 
                echo 'The job has been tested'
            }
        }
    }
}

* 'Checkout' - Pulls the latest changes from the main branch of your repository, ensuring that the pipeline always operates on the latest codebase. 
* 'Build' - Compiles the Python code using the py_compile module and stashes the compiled results for further deployment and testing phases. 
* 'Test' - Executes unit tests on the Python codebase to ensure its quality and reliability before proceeding with deployment
 
![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/1c916371-373f-44b7-9b51-ef942c027de3)

# 9. IDE

Visual Studio Code (VSCode) is used for programming and developing software. The following picture shows the working environment of VSCode and the project tree (on the left side). 

![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/9719efe6-1616-444d-bf83-05f2aed491af)

My top favorvate key shortcuts on VSCode:

* Ctrl + alt + up/down - Add cursor to multiple lines
* Ctrl + K + C - Comment multiple lines
* Ctrl + K + U - Uncomment multiple lines
* Ctrl + C followed by Ctrl + V - Copy/paste

# 10. DSL

The following picture is an example of DSL, showing the connection to the database, retrieving the movie with the highest rating, and printing its name.
  
![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/e3e04e33-4d7d-4067-b6e6-fac933ec4c13)

* connect: Allows users to connect to the specified cinema database using SQLite.
* get_movie_with_highest_rating: Retrieves the movie with the highest rating from the database by executing a SQL query.

# 11. Functional Programming

* Final Data Structures - In the view_movies method, a list of Movie objects is created from fetched data, which seems to remain unchanged once created.
  
![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/ac2e1430-5999-40a2-aad0-d76c9468217c)

* (Mostly) Side-Effect-Free Functions - The login function retrieves user data from the database based on the provided email and password, without causing any side effects. It returns user information based on the given credentials and does not modify any external state. 

![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/89389770-b8a6-4c97-9b4c-457086f4f95b)

* Use of Higher-Order Functions - The handle_user_menu demonstrates the concept of higher-order functions by dynamically selecting and executing different menu functions based on the user's role.

![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/5d77a453-2091-4bbb-96b4-4172ecf3dd88)

* Functions as Parameters and Return Values - The handle_login function demonstrates functions as parameters. It passes email and password to the login function, then return values with a tuple containing user and role from the login function.

![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/fd308deb-b8bd-49b6-88e0-87bba7010c94)

* Use of Closures/Anonymous Functions: The manage_customer_bookings function demonstrates the use of anonymous functions through the input() function.

![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/c942501e-9fe2-4632-b10d-7d357b7d21f1)
