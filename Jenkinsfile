pipeline {
    agent any
    stages {
        stage('Dev_Test') {
            steps {
                script{
                    dir ('d:\\tmp\\yj_auto') {
                        bat 'for /r . %i in (*.xml,*.html) do @del %i'
                        echo 'starting auto test...'
                        try{
                            bat 'robot --pythonpath . -L debug cases'
                        }
                        catch (err) {
                            echo 'test fail!!!'
                        }
                        bat 'python spend.py'
                    }
                }
            }
        }
    }
    post {
        always {
            bat 'copy d:\\tmp\\yj_auto\\report.html ${JENKINS_HOME}\\workspace\\${ITEM_FULL_NAME}'
        }
        success {
            mail bcc: '', body: "构建版本成功", cc: '', charset: 'UTF-8', from: 'rg_164518@126.com', mimeType: 'text/plain', replyTo: '', subject: "构建版本成功", to: "1918520482@qq.com";
        }
        failure {
            emailext (
                subject: "构建版本失败",body: '''${FILE,path="report.html"}''',
                charset: 'UTF-8', from: 'rg_164518@126.com', mimeType: 'text/html',
                to: "1918520482@qq.com"
                )
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