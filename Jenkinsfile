pipeline {
  agent any
  options { timestamps() }
  environment {
    REGISTRY = "local/autoqa"
    IMAGE_ORCH = "${REGISTRY}/orchestrator:latest"
    IMAGE_CYP = "${REGISTRY}/cypress-runner:latest"
    IMAGE_SEL = "${REGISTRY}/selenium-tests:latest"
    KUBE_CONTEXT = "kind-kind"
  }
  triggers { cron('H H * * 1-5') } // weekday nightly
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Build Images') {
      parallel {
        stage('Orchestrator Image') {
          steps { sh 'docker build -f docker/orchestrator.Dockerfile -t $IMAGE_ORCH .' }
        }
        stage('Cypress Runner Image') {
          steps { sh 'docker build -f docker/cypress-runner.Dockerfile -t $IMAGE_CYP .' }
        }
        stage('Selenium Tests Image') {
          steps { sh 'docker build -f docker/selenium-tests.Dockerfile -t $IMAGE_SEL .' }
        }
      }
    }
    stage('Unit Tests') {
      parallel {
        stage('Selenium Pytest') {
          steps { sh 'cd selenium && python3 -m pip install -r requirements.txt && pytest -q --junitxml=report-junit.xml' }
          post { always { junit 'selenium/report-junit.xml' } }
        }
        stage('Cypress Headless') {
          steps { sh 'cd cypress && npm ci && npx cypress run --reporter junit --reporter-options "mochaFile=junit-[hash].xml"' }
          post { always { junit 'cypress/junit-*.xml' } }
        }
      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        sh '''
        kubectl apply -f infra/k8s/namespace.yaml
        kubectl apply -f infra/k8s/orchestrator-deploy.yaml
        kubectl apply -f infra/k8s/orchestrator-svc.yaml
        kubectl apply -f infra/k8s/selenium-grid.yaml
        kubectl apply -f infra/k8s/jenkins-deploy.yaml
        kubectl apply -f infra/k8s/grafana-deploy.yaml
        kubectl -n autoqa rollout status deploy/autoqa-orchestrator
        '''
      }
    }
    stage('Schedule Suites') {
      steps {
        sh 'curl -sS http://autoqa-orchestrator.autoqa.svc.cluster.local:8080/schedule -H "Content-Type: application/json" -d \'{"suite":"regression"}\''
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: 'cypress/junit-*.xml, selenium/report-junit.xml', fingerprint: true
    }
  }
}
