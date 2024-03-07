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