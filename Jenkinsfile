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
                catch (exc) {
                    if not (dir ('d:\\tmp\\yj_auto') {
                                bat 'python spend.py'
                            }){
                    mail bcc: '', body: "构建版本失败", cc: '', charset: 'UTF-8', from: 'rg_164518@126.com', mimeType: 'text/plain', replyTo: '', subject: "build_${BUILD_NUMBER}$", to: "1918520482@qq.com";
                    }
                    mail bcc: '', body: "构建版本成功", cc: '', charset: 'UTF-8', from: 'rg_164518@126.com', mimeType: 'text/plain', replyTo: '', subject: "build_${BUILD_NUMBER}$", to: "1918520482@qq.com";
                    throw
                }

            }
        }
    }
}