pipeline {
    agent any
    stages {
        stage('Dev_Test') {
            steps {
                script{
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
    }
    post {
        success {
            mail bcc: '', body: "构建版本成功", cc: '', charset: 'UTF-8', from: 'rg_164518@126.com', mimeType: 'text/plain', replyTo: '', subject: "构建版本成功", to: "1918520482@qq.com";
        }
        failure {
            mail bcc: '', body: "<!DOCTYPEhtml><html><head><metacharset="utf-8"><title></title><styletype="text/css">h3{font-size:16px;line-height:10px;letter-spacing:1px;}table{border:1pxsolidblack;border-collapse:collapse;}th,td{border:1pxsolidblack;}th{background:#CCCCCC;}</style></head><body><h3>${env.JOB_NAME}项目测试版本信息</h3><divid='tb1'><table><tr><th>测试版本</th><td>${env.BUILD_NUMBER}</td></tr><tr><th>测试环境</th><td>${env.BUILD_URL}</td></tr></table></div><h3>测试用例统计</h3><divid='tb2'><table><thead><th>执行用例数</th><th>通过用例数</th><th>失败用例数</th><th>通过率</th><th>测试结果</th></thead><tr><td>100</td><td>100</td><td>0</td><td>100%</td><td>PASS</td></tr></table></div><h3>测试详情可点击以下链接</h3><div><ahref='#'>rf报告</a><ahref='#'>rf日志</a></div></body></html>", cc: '', charset: 'UTF-8', from: 'rg_164518@126.com', mimeType: 'text/plain', replyTo: '', subject: "构建版本失败", to: "1918520482@qq.com";
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