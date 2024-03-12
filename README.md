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

SonarQube is used to evaluate code quality, including metrics for code complexity, duplication, maintainability, and security vulnerabilities. From the following picture, these metrics are satisfied for improvement and maintain high-quality code standards for the progam. 

![311001368-08129a62-14a9-4cc2-8534-a5725ce5c5e6](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/06613a0b-58d7-4c35-b77c-bcea4e619cd7)

# 5. Clean Code Development
The code from system.py demonstrates several aspects of clean code development such as readability, modularity, simplicity, error handling and consistency. First, variable and method names have been made more consistent and descriptive to enhance readability. Second, repeated code blocks have been refactored into reusable functions. Third, comments that merely repeated what the code was doing have been removed, favoring descriptive function and variable names instead. Fourth, simplified conditional expressions where possible to make the code more straightforward. Finally, each method now focuses on a single responsibility, promoting better maintainability and readability. An example is extracted from the system.py file: 

![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/667c1f88-c4e8-4840-ae27-318d25e86979)

![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/ec4ffe81-d760-417f-9a97-794f39b5425b)

# 6. Build Management
PyBuilder

![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/ad226445-b19b-4b9e-908e-d731d6fe4d76)

# 7. Unit Tests

* Test logging with a user account

  ![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/df5a3938-2a49-4ff9-b1e8-1a7c65c60d35)

* Test logging with admin account

  ![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/be75d07a-db18-4045-918c-aa1637d84726)
  
* Result for both unit tests

  ![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/f91dd942-0313-46d3-832a-4c3ed82dd220)
  ![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/9f737928-1ed9-477c-a61e-3961d4e7c7bb)


# 8. Continuous Delivery
Jenkins

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

![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/1c916371-373f-44b7-9b51-ef942c027de3)

# 9. IDE
VSCode
![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/9719efe6-1616-444d-bf83-05f2aed491af)

# 10. DSL

![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/e3e04e33-4d7d-4067-b6e6-fac933ec4c13)

+ connect: Allows users to connect to the specified cinema database using SQLite.
+ get_movie_with_highest_rating: Retrieves the movie with the highest rating from the database by executing a SQL query.
+ The DSL is demonstrated by connecting to the database, retrieving the movie with the highest rating, and printing its name.

# 11. Functional Programming

* Final Data Structures: The data structures used in the code, such as lists and tuples, appear to be immutable. For example, in the view_movies method, a list of Movie objects is created from fetched data, which seems to remain unchanged once created.

* (Mostly) Side-Effect-Free Functions: Most functions in the code seem to have minimal side effects. For instance, methods like view_movies, view_customer_bookings, and get_available_seats appear to be pure functions as they take input arguments and return computed results without modifying any external state. However, methods like handle_login, handle_registration, and functions that interact with the database involve side effects (such as database interactions), but these are isolated to specific areas of the code.

* Use of Higher-Order Functions: Higher-order functions are functions that take other functions as parameters or return functions as results. There are several instances of this in the code: The create_user_instance function is a higher-order function as it returns different types of users (Customer or Admin) based on the provided parameters. The menu function inside handle_user_menu is another example. It defines a menu loop and is invoked within the handle_user_menu function. Additionally, there are built-in higher-order functions like map or filter that could potentially be utilized in various parts of the code for more functional style operations.

* Functions as Parameters and Return Values: The create_user_instance function takes a function (either Admin or Customer) as a parameter and returns an instance of that type. Functions like handle_user_menu and menu return functions or accept functions as parameters. In the login method, the create_user_instance function is passed as a parameter to determine the type of user to create.

* Use of Closures/Anonymous Functions: While the code doesn't explicitly demonstrate closures, it does utilize anonymous functions (lambda functions) in certain places. For instance, you might use a lambda function as a callback function in GUI libraries or event-driven programming. Although not prevalent in the provided snippet, closures could potentially be used in more advanced scenarios or if the code is extended.

Overall, the code demonstrates several aspects of functional programming, including the use of immutable data structures, (mostly) side-effect-free functions, higher-order functions, functions as parameters and return values, and the potential use of closures/anonymous functions in certain contexts.
