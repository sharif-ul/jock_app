pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    reuseNode true
                }
            }

            steps {
                sh '''
                    python -m venv .venv
                    .venv/bin/pip install --no-cache-dir -r requirements.txt
                    .venv/bin/pytest
                '''
            }
        }

        stage('Check Docker') {
            steps {
                sh 'docker --version'
                sh 'docker ps'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t joke-app:${BUILD_NUMBER} .'
            }
        }
    }
}
