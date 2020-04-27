pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo '执行自动构建...'
                mail bcc: '', body: "构建版本成功", cc: '', charset: 'UTF-8', from: 'rg_164518@126.com', mimeType: 'text/plain', replyTo: '', subject: "构建版本成功", to: "1918520482@qq.com";
            }
        }

        stage('Dev_Test'){
            steps {
                input '等待开发人员测试通过，通过后再继续'
            }
        }

        stage('QA_Test') {
            steps {
                echo '执行自动化测试...'

                dir ('d:\\tmp\\yj_auto') {
                    bat 'robot --pythonpath . --name build_%BUILD_NUMBER% -L debug cases'
                }

            }
        }
    }
}