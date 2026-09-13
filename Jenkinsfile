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
                    echo "Creating kubeconfig..."

                    kind get kubeconfig \
                        --internal \
                        --name "${KIND_CLUSTER}" \
                        > "${KUBECONFIG_FILE}"

                    export KUBECONFIG="${KUBECONFIG_FILE}"

                    echo "Kubernetes cluster:"
                    kubectl cluster-info

                    echo "Current deployment:"
                    kubectl get deployment joke-deployment

                    echo "Updating deployment to ${IMAGE}"

                    CONTAINER=$(kubectl get deployment joke-deployment \
                        -o jsonpath='{.spec.template.spec.containers[0].name}')

                    kubectl set image deployment/joke-deployment \
                        "${CONTAINER}=${IMAGE}"

                    echo "Waiting for rollout..."

                    kubectl rollout status deployment/joke-deployment \
                        --timeout=120s
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    export KUBECONFIG="${KUBECONFIG_FILE}"

                    echo "Pods:"
                    kubectl get pods -l app=joke -o wide

                    echo "Deployment:"
                    kubectl get deployment joke-deployment

                    echo "Service:"
                    kubectl get service joke-service
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
