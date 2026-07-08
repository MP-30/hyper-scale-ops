pipeline {
    agent {
        label 'docker-agent'
    }

    environment {
        DOCKER_IMAGE = "mp30/hyper-ops:${BUILD_NUMBER}"
        DOCKERHUB_CREDENTIAL = credentials('dockerid')
    }
    stages {
             stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/MP-30/hyper-scale-ops.git'
            }
        }

        stage('Unit Tests'){
            steps {
                withCredentials([file(credentialsId: 'hyper-ops-test-env', variable: 'ENV_FILE')]) {
                sh '''
                cp $ENV_FILE .env.test

                export $(grep -v '^#' .env.test | xargs)

                pytest
                '''
                }
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

        stage('Deploy local') {
            steps {
                withCredentials([file(credentialsId: 'hyper-ops-env', variable: 'ENV_FILE')]) {
                sh """
                docker rm -f hyper-ops || true

                docker run -d \
                    --name hyper-ops \
                    --env-file $ENV_FILE \
                    -p 8000:8000 \
                    ${DOCKER_IMAGE}
                """
                }
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

            slackSend tokenCredentialId: 'slack-link',
                      color: '#00FF00', // Green bar
                      message: "SUCCESS: FastAPI build and test succeeded on Jenkins! Job: ${env.JOB_NAME} [Build #${env.BUILD_NUMBER}] (${env.BUILD_URL})"

        }
        failure {
            mail body: 'Jenkins Python Pipeline Failed! Please check the console logs.',
                 subject: 'ALARM: Jenkins Python Build Failed',
                 to: 'learningonly092@gmail.com'

            slackSend tokenCredentialId: 'slack-link',
                      color: '#FF0000', // Red bar
                      message: "ALARM: Jenkins Python Build Failed! Check console logs. Job: ${env.JOB_NAME} [Build #${env.BUILD_NUMBER}] (${env.BUILD_URL})"
        }
    }
}