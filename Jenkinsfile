pipeline {
    agent {
        docker {
            image 'python:3.12-slim'
        }
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest'
            }
        }

    }
}
