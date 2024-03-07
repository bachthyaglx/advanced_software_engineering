# 1. Git
  ![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/1fb97edd-7604-410f-8e1d-38a122849718)


# 2. UML
* Usecases
  
  ![Cinema_Usecases](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/3aec3fb2-627d-48a0-9e72-0c8992fc279d)

* Class
  
  ![Cinema_Class](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/51b8fa94-a359-449d-9704-6ed2f91d5356)

* Activity
  
  ![Cinema_Activity](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/fe6bec53-9358-4e4c-9c4a-742d46454b0f)

# 3. DDD

![Cinema_DDD](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/bd506c19-1724-4145-a1b3-887c02103031)

# 4. Metrics

![image](https://github.com/bachthyaglx/advanced_software_engineering/assets/62774638/08129a62-14a9-4cc2-8534-a5725ce5c5e6)


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


# 11. Functional Programming
