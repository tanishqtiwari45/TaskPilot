pipeline {
    agent any

    options {
        buildDiscarder(
            logRotator(
                numToKeepStr: '10',
                artifactNumToKeepStr: '5'
            )
        )

        timeout(time: 20, unit: 'MINUTES')
        timestamps()
        disableConcurrentBuilds()
    }

    parameters {
        string(
            name: 'BRANCH_NAME',
            defaultValue: 'main',
            description: 'Git branch to build'
        )
    }

    triggers {
        githubPush()
    }

    environment {
        // Project
        FRONTEND_DIR = 'frontend'
        UAT_ROOT = 'C:\\TaskPilot-UAT'
        PROD_ROOT = 'C:\\TaskPilot-PROD'

        // Python
        PYTHON_EXE = 'C:\\Users\\Tanishq Tiwari\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
        VENV_DIR = "${WORKSPACE}\\.venv"
        PYTHONPATH = "${WORKSPACE}"

        // MySQL / UAT runtime configuration
        DB_HOST = '127.0.0.1'
        DB_PORT = '3306'
        DB_USER = 'root'
        DB_PASSWORD = 'Octe@2026$#'
        DB_NAME = 'task_pilot'

        // Production Configuration
        PROD_PORT = '5001'
        PROD_ENV = 'production'
    }

    stages {

        // =========================================================
        // 1. CHECKOUT
        // =========================================================
        stage('Checkout') {
            steps {
                echo '=================================================='
                echo '              TASKPILOT CHECKOUT'
                echo '=================================================='

                // Jenkins already performs the SCM checkout
                // because the job uses "Pipeline script from SCM".

                bat '''
                    echo Workspace:
                    echo "%WORKSPACE%"

                    echo.
                    echo Current Git revision:
                    git rev-parse --short HEAD

                    echo.
                    echo Current branch:
                    git branch --show-current
                '''

                echo 'Repository checkout completed.'
            }
        }

        // =========================================================
        // 2. BACKEND SETUP
        // =========================================================
        stage('Backend Setup') {
            steps {
                echo '=================================================='
                echo '              BACKEND SETUP'
                echo '=================================================='

                bat '''
                    echo Python executable:
                    "%PYTHON_EXE%" --version

                    if errorlevel 1 (
                        echo ERROR: Python executable could not be started.
                        exit /b 1
                    )

                    echo.
                    echo Pip:
                    "%PYTHON_EXE%" -m pip --version

                    if errorlevel 1 (
                        echo ERROR: pip is not available.
                        exit /b 1
                    )

                    echo.
                    echo Checking requirements.txt...

                    if not exist "%WORKSPACE%\\requirements.txt" (
                        echo ERROR: requirements.txt was not found.
                        exit /b 1
                    )

                    echo requirements.txt found.

                    echo.
                    echo Removing old virtual environment...

                    if exist "%VENV_DIR%" (
                        rmdir /S /Q "%VENV_DIR%"
                    )

                    echo.
                    echo Creating Python virtual environment...

                    "%PYTHON_EXE%" -m venv "%VENV_DIR%"

                    if errorlevel 1 (
                        echo ERROR: Failed to create virtual environment.
                        exit /b 1
                    )

                    if not exist "%VENV_DIR%\\Scripts\\python.exe" (
                        echo ERROR: Virtual environment Python executable was not created.
                        exit /b 1
                    )

                    echo.
                    echo Virtual environment created successfully.

                    echo.
                    echo Virtual environment Python:
                    "%VENV_DIR%\\Scripts\\python.exe" --version

                    echo.
                    echo Upgrading pip...

                    "%VENV_DIR%\\Scripts\\python.exe" -m pip install --upgrade pip setuptools wheel

                    if errorlevel 1 (
                        echo ERROR: Failed to upgrade pip.
                        exit /b 1
                    )

                    echo.
                    echo Installing backend dependencies...

                    "%VENV_DIR%\\Scripts\\python.exe" -m pip install -r "%WORKSPACE%\\requirements.txt"

                    if errorlevel 1 (
                        echo ERROR: Backend dependency installation failed.
                        exit /b 1
                    )

                    echo.
                    echo Installing pytest...

                    "%VENV_DIR%\\Scripts\\python.exe" -m pip install pytest pytest-cov

                    if errorlevel 1 (
                        echo ERROR: pytest installation failed.
                        exit /b 1
                    )

                    echo.
                    echo Backend environment ready.
                '''
            }
        }

        // =========================================================
        // 3. BACKEND TESTS
        // =========================================================
        stage('Backend Tests') {
            steps {
                echo '=================================================='
                echo '              BACKEND TESTS'
                echo '=================================================='

                bat '''
                    if not exist "%VENV_DIR%\\Scripts\\python.exe" (
                        echo ERROR: Virtual environment does not exist.
                        exit /b 1
                    )

                    if exist "%WORKSPACE%\\tests" (

                        echo Tests directory found.
                        echo Running pytest...

                        "%VENV_DIR%\\Scripts\\python.exe" -m pytest "%WORKSPACE%\\tests" -v --tb=short

                        if errorlevel 1 (
                            echo ERROR: Backend tests failed.
                            exit /b 1
                        )

                        echo.
                        echo Backend tests passed successfully.

                    ) else (

                        echo No tests directory found.
                        echo Running Python syntax validation...

                        "%VENV_DIR%\\Scripts\\python.exe" -m compileall -q "%WORKSPACE%"

                        if errorlevel 1 (
                            echo ERROR: Python syntax validation failed.
                            exit /b 1
                        )

                        echo Python syntax validation passed.
                    )
                '''
            }
        }

        // =========================================================
        // 4. FRONTEND SETUP
        // =========================================================
        stage('Frontend Setup') {
            steps {
                echo '=================================================='
                echo '              FRONTEND SETUP'
                echo '=================================================='

                bat '''
                    cd /d "%WORKSPACE%\\%FRONTEND_DIR%"

                    echo Frontend directory:
                    cd

                    echo.
                    echo Checking package.json...

                    if not exist "package.json" (
                        echo ERROR: frontend\\package.json was not found.
                        exit /b 1
                    )

                    echo package.json found.

                    echo.
                    echo Node version:
                    node --version

                    if errorlevel 1 (
                        echo ERROR: Node.js is not available to Jenkins.
                        exit /b 1
                    )

                    echo.
                    echo npm version:
                    npm --version

                    if errorlevel 1 (
                        echo ERROR: npm is not available to Jenkins.
                        exit /b 1
                    )

                    echo.
                    echo Checking npm configuration...

                    npm config get registry

                    echo.
                    echo Removing old node_modules...

                    if exist "node_modules" (
                        rmdir /S /Q "node_modules"
                    )

                    echo.
                    echo Installing frontend dependencies...

                    if exist "package-lock.json" (

                        echo package-lock.json found.
                        echo Running npm ci...

                        npm ci --no-audit --no-fund

                        if errorlevel 1 (
                            echo ERROR: npm ci failed.
                            exit /b 1
                        )

                    ) else (

                        echo package-lock.json not found.
                        echo Running npm install...

                        npm install --no-audit --no-fund

                        if errorlevel 1 (
                            echo ERROR: npm install failed.
                            exit /b 1
                        )
                    )

                    echo.
                    echo Verifying node_modules...

                    if not exist "node_modules" (
                        echo ERROR: node_modules directory was not created.
                        exit /b 1
                    )

                    echo node_modules created successfully.

                    echo.
                    echo Checking Vite package...

                    npm ls vite --depth=0

                    if errorlevel 1 (
                        echo ERROR: Vite is not installed as a project dependency.
                        echo.
                        echo package.json dependencies:
                        type package.json
                        exit /b 1
                    )

                    echo.
                    echo Checking Vite executable...

                    if not exist "node_modules\\.bin\\vite.cmd" (
                        echo ERROR: node_modules\\.bin\\vite.cmd was not created.
                        echo.
                        echo Contents of node_modules\\.bin:
                        dir "node_modules\\.bin"
                        exit /b 1
                    )

                    echo Vite executable found successfully.

                    echo.
                    echo Testing Vite version...

                    npx --no-install vite --version

                    if errorlevel 1 (
                        echo ERROR: Local Vite executable could not run.
                        exit /b 1
                    )

                    echo.
                    echo Frontend setup completed successfully.
                '''
            }
        }

        // =========================================================
        // 5. FRONTEND BUILD
        // =========================================================
        stage('Frontend Build') {
            steps {
                echo '=================================================='
                echo '              FRONTEND BUILD'
                echo '=================================================='

                bat '''
                    cd /d "%WORKSPACE%\\%FRONTEND_DIR%"

                    echo Checking if frontend dependencies are installed...

                    if not exist "node_modules\\.bin\\vite.cmd" (
                        echo Vite dependency missing. Installing frontend dependencies...

                        if exist "package-lock.json" (
                            npm ci --no-audit --no-fund
                        ) else (
                            npm install --no-audit --no-fund
                        )

                        if errorlevel 1 (
                            echo ERROR: Frontend dependency installation failed.
                            exit /b 1
                        )
                    ) else (
                        echo Frontend dependencies already installed.
                    )

                    echo.
                    echo Running frontend production build...
                    npm run build

                    if errorlevel 1 (
                        echo ERROR: Vite production build failed.
                        exit /b 1
                    )

                    echo.
                    echo Verifying build output...

                    if not exist "dist" (
                        echo ERROR: dist directory was not created.
                        exit /b 1
                    )

                    echo.
                    echo Frontend build completed successfully.

                    echo.
                    echo Build output:
                    dir "dist"
                '''
            }
        }

        // =========================================================
        // 6. PACKAGE APPLICATION
        // =========================================================
        stage('Package Application') {
            steps {
                echo '=================================================='
                echo '             PACKAGE APPLICATION'
                echo '=================================================='

                bat '''
                    setlocal enabledelayedexpansion

                    set "PACKAGE_ROOT=%UAT_ROOT%\\releases\\TaskPilot-UAT-%BUILD_NUMBER%"
                    set "PACKAGE_ZIP=%UAT_ROOT%\\releases\\TaskPilot-UAT-%BUILD_NUMBER%.zip"

                    if exist "%UAT_ROOT%" (
                        rmdir /S /Q "%UAT_ROOT%"
                    )

                    mkdir "%UAT_ROOT%"
                    mkdir "%UAT_ROOT%\\releases"
                    mkdir "%UAT_ROOT%\\logs"

                    if not exist "%WORKSPACE%\\requirements.txt" (
                        echo ERROR: requirements.txt is missing from the repository.
                        exit /b 1
                    )

                    if not exist "%WORKSPACE%\\%FRONTEND_DIR%\\dist\\index.html" (
                        echo ERROR: Frontend dist index.html is missing.
                        exit /b 1
                    )

                    echo Copying Python backend files...
                    xcopy /E /I /Y "%WORKSPACE%\\*.py" "%PACKAGE_ROOT%\" >nul
                    xcopy /E /I /Y "%WORKSPACE%\\requirements.txt" "%PACKAGE_ROOT%\" >nul
                    if exist "%WORKSPACE%\\.env" (
                        xcopy /Y /H "%WORKSPACE%\\.env" "%PACKAGE_ROOT%\" >nul
                    ) else (
                        echo Creating runtime .env for UAT package...
                        (
                            echo FLASK_ENV=development
                            echo SECRET_KEY=taskpilot-uat-secret-key
                            echo DB_HOST=%DB_HOST%
                            echo DB_PORT=%DB_PORT%
                            echo DB_USER=%DB_USER%
                            echo DB_PASSWORD=%DB_PASSWORD%
                            echo DB_NAME=%DB_NAME%
                        ) > "%PACKAGE_ROOT%\\.env"
                    )

                    echo Copying production frontend files...
                    xcopy /E /I /Y "%WORKSPACE%\\%FRONTEND_DIR%\\dist" "%PACKAGE_ROOT%\\%FRONTEND_DIR%\\dist\" >nul

                    if not exist "%PACKAGE_ROOT%\\app.py" (
                        echo ERROR: Deployment package is missing app.py.
                        exit /b 1
                    )

                    if not exist "%PACKAGE_ROOT%\\%FRONTEND_DIR%\\dist\\index.html" (
                        echo ERROR: Deployment package is missing frontend dist index.html.
                        exit /b 1
                    )

                    echo Creating deployment zip artifact...
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; Compress-Archive -Path '%PACKAGE_ROOT%\\*' -DestinationPath '%PACKAGE_ZIP%' -Force"

                    if errorlevel 1 (
                        echo ERROR: Packaging failed.
                        exit /b 1
                    )

                    echo Package created successfully: %PACKAGE_ZIP%
                '''
            }
        }

        // =========================================================
        // 7. DEPLOY TO UAT
        // =========================================================
        stage('Deploy UAT') {
            steps {
                echo '=================================================='
                echo '               DEPLOY UAT'
                echo '=================================================='

                bat '''
                    setlocal enabledelayedexpansion

                    set "PACKAGE_ROOT=%UAT_ROOT%\\releases\\TaskPilot-UAT-%BUILD_NUMBER%"
                    set "DEPLOY_DIR=%UAT_ROOT%\\current"

                    if exist "%DEPLOY_DIR%" (
                        rmdir /S /Q "%DEPLOY_DIR%"
                    )

                    xcopy /E /I /Y "%PACKAGE_ROOT%\\*" "%DEPLOY_DIR%\\*" >nul

                    if errorlevel 1 (
                        echo ERROR: UAT deployment copy failed.
                        exit /b 1
                    )

                    if not exist "%DEPLOY_DIR%\\app.py" (
                        echo ERROR: UAT deployment directory is missing app.py.
                        exit /b 1
                    )

                    echo UAT deployment completed: %DEPLOY_DIR%
                '''
            }
        }

        // =========================================================
        // 8. UAT HEALTH / SMOKE TEST
        // =========================================================
        stage('UAT Health Check') {
            steps {
                echo '=================================================='
                echo '           UAT HEALTH / SMOKE TEST'
                echo '=================================================='

                bat '''
                    setlocal enabledelayedexpansion

                    set "DEPLOY_DIR=%UAT_ROOT%\\current"
                    set "VENV_DIR=%DEPLOY_DIR%\\.venv"
                    set "LOG_FILE=%UAT_ROOT%\\logs\\taskpilot-uat.log"
                    set "PORT=5000"
                    set "DB_HOST=%DB_HOST%"
                    set "DB_PORT=%DB_PORT%"
                    set "DB_USER=%DB_USER%"
                    set "DB_PASSWORD=%DB_PASSWORD%"
                    set "DB_NAME=%DB_NAME%"

                    if not exist "%DEPLOY_DIR%\\.env" (
                        (
                            echo FLASK_ENV=development
                            echo SECRET_KEY=taskpilot-uat-secret-key
                            echo DB_HOST=%DB_HOST%
                            echo DB_PORT=%DB_PORT%
                            echo DB_USER=%DB_USER%
                            echo DB_PASSWORD=%DB_PASSWORD%
                            echo DB_NAME=%DB_NAME%
                        ) > "%DEPLOY_DIR%\\.env"
                    )

                    echo Preparing the UAT runtime environment...
                    if exist "%VENV_DIR%" (
                        rmdir /S /Q "%VENV_DIR%"
                    )

                    "%PYTHON_EXE%" -m venv "%VENV_DIR%"
                    if errorlevel 1 (
                        echo ERROR: Failed to create the UAT virtual environment.
                        exit /b 1
                    )

                    "%VENV_DIR%\\Scripts\\python.exe" -m pip install --upgrade pip setuptools wheel
                    if errorlevel 1 (
                        echo ERROR: Failed to upgrade pip in UAT environment.
                        exit /b 1
                    )

                    "%VENV_DIR%\\Scripts\\python.exe" -m pip install -r "%DEPLOY_DIR%\\requirements.txt"
                    if errorlevel 1 (
                        echo ERROR: Failed to install backend dependencies in UAT environment.
                        exit /b 1
                    )

                    echo Initializing the UAT database and demo user...
                    "%VENV_DIR%\\Scripts\\python.exe" "%DEPLOY_DIR%\\database.py"
                    if errorlevel 1 (
                        echo ERROR: UAT database initialization failed.
                        exit /b 1
                    )

                    echo Stopping any previous TaskPilot UAT process on the health port...
                    for /f "tokens=1,2,3,4,5" %%a in ('netstat -ano ^| findstr :5000') do (
                        if not "%%e"=="" (
                            taskkill /PID %%e /F >nul 2>&1
                        )
                    )

                    if exist "%LOG_FILE%" (
                        del /Q "%LOG_FILE%"
                    )

                    echo Starting TaskPilot in the UAT environment...
                    start "TaskPilot-UAT" /B "%VENV_DIR%\\Scripts\\python.exe" "%DEPLOY_DIR%\\app.py" > "%LOG_FILE%" 2>&1

                    echo Waiting for the backend to start...
                    timeout /T 15 /NOBREAK >nul

                    echo Calling the TaskPilot health endpoint: http://127.0.0.1:5000/health
                    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
                        "$ErrorActionPreference='Stop'; " ^
                        "$response = Invoke-WebRequest -Uri 'http://127.0.0.1:5000/health' -UseBasicParsing -TimeoutSec 20; " ^
                        "if ($response.StatusCode -ne 200) { " ^
                            "throw 'Health check returned status code ' + $response.StatusCode " ^
                        "}; " ^
                        "$body = $response.Content; " ^
                        "Write-Host 'Response Body: ' $body; " ^
                        "if ($body -notmatch 'healthy') { " ^
                            "throw 'Health endpoint response does not contain healthy status' " ^
                        "}; " ^
                        "Write-Host 'UAT health check passed'"

                    if errorlevel 1 (
                        echo ERROR: UAT health check failed.
                        echo Showing UAT log output:
                        type "%LOG_FILE%"
                        exit /b 1
                    )

                    echo UAT deployment and health check passed successfully.
                '''
            }
        }

        // =========================================================
        // 9. PRODUCTION APPROVAL
        // =========================================================
        stage('Production Approval') {
            steps {
                echo '=================================================='  
                echo '          PRODUCTION DEPLOYMENT APPROVAL'
                echo '=================================================='  
                echo ''
                echo 'UAT has passed successfully.'
                echo ''
                echo 'Ready to deploy to PRODUCTION?'
                echo ''
                echo 'This will deploy the application to:'
                echo 'Location: C:\\TaskPilot-PROD'
                echo 'Port:     5001'
                echo ''

                input(
                    id: 'ProductionApproval',
                    message: 'Deploy to PRODUCTION?',
                    ok: 'Deploy to PROD',
                    submitter: ''
                )

                echo 'PRODUCTION DEPLOYMENT APPROVED'
            }
        }

        // =========================================================
        // 10. DEPLOY PROD
        // =========================================================
        stage('Deploy PROD') {
            steps {
                echo '=================================================='
                echo '            DEPLOY TO PRODUCTION'
                echo '=================================================='

                bat '''
                    setlocal enabledelayedexpansion

                    set "PACKAGE_ROOT=%UAT_ROOT%\\releases\\TaskPilot-UAT-%BUILD_NUMBER%"
                    set "PROD_DEPLOY_DIR=%PROD_ROOT%\\current"

                    if not exist "%PACKAGE_ROOT%" (
                        echo ERROR: UAT artifact not found at %PACKAGE_ROOT%
                        exit /b 1
                    )

                    echo Creating PROD environment structure...
                    if not exist "%PROD_ROOT%" (
                        mkdir "%PROD_ROOT%"
                    )

                    if not exist "%PROD_ROOT%\\releases" (
                        mkdir "%PROD_ROOT%\\releases"
                    )

                    if not exist "%PROD_ROOT%\\logs" (
                        mkdir "%PROD_ROOT%\\logs"
                    )

                    echo Removing previous PROD deployment...
                    if exist "%PROD_DEPLOY_DIR%" (
                        rmdir /S /Q "%PROD_DEPLOY_DIR%"
                    )

                    echo Copying UAT artifact to PROD...
                    xcopy /E /I /Y "%PACKAGE_ROOT%\\*" "%PROD_DEPLOY_DIR%\\*" >nul

                    if errorlevel 1 (
                        echo ERROR: PROD deployment copy failed.
                        exit /b 1
                    )

                    if not exist "%PROD_DEPLOY_DIR%\\app.py" (
                        echo ERROR: PROD deployment directory is missing app.py.
                        exit /b 1
                    )

                    echo PROD deployment copied successfully: %PROD_DEPLOY_DIR%
                '''
            }
        }

        // =========================================================
        // 11. PROD HEALTH CHECK
        // =========================================================
        stage('PROD Health Check') {
            steps {
                echo '=================================================='
                echo '         PRODUCTION HEALTH / SMOKE TEST'
                echo '=================================================='

                bat '''
                    setlocal enabledelayedexpansion

                    set "PROD_DEPLOY_DIR=%PROD_ROOT%\\current"
                    set "PROD_VENV_DIR=%PROD_DEPLOY_DIR%\\.venv"
                    set "PROD_LOG_FILE=%PROD_ROOT%\\logs\\taskpilot-prod.log"
                    set "PROD_PORT=%PROD_PORT%"

                    echo Preparing the PROD runtime environment...
                    if exist "%PROD_VENV_DIR%" (
                        rmdir /S /Q "%PROD_VENV_DIR%"
                    )

                    "%PYTHON_EXE%" -m venv "%PROD_VENV_DIR%"
                    if errorlevel 1 (
                        echo ERROR: Failed to create the PROD virtual environment.
                        exit /b 1
                    )

                    "%PROD_VENV_DIR%\\Scripts\\python.exe" -m pip install --upgrade pip setuptools wheel >nul 2>&1
                    if errorlevel 1 (
                        echo ERROR: Failed to upgrade pip in PROD environment.
                        exit /b 1
                    )

                    "%PROD_VENV_DIR%\\Scripts\\python.exe" -m pip install -r "%PROD_DEPLOY_DIR%\\requirements.txt" >nul 2>&1
                    if errorlevel 1 (
                        echo ERROR: Failed to install backend dependencies in PROD environment.
                        exit /b 1
                    )

                    echo Initializing the PROD database and demo user...
                    "%PROD_VENV_DIR%\\Scripts\\python.exe" "%PROD_DEPLOY_DIR%\\database.py"
                    if errorlevel 1 (
                        echo ERROR: PROD database initialization failed.
                        exit /b 1
                    )

                    echo Stopping any previous TaskPilot PROD process on port %PROD_PORT%...
                    for /f "tokens=1,2,3,4,5" %%a in ('netstat -ano ^| findstr :%PROD_PORT%') do (
                        if not "%%e"=="" (
                            taskkill /PID %%e /F >nul 2>&1
                        )
                    )

                    if exist "%PROD_LOG_FILE%" (
                        del /Q "%PROD_LOG_FILE%"
                    )

                    echo Updating PROD .env configuration...
                    (
                        echo FLASK_ENV=%PROD_ENV%
                        echo SECRET_KEY=taskpilot-prod-secret-key
                        echo DB_HOST=%DB_HOST%
                        echo DB_PORT=%DB_PORT%
                        echo DB_USER=%DB_USER%
                        echo DB_PASSWORD=%DB_PASSWORD%
                        echo DB_NAME=%DB_NAME%
                        echo PORT=%PROD_PORT%
                        echo HOST=0.0.0.0
                    ) > "%PROD_DEPLOY_DIR%\\.env"

                    echo Starting TaskPilot in the PROD environment on port %PROD_PORT%...
                    start "TaskPilot-PROD" /B "%PROD_VENV_DIR%\\Scripts\\python.exe" "%PROD_DEPLOY_DIR%\\app.py" > "%PROD_LOG_FILE%" 2>&1

                    echo Waiting for PROD backend to start...
                    timeout /T 15 /NOBREAK

                    echo Calling the TaskPilot PROD health endpoint: http://127.0.0.1:%PROD_PORT%/health
                    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
                        "$ErrorActionPreference='Stop'; " ^
                        "$response = Invoke-WebRequest -Uri 'http://127.0.0.1:%PROD_PORT%/health' -UseBasicParsing -TimeoutSec 20; " ^
                        "if ($response.StatusCode -ne 200) { " ^
                            "throw 'PROD health check returned status code ' + $response.StatusCode " ^
                        "}; " ^
                        "$body = $response.Content; " ^
                        "Write-Host 'Response Body: ' $body; " ^
                        "if ($body -notmatch 'healthy') { " ^
                            "throw 'PROD health endpoint response does not contain healthy status' " ^
                        "}; " ^
                        "Write-Host 'PROD health check passed'"

                    if errorlevel 1 (
                        echo ERROR: PROD health check failed.
                        echo Showing PROD log output:
                        type "%PROD_LOG_FILE%"
                        exit /b 1
                    )

                    echo PROD deployment and health check passed successfully.
                '''
            }
        }
    }

    post {

        success {
            echo '''
==================================================
       TASKPILOT CI BUILD SUCCESSFUL
==================================================
'''
            echo "Build Number: #${BUILD_NUMBER}"
            echo "Branch: ${params.BRANCH_NAME}"
            echo "Status: SUCCESS"
        }

        failure {
            echo '''
==================================================
         TASKPILOT CI BUILD FAILED
==================================================
'''
            echo "Build Number: #${BUILD_NUMBER}"
            echo "Branch: ${params.BRANCH_NAME}"
            echo "Status: FAILURE"
            echo "Review the failed stage above."
        }

        always {
            echo 'TaskPilot CI pipeline execution completed.'
        }
    }
}