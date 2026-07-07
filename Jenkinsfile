pipeline {
    agent {
        label 'dind-agent'
    }

    environment {
        DOCKER_IMAGE = "mp30/hyper-ops:${BUILD_NUMBER}"
        DOCKERHUB_CREDENTIAL = credentials('dockerid')
    }
    stages {
        stage('Check Docker') {
            steps {
                sh '''
                    echo "===== USER ====="
                    whoami

                    echo "===== PATH ====="
                    echo $PATH

                    echo "===== WHICH DOCKER ====="
                    which docker || true

                    echo "===== DOCKER VERSION ====="
                    docker --version || true

                    echo "===== DOCKER BINARY ====="
                    ls -l /usr/bin/docker || true
                    ls -l /usr/local/bin/docker || true
                '''
            }
        }

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/MP-30/hyper-scale-ops.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }
        stage('RUN Tests') {
            steps {
                sh 'echo "Running faltu tests..."'
            }
        }
        stage('Dockerhub login and push') {
            steps {
                sh '''
                    echo ${DOCKERHUB_CREDENTIAL_PSW} | docker login -u ${DOCKERHUB_CREDENTIAL_USR} --password-stdin
                    docker push ${DOCKER_IMAGE}
                    docker logout
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh 'echo "Deploying..."'
            }
        }
        stage('Debug') {
            steps {
                sh '''
                    echo "debuging..."
                '''
            }
        }
    }
    post {
        success {
            mail body: 'FastAPI build and test succeeded on Jenkins!',
                 subject: 'Success: Jenkins Python Pipeline',
                 to: 'learningonly092@gmail.com'
        }
        failure {
            mail body: 'Jenkins Python Pipeline Failed! Please check the console logs.',
                 subject: 'ALARM: Jenkins Python Build Failed',
                 to: 'learningonly092@gmail.com'
        }
    }
}