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

        stage('Unit Tests') {
            steps {
                withCredentials([file(credentialsId: 'hyper-ops-test-env', variable: 'TEST_ENV_FILE')]) {
                    sh '''
                    cp "$TEST_ENV_FILE" .env.test
                    make run-pytest
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

        stage('Heroku Verification') {
            steps {
                withCredentials([
                    string(credentialsId: 'heroku-api-key', variable: 'HEROKU_API_KEY')
                ]) {
                    sh '''
                    export HEROKU_API_KEY=$HEROKU_API_KEY

                    heroku auth:whoami
                    heroku apps
                    heroku ps --app hyper-scale-ops-dev
                    heroku buildpacks --app hyper-scale-ops-dev
                    '''
                }
            }
        }
        stage('Deploy to Heroku') {
            steps {
                withCredentials([
                    string(credentialsId: 'heroku-api-key', variable: 'HEROKU_API_KEY')
                ]) {
                    sh '''
                    set -e

                    export HEROKU_API_KEY=$HEROKU_API_KEY

                    echo "Configuring Git..."
                    git config user.name "Jenkins"
                    git config user.email "jenkins@localhost"

                    echo "Adding Heroku remote..."
                    git remote remove heroku || true
                    heroku git:remote --app hyper-scale-ops-dev

                    git remote -v

                    echo "Deploying to Heroku..."
                    git push heroku main:main --force
                    '''
                }
            }
        }
        stage('Debug') {
             steps {
                withCredentials([
                    string(credentialsId: 'heroku-api-key', variable: 'HEROKU_API_KEY')
                ]) {
                    sh '''
                    export HEROKU_API_KEY=$HEROKU_API_KEY

                    heroku ps --app hyper-scale-ops-dev
                    '''
                }
        }
    }
    post {
        success {
            mail body: 'FastAPI build and test succeeded on Jenkins!',
                 subject: 'Success: Jenkins Python Pipeline',
                 to: 'learningonly092@gmail.com'

            withCredentials([string(credentialsId: 'slack-link', variable: 'SLACK_WEBHOOK')]) {
                sh '''
                curl -X POST -H 'Content-type: application/json' \
                --data '{"text":"✅ SUCCESS: FastAPI build succeeded. Job: '"$JOB_NAME"' Build #'"$BUILD_NUMBER"'"}' \
                "$SLACK_WEBHOOK"
                '''
            }
        }
        failure {
            mail body: 'Jenkins Python Pipeline Failed! Please check the console logs.',
                 subject: 'ALARM: Jenkins Python Build Failed',
                 to: 'learningonly092@gmail.com'

            withCredentials([string(credentialsId: 'slack-link', variable: 'SLACK_WEBHOOK')]) {
                sh '''
                curl -X POST -H 'Content-type: application/json' \
                --data '{"text":"❌ FAILURE: FastAPI build failed. Job: '"$JOB_NAME"' Build #'"$BUILD_NUMBER"'"}' \
                "$SLACK_WEBHOOK"
                '''
            }
        }
    }
}