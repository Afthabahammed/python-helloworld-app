pipeline {

    agent any

    environment {

        // ==============================
        // CHANGE THESE VALUES
        // ==============================

        DOCKERHUB_USERNAME = 'afthab12'
        DOCKER_IMAGE = "${DOCKERHUB_USERNAME}/python-helloworld-app"

        // Jenkins credential IDs
        DOCKER_CREDENTIALS = 'docker-cred'

        // Kubernetes deployment
        K8S_DEPLOYMENT = 'python-helloworld-app'
        K8S_NAMESPACE = 'argocd-operator'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(
            logRotator(numToKeepStr: '10')
        )
    }

    stages {

        stage('Checkout') {

            steps {

                echo 'Checking out source code...'

                checkout scm
            }
        }

        stage('Verify Files') {

            steps {

                sh '''
                    echo "Checking project files..."

                    ls -la

                    echo "Python version:"
                    python3 --version || true

                    echo "Docker version:"
                    docker --version
                '''
            }
        }

        stage('Build Docker Image') {

            steps {

                echo "Building Docker image..."

                sh '''
                    docker build \
                    -t ${DOCKER_IMAGE}:${BUILD_NUMBER} \
                    -t ${DOCKER_IMAGE}:latest \
                    .
                '''
            }
        }

        stage('Login to DockerHub') {

            steps {

                echo 'Logging in to DockerHub...'

                withCredentials([
                    usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS}",
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {

                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                        -u "$DOCKER_USERNAME" \
                        --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {

            steps {

                echo 'Pushing image to DockerHub...'

                sh '''
                    docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}
                    docker push ${DOCKER_IMAGE}:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {

            steps {

                echo 'Deploying application to Kubernetes...'

                sh '''
                    kubectl apply -f deployment.yaml \
                    -n ${K8S_NAMESPACE}

                    kubectl apply -f service.yaml \
                    -n ${K8S_NAMESPACE}

                    kubectl set image deployment/${K8S_DEPLOYMENT} \
                    python-helloworld-app=${DOCKER_IMAGE}:${BUILD_NUMBER} \
                    -n ${K8S_NAMESPACE}

                    kubectl rollout status deployment/${K8S_DEPLOYMENT} \
                    -n ${K8S_NAMESPACE}
                '''
            }
        }

        stage('Verify Deployment') {

            steps {

                sh '''
                    echo "=============================="
                    echo "Pods"
                    echo "=============================="

                    kubectl get pods \
                    -l app=python-helloworld-app \
                    -n ${K8S_NAMESPACE}

                    echo "=============================="
                    echo "Service"
                    echo "=============================="

                    kubectl get service \
                    python-helloworld-service \
                    -n ${K8S_NAMESPACE}

                    echo "=============================="
                    echo "Deployment"
                    echo "=============================="

                    kubectl get deployment \
                    python-helloworld-app \
                    -n ${K8S_NAMESPACE}
                '''
            }
        }
    }

    post {

        success {

            echo '''
            =====================================
            BUILD SUCCESSFUL
            =====================================
            FastAPI application deployed successfully!
            =====================================
            '''
        }

        failure {

            echo '''
            =====================================
            BUILD FAILED
            =====================================
            Check the Jenkins console output.
            =====================================
            '''
        }

        always {

            sh '''
                docker logout || true
            '''
        }
    }
}
