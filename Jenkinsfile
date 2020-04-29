pipeline {
    agent any
    stages {
        stage('Dev_Test') {
            steps {
                echo 'starting auto test...'
                try{
                    dir ('d:\\tmp\\yj_auto') {
                        bat 'robot --pythonpath . -L debug cases'
                    }
                }
                catch (err) {
                    echo 'test fail!!!'
                }
                dir ('d:\\tmp\\yj_auto') {
                    bat 'python spend.py'
                }
            }

        }
    }
    post {
        success {
            mail bcc: '', body: "构建版本成功", cc: '', charset: 'UTF-8', from: 'rg_164518@126.com', mimeType: 'text/plain', replyTo: '', subject: "构建版本成功", to: "1918520482@qq.com";
        }
        failure {
            mail bcc: '', body: "<b>fail!!!</b><br>Project: ${env.JOB_NAME} <br>Build Number: ${env.BUILD_NUMBER} <br> URL de build: ${env.BUILD_URL}", cc: '', charset: 'UTF-8', from: '', mimeType: 'text/html', replyTo: '', subject: "ERROR CI: Project name -> ${env.JOB_NAME}", to: "1918520482@qq.com";
        }
        unstable {
            echo 'This will run only if the run was marked as unstable'
        }
        changed {
            echo 'This will run only if the state of the Pipeline has changed'
            echo 'For example, if the Pipeline was previously failing but is now successful'
        }
    }
}