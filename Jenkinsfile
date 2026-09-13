pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *')
    }

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        IMAGE = "joke-app:${BUILD_NUMBER}"
        KIND_CLUSTER = "joke-cluster"
        KUBECONFIG_FILE = "${WORKSPACE}/kubeconfig"
    }

    stages {

        stage('Test') {
            steps {
                script {
                    docker.image('python:3.12-slim').inside {
                        sh '''
                            python -m venv .venv
                            .venv/bin/pip install --no-cache-dir -r requirements.txt
                            .venv/bin/pytest
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building ${IMAGE}"
                    docker build -t "${IMAGE}" .
                    docker images "${IMAGE}"
                '''
            }
        }

        stage('Load Image into kind') {
            steps {
                sh '''
                    echo "Loading ${IMAGE} into kind..."

                    kind load docker-image "${IMAGE}" \
                        --name "${KIND_CLUSTER}"
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    echo "Deploying joke-app:${BUILD_NUMBER}"

                    kind load docker-image joke-app:${BUILD_NUMBER} \
                        --name joke-cluster

                    kubectl set image deployment/joke-deployment \
                        joke-container=joke-app:${BUILD_NUMBER}

                    kubectl rollout status deployment/joke-deployment \
                        --timeout=120s
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    echo "Deployment status:"
                    kubectl get deployment joke-deployment

                    echo "Pods:"
                    kubectl get pods -l app=joke -o wide

                    echo "Running image:"
                    kubectl get deployment joke-deployment \
                        -o jsonpath='{.spec.template.spec.containers[0].image}'

                    echo
                '''
            }
        }
    }

    post {
        always {
            sh 'rm -f "${KUBECONFIG_FILE}" || true'
        }
    }
}
