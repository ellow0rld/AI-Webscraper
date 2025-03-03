pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/ellow0rld/AI-Webscraper.git'
            }
        }
        stage('Build') {
            steps {
                sh 'echo "Building project..."'
            }
        }
        stage('Deploy') {
            steps {
                sh 'echo "Deploying project..."'
            }
        }
    }
}
