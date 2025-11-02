pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Siddhi-Karhekar/weather-predictor.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build('weather-predictor')
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'echo "Running tests..."'
                // example: sh 'pytest tests/'
            }
        }

        stage('Deploy to Render') {
            steps {
                sh '''
                echo "Deploying to Render..."
                curl -X POST https://api.render.com/deploy/srv-d43mk46mcj7s73b8uoag?key=rnd_tyDHJTbCRISjk59Oi1utkAdYziwv
                '''
            }
        }
    }
}
