pipeline {
    agent any
    stages {
        stage('QA_Test') {
            steps {
                echo '执行自动化测试...'

                dir ('d:\\tmp\\yj_auto') {
                    bat 'robot --pythonpath . -L debug cases'
                }

            }
        }
    }
}