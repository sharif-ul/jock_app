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
    KUBECONFIG = "${WORKSPACE}/kubeconfig"
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
                set -e

                echo "Building ${IMAGE}"

                docker build -t "${IMAGE}" .

                echo "Built image:"
                docker images "${IMAGE}"
            '''
        }
    }

    stage('Load Image into kind') {
        steps {
            sh '''
                set -e

                echo "Loading ${IMAGE} into ${KIND_CLUSTER}..."

                kind load docker-image "${IMAGE}" \
                    --name "${KIND_CLUSTER}"

                echo "Image loaded successfully."
            '''
        }
    }

    stage('Configure Kubernetes') {
        steps {
            sh '''
                set -e

                echo "Configuring kubeconfig for ${KIND_CLUSTER}..."

                rm -f "${KUBECONFIG_FILE}"

                kind export kubeconfig \
                    --name "${KIND_CLUSTER}" \
                    --kubeconfig "${KUBECONFIG_FILE}"

                export KUBECONFIG="${KUBECONFIG_FILE}"
                chmod 600 "${KUBECONFIG_FILE}"

                kubectl config current-context
                kubectl cluster-info
                kubectl get nodes -o wide
            '''
        }
    }

    stage('Deploy to Kubernetes') {
        steps {
            sh '''
                set -e
                export KUBECONFIG="${KUBECONFIG_FILE}"

                echo "Deploying ${IMAGE}..."

                kubectl set image deployment/joke-deployment \
                    joke-container="${IMAGE}"

                echo "Waiting for rollout..."
                kubectl rollout status deployment/joke-deployment --timeout=120s
            '''
        }
    }
    stage('Verify Deployment') {
        steps {
            sh '''
                set -e

                echo "Deployment status:"
                kubectl get deployment joke-deployment

                echo
                echo "Pods:"
                kubectl get pods -l app=joke -o wide

                echo
                echo "Running image:"
                kubectl get deployment joke-deployment \
                    -o jsonpath='{.spec.template.spec.containers[0].image}'

                echo

                echo
                echo "ReplicaSets:"
                kubectl get replicasets -l app=joke
            '''
        }
    }
}

post {
    always {
        sh '''
            rm -f "${KUBECONFIG_FILE}" || true
        '''
    }
}


}