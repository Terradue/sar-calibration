def dockerTag = 'docker.terradue.com/sar-calibration'
def dockerNewVersion = 0.1

pipeline {
    agent any
    stages {
        stage('Build & Publish Docker') {
            steps {
                script {
                    def app = docker.build(dockerTag, "-f .docker/Dockerfile .")
                    def mType=getTypeOfVersion(env.BRANCH_NAME)
                    docker.withRegistry('https://docker.terradue.com', 'docker-terradue') {
                     app.push("${mType}${dockerNewVersion}")
                      app.push("${mType}latest")
                    }
                }
            }
        }
    }
}

def getTypeOfVersion(branchName) {
  
  def matcher = (env.BRANCH_NAME =~ /master/)
  if (matcher.matches())
    return ""
  
  return "dev"
}