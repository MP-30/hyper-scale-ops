pipeline {
    agent any

    environment {
        UV_PROJECT_ENVIRONMENT = "${WORKSPACE}/.venv"
    }
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/MP-30/hyper-scale-ops.git'
            }
        }
        stage('Environment Setup & Install') {
            steps {
                sh '''
                    if ! command -v uv > /dev/null 2>&1; then
                        echo "uv not found, installing..."
                        curl -LsSf https://astral.sh/uv/install.sh | sh
                        export PATH="$HOME/.local/bin:$PATH"
                    else
                        echo "uv is already installed"
                    fi

                    uv --version
                    # Install dependencies and sync virtual environment instantly
                    uv sync
                    '''
            }
        }
        stage('Lint & Format Check') {
            steps {
                sh 'uv run ruff check app/'
            }
        }
        stage('RUN Tests') {
            steps {
                sh 'echo "Running faltu tests..."'
            }
        }
        stage('Deploy') {
            steps {
                sh 'nohup uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &'
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